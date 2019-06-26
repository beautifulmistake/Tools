"""
参考学习猿人学的对海量或者中量文章去重的算法实现

参考链接：https://github.com/veelion/nshash
"""
import hashlib
import os
import pickle
import re
import traceback


class HashDBLeveldb(object):
    def __init__(self, name):
        """
        初始化方法
        :param name:
        """
        import leveldb
        db_name = name + '.hashdb'
        self.db = leveldb.LevelDB(db_name)

    def get(self, key):
        """
        根据 key  获取 value
        :param key:
        :return:
        """
        if isinstance(key, str):
            key = key.encode('utf-8')
        elif isinstance(key, int):
            key = str(key).encode()
        try:
            value = self.db.Get(key).decode()
        except:
            value = None
        return value

    def put(self, key, value):
        """
        向数据库中添加键值对儿
        :param key:
        :param value:
        :return:
        """
        if isinstance(key, str):
            key = key.encode('utf8')
        elif isinstance(key, int):
            key = str(key).encode('utf8')
        if isinstance(value, str):
            value = value.encode('utf8')
        elif isinstance(value, int):
            value = str(value).encode('utf8')
        # 向数据库中添加键值
        self.db.Put(key, value)


class HashDBMemory(object):
    def __init__(self, name):
        """
        初始化方法
        :param name:
        """
        self.name = name
        self.db_name = name + '.hashdb.pkl'
        self.db = {}
        if os.path.isfile(self.db_name):
            with open(self.db_name, 'rb') as f:
                try:
                    self.db = pickle.load(f)
                except:
                    traceback.print_exc()
                    self.db = {}

    def __del__(self):
        with open(self.db_name, 'wb') as f:
            pickle.dump(self.db, f)

    def get(self, key):
        """
        根据 key 获取 value
        :param key:
        :return:
        """
        return self.db.get(key)

    def put(self, key, value):
        """
        存入 键值 对儿
        :param key:
        :param value:
        :return:
        """
        self.db[key] = value


class NSHash(object):
    def __init__(self, name, hashfunc='md5', hashdb='memory'):
        """
        初始化方法
        :param name:
        :param hashfunc:
        :param hashdb:
        """
        if hashfunc == 'farmhash':
            import farmhash
            self.hasfunc = farmhash.hash64

        elif hashfunc == 'md5':
            def md5hash(s):
                if isinstance(s, str):
                    s = s.encode('utf8')
                return hashlib.md5(s).hexdigest()
            self.hashfunc = md5hash
        else:
            raise Exception('not supported hash function type')
        if hashdb == 'memory':
            self.db = HashDBMemory(name)
        else:
            self.db = HashDBLeveldb(name)
        self.max_similar_id = self.db.get('max_similar_id')
        if self.max_similar_id is None:
            self.max_similar_id = 0

    def get_nshash(self, doc, n=5):
        sentences = re.split(r':|：|；|？|。|！|】|\n', doc)
        ss = [s for s in sentences if len(s) > 30]
        if not ss:
            ss = sentences
        ss.sort(key=lambda a: len(a), reverse=True)
        ss = ss[:n]
        hashes = [self.hashfunc(s) for s in ss]
        return hashes

    def get_similar(self, doc):
        """

        :param doc:
        :return:
        """
        hashes = self.get_nshash(doc)
        doc_similar_id = 0
        simids = []
        for h in hashes:
            simid = self.db.get(h)
            if simid:
                simids.append(simid)
        if simids:
            doc_similar_id = min(simids)
        else:
            self.max_similar_id += 1
            doc_similar_id = self.max_similar_id
        for h in hashes:
            self.db.put(h, doc_similar_id)
        return doc_similar_id