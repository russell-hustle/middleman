from flask import Flask, request, jsonify
from urllib.parse import parse_qs
from requests import get
from flask_cors import CORS
from database import Database


GENIUS_TOKEN = "jnk3Z7zFGcLZsSgZPk0kGifKBUhJzYlhqgDJmbYPCJBxKUVjE1EtudaHvco_90Tr"

app = Flask(__name__)
app.secret_key = 'afhawiq89q2fbq92'
CORS(app)
db = Database() # local config

@app.route('/')
def main():
	return 'CORS is annoying!'

@app.route('/lyrics', methods = ['POST'])
def lyrics_endpoint():
	data = parse_qs(request.get_data().decode('utf-8'))
	url = data['url'][0]
	r = get(url)
	return r.text, 200

@app.route('/getleaderboard', methods = ['GET'])
def leaderboard_endpoint():
    data = db.getAllRankings()
    return jsonify(data), 200

@app.route('/updatescore', methods = ['PUT'])
def updatescore_endpoint():
    data = parse_qs(request.get_data().decode('utf-8'))
    print("parsed data: ", data)
    user_data = db.getUser(data['user_id'][0])
    print("user data: ", user_data)
    if not user_data:
        # user does not yet exist, so we must maketh
        db.addUser(data['user_id'][0])
        user_data = db.getUser(data['user_id'][0])[0]
        new_points = int(data['points'][0]) + int(user_data['points'])
        new_efficiency = float(data['efficiency'][0]) + float(user_data['efficiency']) / 2
        db.updateScore(str(data['user_id'][0]), str(new_points), str(new_efficiency))
        return 'Score successfully updated.', 201
    else:
        new_points = int(data['points'][0]) + int(user_data['points'])
        new_efficiency = float(data['efficiency'][0]) + float(user_data['efficiency']) / 2
        db.updateScore(str(data['user_id'][0]), str(new_points), str(new_efficiency))
        return 'Score successfully updated.', 204

if __name__ == '__main__':
    app.debug = True
    app.run()
