from pymysql import cursors, connect


class Database:

    def __init__(self):
        self.connection = None
        self.cursor = None

    def initConnection(self):
        self.connection = connect(  host = 'leaderboard-database.cp43fezouin8.us-west-2.rds.amazonaws.com',
                                    port = 3306,
                                    user = 'Root',
                                    password = 'password1',
                                    db = 'leaderboard_database')
        self.cursor = self.connection.cursor(cursors.DictCursor)

    def closeConnection(self):
        if self.connection:
            self.connection.close()

    def resetTable(self):
        self.cursor.execute('drop table leaderboard')
        self.connection.commit()
        self.cursor.execute('''create table leaderboard(id integer auto_increment primary key, 
                                                        user_id text, 
                                                        name text, 
                                                        points integer, 
                                                        efficiency float, 
                                                        num_words_tried integer, 
                                                        overall_score float)''')
        self.connection.commit()

    def getUser(self, user_id):
        self.cursor.execute('select * from leaderboard where user_id = (%s)', [user_id])
        user = self.cursor.fetchall()
        return user

    def getAllRankings(self):
        self.cursor.execute('select * from leaderboard')
        all_rankings = self.cursor.fetchall()
        return all_rankings

    def addUser(self, user_id, name):  
        self.cursor.execute('''insert into leaderboard (user_id, name, points, efficiency, num_words_tried, overall_score) 
                                                        values (%s, %s, %s, %s, %s, %s)''', 
                                                        [user_id, name, 0, 0.0, 0, 0.0])
        self.connection.commit()

    def updateScore(self, user_id, points, efficiency, num_words_tried, overall_score):
        self.cursor.execute('''update leaderboard set points = (%s), efficiency = (%s), num_words_tried = (%s), overall_score = (%s)
                               where user_id = (%s)''', [points, efficiency, num_words_tried, overall_score, user_id])
        self.connection.commit()
