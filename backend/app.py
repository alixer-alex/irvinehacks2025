
# import time
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS  # Import CORS
import json
from instagrapi import Client
import inspect
from username_processing import follower_processing
import os


app = Flask(__name__, static_folder='./template',static_url_path='/')
CORS(app)
master = follower_processing.startup()
# @app.route('/api/username?')
# def get_current_time():
#     return {'time': time.time()}
@app.route('/')
def home():
	return "<p> Hello! </p>"	

#when someone visits http://localhost:5173/api/<username>, get_username is called
#@app.route('/api/<username>', methods=['GET'])
#def get_username(username): #flask automatically calls this when a user makes an HTTP request
	#"take the username from the info in the url (../api?)"
    #just the usernames of 1 username, process it and send over to follower_processing
    # return a tuple of a blank dictionary, 200 (success code)
	# gives one username at a time
	

	try:
		# username captured by flask: jsonify({"username": username})
		if str(username) == 'x':
			#pdrint("HELLO")
			with open("mutual_followers.json", "r") as f:
				data = json.load(f) 
			return jsonify(data), 200
		follower_processing.main_process_username(str(username),master)
		with open("mutual_followers.json", "r") as f:
				data = json.load(f) 
		return jsonify(data), 200
	except Exception as ex:
		with open("mutual_followers.json", "r") as f:
				data = json.load(f) 
		return jsonify(data), 400
	
# print(get_username(Client()))

if __name__ == '__main__':
	app.run(debug = False, port=os.getenv("PORT", default=5000))
	