from tinydb import TinyDB, Query, where
from tinydb.operations import set

# leaderboard logic for the lyrical web app
# methods it will need to support:
#   GET: return the leaderboard in json  /getleaderboard
#   POST: add a new user to the database  /adduser
#   POST: update someone's score in the database  /updatescore

# create table leaderboard(
#   ...> id integer primary key,
#   ...> user_id text,
#   ...> points integer,
#   ...> efficiency float);
   
class Database:

    def __init__(self):
        self.db = TinyDB('db.json')
        self.leaderboard = self.db.table('leaderboard')

    def getUser(self, user_id):
        return self.leaderboard.get(where('user_id') == user_id)

    def getAllRankings(self):
        return self.leaderboard.all()

    def addUser(self, user_id):  
        return self.leaderboard.insert({'user_id' : user_id, 'points' : 0, 'efficiency' : 0.0})

    def updateScore(self, user_id, points, efficiency):
        self.leaderboard.update(set('points', points), where('user_id') == user_id)
        self.leaderboard.update(set('efficiency', efficiency), where('user_id') == user_id)

