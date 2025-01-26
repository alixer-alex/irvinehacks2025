from instagrapi import Client
import instagrapi as i
from instagrapi.exceptions import LoginRequired
import logging
from pathlib import Path
import json
import inspect


USERNAME = "steveyivicious"
PASSWORD = "1028571DV"
"""
Remember: A connection between nodes is only made when people follow each other

You'll be receiving the username of the new person that entered their username
"""



def example(a, b):
    """
    Args:
        a: a tuple that represents yada yada
        b: a string that represents yada yada
    Returns:
        an integer which represents yada yada
    """
    pass


class CentralAccount:
    def __init__(self):
        self.central_account = Client()


    def login_user(self):
        """
        Attempts to login to Instagram using either the provided session information
        or the provided username and password.
        """
        logger = logging.getLogger()

        self.central_account = Client()
        session = self.central_account.load_settings("session.json")

        login_via_session = False
        login_via_pw = False

        if session:
            try:
                self.central_account.set_settings(session)
                self.central_account.login(USERNAME, PASSWORD)

                # check if session is valid
                try:
                    self.central_account.get_timeline_feed()
                except LoginRequired:
                    logger.info("Session is invalid, need to login via username and password")

                    old_session = self.central_account.get_settings()

                    # use the same device uuids across logins
                    self.central_account.set_settings({})
                    self.central_account.set_uuids(old_session["uuids"])

                    self.central_account.login(USERNAME, PASSWORD)
                login_via_session = True
            except Exception as e:
                logger.info("Couldn't login user using session information: %s" % e)

        if not login_via_session:
            try:
                logger.info("Attempting to login via username and password. username: %s" % USERNAME)
                if self.central_account.login(USERNAME, PASSWORD):
                    login_via_pw = True
            except Exception as e:
                logger.info("Couldn't login user using username and password: %s" % e)

        if not login_via_pw and not login_via_session:
            raise Exception("Couldn't login user with either password or session")
        

    def get_followers(self, username: str):
        """
        Args:
            username: a string that represents the username from which to get the followers
        Returns:
            A dictionary that is of the format: {username_from_arg : [follower1name, follower2name]}
        """
        # get dictionary (key: user id, value: UserShort dict w username, etc.)
        user_id = self.central_account.user_info_by_username(username).pk #need to parse
        dictt = self.central_account.user_followers(user_id)
        result = {username: []}
        for short in dictt.values():
           result[username].append(short.username)
        return result


    def update_all_followers(self, user_with_followers: dict):
        """
        Writes to all_followers.json by appending to its current dictionary with the new dictionary
    
        Args:
            user_with_followers: a dictionary of the format: {username : [follower1name, follower2name]}
        Returns:
            void.
        """
        all_flwrs_path = Path("all_followers.json")
        with all_flwrs_path.open("r") as infile:
            old_users_and_flwrs = infile.read() #returns a string

        #parse the old data
        parsed_old_users_and_flwrs = json.loads(old_users_and_flwrs)

        #append the new data to the old
        parsed_old_users_and_flwrs.update(user_with_followers)

        #write it back to the file
        with all_flwrs_path.open("w") as outfile:
            json.dump(parsed_old_users_and_flwrs, outfile)


    def get_mutuals(self, new_user: dict):
        """
        Gets the mutual followers of a user by checking the all_folowers.json file

        From an optimized design perspective, you only need to check if the new person being added
        has any mutuals with any existing users within the all_followers.json file.

        For each user/key in all_followers.json, you only have to check if the new-user is in that
        person's follower list. DO NOT check the follower lists of each follower of each user in
        all_followers.

        Args:
            new_user: A dictionary of the format {"insert-user's-username-here" : [follower1, follower2]}
        Returns:
            A dictionary of the format {"user's-username-here" : [mutualfollower1, mutualfollower2]}
        """
        mutuals = {new_user.keys()[0]: []}
        file = open('all_followers.json', 'r')
        contents = file.read()
        followers = json.loads(contents)
        
        file.close()

        return mutuals





    def update_mutuals(self, new_mutuals: dict):
        """
        Writes in the mutual followers of a new user into mutual_followers.json
        Here's an example format of the JSON file, except note that in reality, everything will be in-line.
        There will be no newlines in the file

        {
        "steven":
            ["alex","jessica"],
        "alex":
            ["steven"],
        "jessica":
            ["steven"]}

        Args:
            new_mutuals: A dictionary of the format {"new-user-username" : [mutualflwr1, mutualflwr2]}
        Returns:
            void
        """
        #get the current mutual_followers dictionary from mutual_followers.json
        mutual_path = Path("mutual_followers.json")
        with mutual_path.open("r") as infile:
            old_mutual_flwrs = infile.read()
        
        #turn the json string into a dictionary
        parsed_old_mutual_flwrs = json.loads(old_mutual_flwrs)
        #update the dictionary
        parsed_old_mutual_flwrs.update(new_mutuals)

        #write it back into the file
        with mutual_path.open("w") as outfile:
            json.dump(parsed_old_mutual_flwrs, outfile)



###RUN EACH TIME YOU PULL FROM GITHUB###
def first_time_login_user():
    cl = Client()
    cl.login(USERNAME, PASSWORD)
    cl.dump_settings("session.json")
    return cl


if __name__ == '__main__':
    #a = CentralAccount()
    #a.login_user()
    #print(inspect.signature(a.central_account.user_id_from_username))
    #print(a.central_account.user_info_by_username(USERNAME))
    #print(a.central_account.user_followers("70684503354"))

    a = CentralAccount()
    #a.login_user()
    new_mutuals = {"test2": ["demo1","demo2"]}
    a.update_mutuals(new_mutuals)
    a.update_all_followers(new_mutuals)
    #print(inspect.signature(a.central_account.user_id_from_username))
    #print(a.central_account.user_info_by_username(USERNAME))
    #print(a.central_account.user_followers("13586646940"))

    print(a.get_mutuals(a.get_followers("steveyivicious")))
    
