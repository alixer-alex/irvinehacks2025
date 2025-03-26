
from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import logging
import inspect

#steveyilicious


USERNAME = "irvinehacks2025_2"
PASSWORD = "7Ysteveni*"


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
    # a = Client()
    # username = "filthy_franks_partner"
    # session = a.load_settings("session.json")
    # a.set_settings(session)
    # a.login(USERNAME, PASSWORD)
    # user_id = a.user_info_by_username_v1(username).pk
    # dictt = a.user_followers(user_id)
    # result = {username: []}
    # for short in dictt.values():
    #     result[username].append(short.username)
    # print(result)

    


    first_time_login_user()
