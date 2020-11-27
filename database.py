import sqlite3

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

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]

    return d
    
class Database:

    def __init__(self):
        self.connection = sqlite3.connect('leaderboard.db', check_same_thread = False)
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()

    def getUser(self, user_id):
        self.cursor.execute('select * from leaderboard where user_id = (?)', [user_id])
        return self.cursor.fetchall()

    def getAllRankings(self):
        self.cursor.execute('select * from leaderboard')
        return self.cursor.fetchall()

    def addUser(self, user_id):  
        self.cursor.execute('insert into leaderboard (user_id, points, efficiency) values (?, ?, ?)', [user_id, 0, 0.0])
        self.connection.commit()

    def updateScore(self, user_id, points, efficiency):
        self.cursor.execute('update leaderboard set points = (?), efficiency = (?) where user_id = (?)', [points, efficiency, user_id])
