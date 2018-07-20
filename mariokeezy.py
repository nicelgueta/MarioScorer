from tweepy import OAuthHandler
import time
import pandas as pd
import json
import datetime
import tweepy
from MarioEnterScores import MarioBoard
import os
from mongo import BotDB

BOTENV = os.environ['BOTENV']

#Variables that contains the user credentials to access Twitter API
consumer_key = os.environ['TWITTER_CONSUMER_KEY']
consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']
access_token = os.environ['TWITTER_ACCESS_TOKEN']
access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

def joinList(List,separator):
    st = ''
    for item in List:
        st+=item+separator
    #remove last separator
    st = st[:len(st)-1]
    return st
def readabledate(unixdate):
    date =  datetime.datetime.fromtimestamp(int(float(unixdate))).strftime('%Y-%m-%d %H:%M:%S')
    return date

class MarioKeezy(tweepy.API):

    def  __init__(self):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        super(MarioKeezy,self).__init__(auth)
        self.db = BotDB(BOTENV)
        self.userDict = self.db.getkv('marioUserDict')

    def convert_api_string_to_tweet_version(self,api_txt):
        api_list = api_txt.split(',')
        new_str = joinList([self.userDict[player]['code'] for player in api_list],',')
        return new_str

    def runtweetfunc(self,apistr):
        self.db.log.info('Mario input -- %s' % (apistr))

        #reply tweet with results:
        resdf = self.rusFunction(apistr) #your main function
        if not resdf.empty:
            ''' not using image for this iteration on twitter '''
            #imageFile = createDFImage(resdf)
            #tweetback = ('%s - %s - Current Standings'% (readabledate(time.time()) , (joinList([self.userDict[key]['handle'] for key in self.userDict],' ')))) #add handle and current time. time need to prevent a duplicate tweet error
            #self.update_with_media(filename=imageFile,status=tweetback)
            #for testing:
            #img = Image.open(imageFile)
            #img.show()
            self.db.log.info('Complete')
            return resdf
        else:
            tweetback = ('%s - %s - ' % (readabledate(time.time()) , 'Error - invalid tweet'))
            self.db.log.info('failure')
            #self.update_status(tweetback)

        self.db.log.info('Replied with - %s' % (tweetback))


    def rusFunction(self,apistr):
        ''' mariokeezy is the twitter handle that will tweet the image your string points to.
        :::the bot automatically adds the handle (  tweeter['handle'] ) in the string to be returned so that borted replies to you directly
        so no need to include it in your string to be returned.
        : apistr is the string of text that was sent.
        : the current format is r,t,n. It works out the number of players based on the length of the string originally tweeted.

        run your code here and return what you want the function to return to the twitter handle as a dataFrame object csv file '''

        #just as an idea to start - to save it being messy i'd just save your other.pys in the save folder
        # and import the main functions into here like:
        #    from Mario import Func1, func2 etc...
        #
        userCodes = {'t':'1','n':'2','r':'3','h':'4'}
        try:
            userCodes[apistr[0]]
        except KeyError:
            self.db.log.info('Invalid tweet')
            return pd.DataFrame()
        if len(apistr) == 3:
            winner = userCodes[apistr[0]]
            loser = userCodes[apistr[2]]
            nump = 2

        elif len(apistr) == 5:
            #logic for three players
            winner = userCodes[apistr[0]]
            middle1 = userCodes[apistr[2]]
            loser = userCodes[apistr[4]]
            nump = 3

        elif len(apistr) == 7:
            #logic for four players
            winner = userCodes[apistr[0]]
            middle1 = userCodes[apistr[2]]
            middle2 = userCodes[apistr[4]]
            loser = userCodes[apistr[6]]
            nump = 4

        else:
            #if something's wrong - empty df
            return pd.DataFrame()

        #run func
        a = MarioBoard(self.db)
        if nump == 2:
            a.RankPlayers(nump,winner,loser)
        elif nump == 3:
            a.RankPlayers(nump,winner,loser,middle1)
        elif nump == 4:
            a.RankPlayers(nump,winner,loser,middle1,middle2)
        a.BuildCurrentRating()
        a.Play()
        df = a.UpdateFrame()

        return df

def createDFImage(df):
    '''turns a dataFrame into an png image, returns the filename '''
    ax = plt.subplot(111, frame_on=False) # no visible frame
    ax.xaxis.set_visible(False)  # hide the x axis
    ax.yaxis.set_visible(False)  # hide the y axis
    print(df)
    df = df.drop(['draws','sigma'],1)
    plt.table(ax, df, rowLabels=['']*df.shape[0], loc='center')
    filename = 'Mario_Standings.png'
    plt.savefig(filename)
    return filename


if __name__ == '__main__':

    a = MarioKeezy()
