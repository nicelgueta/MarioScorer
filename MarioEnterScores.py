from trueskill import Rating, quality_1vs1, rate_1vs1, rate, TrueSkill
import pandas as pd
import numpy as np
import csv
import time

todaytime = time.strftime("%d/%m/%Y")


class MarioBoard(object):

    def __init__(self,db):
        self.mariodb = db.mariodb
        self.db = db
        self.playerdf = self.load_db_table()
        self.playerdf.index = np.arange(1,len(self.playerdf)+1)
        self.playerdf.sort_values(by='Name', ascending=0)

        #print(self.playerdf)
        # print(self.playerdf.loc[1,'Name'])
        self.active = []
        self.nowinners = []
        self.norunners = []
        self.nothird = []
        self.response = []
        self.ratings = []
        self.newsigmas = []
        self.newmeans = []

    def load_db_table(self):
        dbdoc = self.mariodb.find_one({'docType':'table'})
        df = pd.DataFrame.from_records(dbdoc['table'])
        return df
    def save_db_table(self,df):
        dfDict = list(df.T.to_dict().values())
        self.mariodb.update_one({'docType':'table'},{'$set':{'dataFrameDict':dfDict}})
        return

    def Leaderboard(self):
        self.playerdf.sort_values('Name', ascending=0)
        self.db.log.info(self.playerdf.to_html()) #.sort('mu', ascending=False))

    def RankPlayers(self,nump,winner,loser,mid1=False,mid2=False):
        self.db.log.info(self.playerdf.to_html())
        #nump = input("Pick number of players (2-4): ")
        self.response = nump
        # Two players
        if int(nump) == 2:
            rank1 = winner
            if len(rank1) > 1:
                self.active.append(rank1[0])
                self.active.append(rank1[2])
                self.nowinners.append(2)

            if len(rank1) == 1:
                rank2 = loser
                self.active.append(rank1)
                self.active.append(rank2)
                self.nowinners.append(1)
                self.norunners.append(1)

            #print(self.active)
        elif int(nump) == 3:
            rank1 = winner
            # All Three rank differently
            if len(rank1) == 1:
                rank2 = mid1
                if len(rank2) > 1:
                    self.active.append(rank1)
                    self.active.append(rank2[0])
                    self.active.append(rank2[2])
                    self.nowinners.append(1)
                    self.norunners.append(2)
                if len(rank2) == 1:
                    rank3 = loser
                    self.active.append(rank1)
                    self.active.append(rank2)
                    self.active.append(rank3)
                    self.nowinners.append(1)
                    self.norunners.append(1)
                    self.nothird.append(1)


        elif int(nump) == 4:
            rank1 = winner
            rank2 = mid1
            rank3 = mid2
            rank4 = loser
            self.active.append(rank1)
            self.active.append(rank2)
            self.active.append(rank3)
            self.active.append(rank4)
        # To Congratulate the players


    def BuildCurrentRating(self):
        # 2p
        if int(self.response) == 2:
            Winmu=float(self.playerdf.loc[int(self.active[0]),'mu'])
            Winsig=float(self.playerdf.loc[int(self.active[0]),'sigma'])
            Runmu=float(self.playerdf.loc[int(self.active[1]),'mu'])
            Runsig=float(self.playerdf.loc[int(self.active[1]),'sigma'])
            WinEnv = TrueSkill(mu=Winmu, sigma=Winsig, draw_probability=0.05, backend=None)
            WinEnv.make_as_global()
            r1=Rating()
            RunEnv = TrueSkill(mu=Runmu, sigma=Runsig, draw_probability=0.05, backend=None)
            RunEnv.make_as_global()
            r2=Rating()
            self.ratings.append(r1)
            self.ratings.append(r2)
        # 3p
        elif int(self.response) == 3:
            oneMu=float(self.playerdf.loc[int(self.active[0]),'mu'])
            oneSig=float(self.playerdf.loc[int(self.active[0]),'sigma'])
            twoMu=float(self.playerdf.loc[int(self.active[1]),'mu'])
            twoSig=float(self.playerdf.loc[int(self.active[1]),'sigma'])
            thrMu=float(self.playerdf.loc[int(self.active[2]),'mu'])
            thrSig=float(self.playerdf.loc[int(self.active[2]),'sigma'])

            WinEnv = TrueSkill(mu=oneMu, sigma=oneSig, draw_probability=0.05, backend=None)
            WinEnv.make_as_global()
            r1=Rating()

            RunEnv = TrueSkill(mu=twoMu, sigma=twoSig, draw_probability=0.05, backend=None)
            RunEnv.make_as_global()
        # print(Rating())
            r2=Rating()

            ThrEnv = TrueSkill(mu=thrMu, sigma=thrSig, draw_probability=0.05, backend=None)
            ThrEnv.make_as_global()
        # print(Rating())
            r3=Rating()
            self.ratings.append(r1)
            self.ratings.append(r2)
            self.ratings.append(r3)

        elif int(self.response) == 4:
            oneMu=float(self.playerdf.loc[int(self.active[0]),'mu'])
            oneSig=float(self.playerdf.loc[int(self.active[0]),'sigma'])
            twoMu=float(self.playerdf.loc[int(self.active[1]),'mu'])
            twoSig=float(self.playerdf.loc[int(self.active[1]),'sigma'])
            thrMu=float(self.playerdf.loc[int(self.active[2]),'mu'])
            thrSig=float(self.playerdf.loc[int(self.active[2]),'sigma'])
            frMu=float(self.playerdf.loc[int(self.active[3]),'mu'])
            frSig=float(self.playerdf.loc[int(self.active[3]),'sigma'])

            WinEnv = TrueSkill(mu=oneMu, sigma=oneSig, draw_probability=0.05, backend=None)
            WinEnv.make_as_global()
        # print(Rating())
            r1=Rating()

            RunEnv = TrueSkill(mu=twoMu, sigma=twoSig, draw_probability=0.05, backend=None)
            RunEnv.make_as_global()
        # print(Rating())
            r2=Rating()

            ThrEnv = TrueSkill(mu=thrMu, sigma=thrSig, draw_probability=0.05, backend=None)
            ThrEnv.make_as_global()
        # print(Rating())
            r3=Rating()

            FrEnv = TrueSkill(mu=frMu, sigma=frSig, draw_probability=0.05, backend=None)
            FrEnv.make_as_global()
        # print(Rating())
            r4=Rating()

            self.ratings.append(r1)
            self.ratings.append(r2)
            self.ratings.append(r3)
            self.ratings.append(r4)

    def Play(self):
        # 2p: game between 2 players and only one winner
        if int(self.response) == 2 and int(self.nowinners[0]) == 1:
            new_r1, new_r2 = rate_1vs1(self.ratings[0],self.ratings[1])
            print(new_r1)
            print(new_r2)
            # make rating object a string
            k1a =  str(new_r1)
            k2a = str(new_r2)
            # New sigmas
            newr1sig = k1a[k1a.index("sigma=") + len("sigma="):][0:-1]
            newr2sig = k2a[k2a.index("sigma=") + len("sigma="):][0:-1]
            self.newsigmas.append(newr1sig)
            self.newsigmas.append(newr2sig)
            # New Means truncated to support those below 100
            newr1mean = k1a[20:26]
            newr2mean = k2a[20:26]
            self.newmeans.append(newr1mean)
            self.newmeans.append(newr2mean)
            print(newr1mean)
            print(newr2mean)

        # 2p: game between 2 players and two winners (draw)
        if int(self.response) == 2 and int(self.nowinners[0]) == 2:
            new_r1, new_r2 = rate_1vs1(self.ratings[0],self.ratings[1], drawn=True)
            print(new_r1)
            print(new_r2)
           # leaderboard = sorted(self.ratings, key=env.expose, reverse=True)
            # make rating object a string
            k1a =  str(new_r1)
            k2a = str(new_r2)
            # New sigmas
            newr1sig = k1a[k1a.index("sigma=") + len("sigma="):][0:-1]
            newr2sig = k2a[k2a.index("sigma=") + len("sigma="):][0:-1]
            self.newsigmas.append(newr1sig)
            self.newsigmas.append(newr2sig)
            # New Means truncated to support those below 100
            newr1mean = k1a[20:26]
            newr2mean = k2a[20:26]
            self.newmeans.append(newr1mean)
            self.newmeans.append(newr2mean)

        # 3p: game between 3 players with two winners (draws)
        if int(self.response) == 3 and int(self.nowinners[0]) == 2:
            (new_r1,), (new_r2,), (new_r3,) = rate([(self.ratings[0],),(self.ratings[1],),(self.ratings[2],)], ranks=(0,0,1))
            print(new_r1)
            print(new_r2)
            print(new_r3)
            # make rating object a string
            k1b =  str(new_r1)
            k2b = str(new_r2)
            k3b = str(new_r3)

            # New sigmas using an index to get the number after sigma in the string of the rating.
            newr1sig = k1b[k1b.index("sigma=") + len("sigma="):][0:-1]
            newr2sig = k2b[k2b.index("sigma=") + len("sigma="):][0:-1]
            newr3sig = k3b[k2b.index("sigma=") + len("sigma="):][0:-1]
            self.newsigmas.append(newr1sig)
            self.newsigmas.append(newr2sig)
            self.newsigmas.append(newr3sig)
            # New Means truncated to support those below 100
            newr1mean = k1b[20:26]
            newr2mean = k2b[20:26]
            newr3mean = k3b[20:26]
            self.newmeans.append(newr1mean)
            self.newmeans.append(newr2mean)
            self.newmeans.append(newr3mean)

        # 3p: game between 3 players no draws
        if int(self.response) == 3 and int(self.nowinners[0]) == 1 and int(self.norunners[0]) == 1:
            (new_r1,), (new_r2,), (new_r3,) = rate([(self.ratings[0],),(self.ratings[1],),(self.ratings[2],)], ranks=(0,1,2))
            print(new_r1)
            print(new_r2)
            print(new_r3)
            # make rating object a string
            k1b =  str(new_r1)
            k2b = str(new_r2)
            k3b = str(new_r3)
            # New sigmas
            newr1sig = k1b[k1b.index("sigma=") + len("sigma="):][0:-1]
            newr2sig = k2b[k2b.index("sigma=") + len("sigma="):][0:-1]
            newr3sig = k3b[k3b.index("sigma=") + len("sigma="):][0:-1]
            self.newsigmas.append(newr1sig)
            self.newsigmas.append(newr2sig)
            self.newsigmas.append(newr3sig)
            # New Means truncated to support those below 100
            newr1mean = k1b[20:26]
            newr2mean = k2b[20:26]
            newr3mean = k3b[20:26]
            self.newmeans.append(newr1mean)
            self.newmeans.append(newr2mean)
            self.newmeans.append(newr3mean)
        # 3p: one winner two runners up in 3p
        if int(self.response) == 3 and int(self.nowinners[0]) == 1 and int(self.norunners[0]) == 2:
            (new_r1,), (new_r2,), (new_r3,) = rate([(self.ratings[0],),(self.ratings[1],),(self.ratings[2],)], ranks=(0,1,1))
            print(new_r1)
            print(new_r2)
            print(new_r3)
            # make rating object a string
            k1b =  str(new_r1)
            k2b = str(new_r2)
            k3b = str(new_r3)
            # New sigmas
            newr1sig = k1b[k1b.index("sigma=") + len("sigma="):][0:-1]
            newr2sig = k2b[k2b.index("sigma=") + len("sigma="):][0:-1]
            newr3sig = k3b[k3b.index("sigma=") + len("sigma="):][0:-1]
            self.newsigmas.append(newr1sig)
            self.newsigmas.append(newr2sig)
            self.newsigmas.append(newr3sig)
            # New Means truncated to support those below 100
            newr1mean = k1b[20:26]
            newr2mean = k2b[20:26]
            newr3mean = k3b[20:26]
            self.newmeans.append(newr1mean)
            self.newmeans.append(newr2mean)
            self.newmeans.append(newr3mean)

        # 4p:
        if int(self.response) == 4:
            (new_r1,), (new_r2,), (new_r3,), (new_r4,) = rate([(self.ratings[0],),(self.ratings[1],),(self.ratings[2],),(self.ratings[3],)], ranks=(0,1,2,3))
            print(new_r1)
            print(new_r2)
            print(new_r3)
            print(new_r4)
            # make rating object a string
            k1c = str(new_r1)
            k2c = str(new_r2)
            k3c = str(new_r3)
            k4c = str(new_r4)
            # New sigmas
            newr1sig = k1c[k1c.index("sigma=") + len("sigma="):][0:-1]
            newr2sig = k2c[k2c.index("sigma=") + len("sigma="):][0:-1]
            newr3sig = k3c[k3c.index("sigma=") + len("sigma="):][0:-1]
            newr4sig = k4c[k4c.index("sigma=") + len("sigma="):][0:-1]
            self.newsigmas.append(newr1sig)
            self.newsigmas.append(newr2sig)
            self.newsigmas.append(newr3sig)
            self.newsigmas.append(newr4sig)
            # New Means truncated to support those below 100
            newr1mean = k1c[20:26]
            newr2mean = k2c[20:26]
            newr3mean = k3c[20:26]
            newr4mean = k4c[20:26]
            self.newmeans.append(newr1mean)
            self.newmeans.append(newr2mean)
            self.newmeans.append(newr3mean)
            self.newmeans.append(newr4mean)

    def UpdateFrame(self):
        # Three player Scenario: Counting Plays, Draws, Losses and Wins.  SOMETHING WRONG WITH WIN COUNTING three player
        if int(self.response) == 3:
            # print(playerdf)
            print(self.active[0])
            # everyone gets a played count
            self.playerdf.loc[int(self.active[0]), 'played'] = int(self.playerdf.loc[int(self.active[0]), 'played']) + 1
            self.playerdf.loc[int(self.active[1]), 'played'] = int(self.playerdf.loc[int(self.active[1]), 'played']) + 1
            self.playerdf.loc[int(self.active[2]), 'played'] = int(self.playerdf.loc[int(self.active[2]), 'played']) + 1
            self.playerdf.loc[int(self.active[0]), 'sigma'] = self.newsigmas[0]
            self.playerdf.loc[int(self.active[1]), 'sigma'] = self.newsigmas[1]
            self.playerdf.loc[int(self.active[2]), 'sigma'] = self.newsigmas[2]
            self.playerdf.loc[int(self.active[0]), 'mu'] = self.newmeans[0]
            self.playerdf.loc[int(self.active[1]), 'mu'] = self.newmeans[1]
            self.playerdf.loc[int(self.active[2]), 'mu'] = self.newmeans[2]
            self.playerdf.loc[int(self.active[0]), 'LastGame'] = todaytime
            self.playerdf.loc[int(self.active[1]), 'LastGame'] = todaytime
            self.playerdf.loc[int(self.active[2]), 'LastGame'] = todaytime

            # p1/p2 joint win (draw and a win for p1 and p2, loss for p3)
            if int(self.response) == 3 and int(self.nowinners[0]) == 2:
                self.playerdf.loc[int(self.active[0]), 'draws'] = int(self.playerdf.loc[int(self.active[0]), 'draws']) + 1
                self.playerdf.loc[int(self.active[1]), 'draws'] = int(self.playerdf.loc[int(self.active[1]), 'draws']) + 1
                self.playerdf.loc[int(self.active[0]), 'wins'] = int(self.playerdf.loc[int(self.active[0]), 'wins']) + 1
                self.playerdf.loc[int(self.active[1]), 'wins'] = int(self.playerdf.loc[int(self.active[1]), 'wins']) + 1
                self.playerdf.loc[int(self.active[2]), 'losses'] = int(self.playerdf.loc[int(self.active[2]), 'losses']) + 1
            # p2/p3 joint loss (draw and a loss counted for p2/p3, win for p1)
            if int(self.norunners[0]) == 2 and int(self.nowinners[0]) == 1:
                self.playerdf.loc[int(self.active[0]), 'wins'] = int(self.playerdf.loc[int(self.active[0]), 'wins']) + 1
                self.playerdf.loc[int(self.active[1]), 'draws'] = int(self.playerdf.loc[int(self.active[1]), 'draws']) + 1
                self.playerdf.loc[int(self.active[2]), 'draws'] = int(self.playerdf.loc[int(self.active[2]), 'draws']) + 1
                self.playerdf.loc[int(self.active[1]), 'losses'] = int(self.playerdf.loc[int(self.active[1]), 'losses']) + 1
                self.playerdf.loc[int(self.active[2]), 'losses'] = int(self.playerdf.loc[int(self.active[2]), 'losses']) + 1
            if int(self.norunners[0]) == 1 and int(self.nowinners[0]) == 1:
                self.playerdf.loc[int(self.active[0]), 'wins'] = int(self.playerdf.loc[int(self.active[0]), 'wins']) + 1
                self.playerdf.loc[int(self.active[2]), 'losses'] = int(self.playerdf.loc[int(self.active[2]), 'losses']) + 1
                self.db.log.info(self.playerdf.to_html())
                self.save_db_table(self.playerdf)

        # Two player scenario: Counting Plays, Draws, Losses and Wins.
        if int(self.response) == 2:
            # print(self.playerdf)
            print(self.active[0])
            self.playerdf.loc[int(self.active[0]), 'played'] = int(self.playerdf.loc[int(self.active[0]), 'played']) + 1
            self.playerdf.loc[int(self.active[1]), 'played'] = int(self.playerdf.loc[int(self.active[1]), 'played']) + 1
            self.playerdf.loc[int(self.active[0]), 'sigma'] = self.newsigmas[0]
            self.playerdf.loc[int(self.active[1]), 'sigma'] = self.newsigmas[1]
            self.playerdf.loc[int(self.active[0]), 'mu'] = self.newmeans[0]
            self.playerdf.loc[int(self.active[1]), 'mu'] = self.newmeans[1]
            self.playerdf.loc[int(self.active[0]), 'LastGame'] = todaytime
            self.playerdf.loc[int(self.active[1]), 'LastGame'] = todaytime
            if int(self.response) == 2 and int(self.nowinners[0]) == 2:
                self.playerdf.loc[int(self.active[0]), 'draws'] = int(self.playerdf.loc[int(self.active[0]), 'draws']) + 1
                self.playerdf.loc[int(self.active[1]), 'draws'] = int(self.playerdf.loc[int(self.active[1]), 'draws']) + 1
            elif int(self.nowinners[0]) == 1:
                self.playerdf.loc[int(self.active[0]), 'wins'] = int(self.playerdf.loc[int(self.active[0]), 'wins']) + 1
                self.playerdf.loc[int(self.active[1]), 'losses'] = int(self.playerdf.loc[int(self.active[1]), 'losses']) + 1
            # 2/3 draw
            self.db.log.info(self.playerdf.to_html())
            self.save_db_table(self.playerdf)
        if int(self.response) == 4:
            # self.db.log.info(self.playerdf.to_html())
            print(self.active[0])
            self.playerdf.loc[int(self.active[0]), 'played'] = int(self.playerdf.loc[int(self.active[0]), 'played']) + 1
            self.playerdf.loc[int(self.active[1]), 'played'] = int(self.playerdf.loc[int(self.active[1]), 'played']) + 1
            self.playerdf.loc[int(self.active[2]), 'played'] = int(self.playerdf.loc[int(self.active[2]), 'played']) + 1
            self.playerdf.loc[int(self.active[3]), 'played'] = int(self.playerdf.loc[int(self.active[3]), 'played']) + 1
            self.playerdf.loc[int(self.active[0]), 'sigma'] = self.newsigmas[0]
            self.playerdf.loc[int(self.active[1]), 'sigma'] = self.newsigmas[1]
            self.playerdf.loc[int(self.active[2]), 'sigma'] = self.newsigmas[2]
            self.playerdf.loc[int(self.active[3]), 'sigma'] = self.newsigmas[3]
            self.playerdf.loc[int(self.active[0]), 'mu'] = self.newmeans[0]
            self.playerdf.loc[int(self.active[1]), 'mu'] = self.newmeans[1]
            self.playerdf.loc[int(self.active[2]), 'mu'] = self.newmeans[2]
            self.playerdf.loc[int(self.active[3]), 'mu'] = self.newmeans[3]
            self.playerdf.loc[int(self.active[0]), 'LastGame'] = todaytime
            self.playerdf.loc[int(self.active[1]), 'LastGame'] = todaytime
            self.playerdf.loc[int(self.active[2]), 'LastGame'] = todaytime
            self.playerdf.loc[int(self.active[3]), 'LastGame'] = todaytime
            self.db.log.info(self.playerdf.to_html())
            self.save_db_table(self.playerdf)
        return self.playerdf




# print('{:.1%} chance to draw'.format(quality_1vs1(r1, r2)))
