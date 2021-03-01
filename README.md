# middleman

A server to bypass CORS, as well as perform SQL queries on an AWS database to manage our leaderboard data. 


Endpoints:

```@app.route('/')```
> Returns a welcome message.

```@app.route('/lyrics', methods = ['POST'])```
> Takes the 'url' data as x-www-form-urlencoded data, and returns the song lyrics in text.

```@app.route('/getleaderboard', methods = ['GET'])```
> Returns the current leaderboard data from the database in json.

```@app.route('/updatescore', methods = ['PUT'])```
> Takes the 'user_id', 'points', and 'efficiency' data as x-www-form-urlencoded data, and returns a proper response code after attempting to update the database. 

```@app.route('/resetleaderboard', methods = ['DELETE'])```
> Takes the 'magic_word' data as x-www-form-urlencoded data, and if it is correct it resets the leaderboard database.
