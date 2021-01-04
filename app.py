from flask import Flask, request, jsonify
from urllib.parse import parse_qs
from requests import get
from flask_cors import CORS
from database import Database

GENIUS_TOKEN = 'jnk3Z7zFGcLZsSgZPk0kGifKBUhJzYlhqgDJmbYPCJBxKUVjE1EtudaHvco_90Tr'

app = Flask(__name__)
app.secret_key = 'afhawiq89q2fbq92'
CORS(app)
db = Database() 

@app.route('/')
def main():
	return 'CORS is annoying, also welcome to Middleman!'

@app.route('/lyrics', methods = ['POST'])
def lyrics_endpoint():
	data = parse_qs(request.get_data().decode('utf-8'))
	url = data['url'][0]
	r = get(url)
	return r.text, 200

@app.route('/getleaderboard', methods = ['GET'])
def leaderboard_endpoint():
    db.initConnection()
    data = db.getAllRankings()
    db.closeConnection()
    return jsonify(data), 200

@app.route('/updatescore', methods = ['PUT'])
def updatescore_endpoint():
    data = parse_qs(request.get_data().decode('utf-8'))
    print('parsed data: ', data)
    db.initConnection()
    user_data = db.getUser(data['user_id'][0])
    print('user data: ', user_data)
    if user_data == ():
        # user does not yet exist, so we must maketh
        print('new user!')
        db.addUser(data['user_id'][0], data['name'][0])
        user_data = db.getUser(data['user_id'][0])[0]
        new_points = int(data['points'][0]) + int(user_data['points'])
        new_num_words_tried = int(user_data['num_words_tried']) 
        new_num_words_tried += 1
        new_efficiency = (float(data['efficiency'][0]) + (float(user_data['efficiency']) * int(user_data['num_words_tried']))) / new_num_words_tried 
        new_overall_score = new_points * new_efficiency
        db.updateScore(str(data['user_id'][0]), str(new_points), str(new_efficiency), str(new_num_words_tried), str(new_overall_score))
        db.closeConnection()
        return 'Score successfully updated.', 201
    else:
        new_points = int(data['points'][0]) + int(user_data[0]['points'])
        new_num_words_tried = int(user_data[0]['num_words_tried']) 
        new_num_words_tried += 1
        new_efficiency = (float(data['efficiency'][0]) + (float(user_data[0]['efficiency']) * int(user_data[0]['num_words_tried']))) / new_num_words_tried 
        new_overall_score = new_points * new_efficiency
        db.updateScore(str(data['user_id'][0]), str(new_points), str(new_efficiency), str(new_num_words_tried), str(new_overall_score))
        db.closeConnection()
        return 'Score successfully updated.', 201

@app.route('/resetleaderboard', methods = ['DELETE'])
def resetleaderboard_endpoint():
    data = parse_qs(request.get_data().decode('utf-8'))
    print('parsed data: ', data)
    try:    
        if data['magic_word'][0] == 'russross':
            db.initConnection() 
            db.resetTable()
            db.closeConnection()
            return 'Database successfully reset.', 201
    except:
        pass
    return 'Nice try but I am still smarter.', 403

if __name__ == '__main__':
    app.debug = True
    app.run()
