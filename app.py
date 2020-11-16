from flask import Flask, request
from urllib.parse import parse_qs
from requests import get
from flask_cors import CORS




GENIUS_TOKEN = "jnk3Z7zFGcLZsSgZPk0kGifKBUhJzYlhqgDJmbYPCJBxKUVjE1EtudaHvco_90Tr"

app = Flask(__name__)
app.secret_key = 'afhawiq89q2fbq92'
CORS(app)

@app.route('/')
def main():
	return 'CORS is annoying!'

@app.route('/lyrics', methods = ['POST'])
def lyrics_endpoint():
	data = parse_qs(request.get_data().decode('utf-8'))
	url = data['url'][0]
	r = get(url)
	return r.text, 200

if __name__ == '__main__':
	app.debug = True
	app.run()
