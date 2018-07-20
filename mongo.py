import os
import pymongo
from mongologger import MongoLogger
from config import X

class BotDB(pymongo.database.Database):
    ''' Main DataBase object for interacting with the back-end datbase.
    Carries all same methods as mongo db class but with Bot-specfic methods for
    simpler kv retrieval.

    __init__ Parameters
    ------------
    - Environment - 3 dbs
    - MONGODB_URI - obvious.

    '''
    def __init__(self,environment):
        if environment not in ['DEV','UAT','PROD']:
            raise ValueError('Invalid environment to initialise DB')
        mongo_uri = os.environ['MONGODB_%s'%environment]
        client = pymongo.MongoClient(mongo_uri)
        self.dbname = X['mongo%s'%environment]
        super(BotDB,self).__init__(client,self.dbname)
        #ensure all data points only to the environment-specfic db
        self.env = environment
        self.log = MongoLogger(objName='BotDB',db=self,debug=False, logstodb=X['LOGS_TO_DB'])

    def addkv(self,key,value):
        if not self.kvstore.find_one({'key':key}):
            return self.kvstore.insert_one({'key':key,'value':value})
        else:
            print(key+' already exists - use updatekv method')
            return

    def getkv(self,key):
        r = self.kvstore.find_one({'key':key})
        if not r:
            self.log.warn('key %s not found in database' % key)
            return False
        else:
            val = r['value']
        return val

    def delkv(self,key):
        return self.kvstore.delete_one({'key':key})

    def updatekv(self,key,value):
        r = self.kvstore.update_one({'key':key},{'$set':{'value':value}})
        return r

    def check_long_markers(self,cpair_list):
        self.log.debug('Checking DataBase currency Long markers')
        for cpair in cpair_list:
            r = self.longmarkers.find_one({'currencyPair':cpair})
            if not r:
                self.log.debug('No long marker found for %s - adding to db'%cpair)
                if cpair in C['shortStrategies']:
                    marklong = True
                else:
                    marklong = False
                document = {'currencyPair':cpair,'longMarker':marklong}
                self.longmarkers.insert_one(document)

    def printLogs(self):
        alllogs = self.logs.find()
        #make sure logs print in order
        loglist = [log for log in alllogs]
        lognos = [log['logNo'] for log in loglist]
        maxno = max(lognos)
        minno = min(lognos)
        ordered = []
        i=minno
        while i <= maxno:
            for log in loglist:
                if log['logNo'] == i:
                    ordered.append(log)
            i+=1
        ret = []
        for log in ordered:
            for line in log['logTxt']:
                ret.append(line+'<br/>')
        return ret
