
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import logging
import inspect



USERNAME = "steveyivicious"
PASSWORD = "1028571DV"


###ONLY NEEDED ONCE IN YOUR LIFETIME, BECAUSE THIS JUST MAKES "session.json"###
def first_time_login_user():
    cl = Client()
    cl.login(USERNAME, PASSWORD)
    cl.dump_settings("session.json")
    return cl
######################################

# cl = Client()
# cl.login("steveyivicious", "1028571DV")
# print(cl.user_id)

# followers = cl.user_followers(cl.user_id, amount=1)
# other_followers = cl.user_followers()
# print(followers)

###THIS WORKS AFTER YOU LOAD THE SESSION SETTINGS. NO LOGIN NEDED.
#print(cl.user_followers("70684503354")) 

if __name__ == '__main__':
    first_time_login_user()
