
# import time
from flask import Flask, jsonify, request
from instagrapi import Client
import inspect
from username_processing import follower_processing

app = Flask(__name__)

# @app.route('/api/username?')
# def get_current_time():
#     return {'time': time.time()}

#when someone visits http://localhost:5173/api/<username>, get_username is called
@app.route('/api/<username>', methods=['GET'])
def get_username(username): #flask automatically calls this when a user makes an HTTP request
	#"take the username from the info in the url (../api?)"
    #just the usernames of 1 username, process it and send over to follower_processing
    # return a tuple of a blank dictionary, 200 (success code)
	# gives one username at a time
	try:
		# username captured by flask: jsonify({"username": username})
		all_followers = follower_processing.get_followers(str(username))
		return jsonify(all_followers), 200
	except Exception as ex:
		return jsonify({"Error": str(ex)}), 400
	
# print(get_username(Client()))

if __name__ == '__main__':
	app.run(debug=True)
