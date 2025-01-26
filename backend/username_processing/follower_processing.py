from instagrapi import Client
import instagrapi as i
from instagrapi.exceptions import LoginRequired
import logging
from pathlib import Path
import json


USERNAME = "irvinehacks2025_1"
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
        user_id = self.central_account.user_info_by_username_v1(username).pk
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
        if (old_users_and_flwrs == ""):
            parsed_old_users_and_flwrs = {}
        else:
            parsed_old_users_and_flwrs = json.loads(old_users_and_flwrs)

        #append the new data to the old
        parsed_old_users_and_flwrs.update(user_with_followers)

        #write it back to the file
        with all_flwrs_path.open("w") as outfile:
            json.dump(parsed_old_users_and_flwrs, outfile)
            outfile.flush()


    def get_mutuals(self, new_user: dict):
        """
        Gets the mutual followers of a user by checking the all_folowers.json file
        Assumes the new_user is not in the all_followers.json, because it doesn't check for duplicate
        followers in new_user

        From an optimized design perspective, you only need to check if the new person being added
        has any mutuals with any existing users within the all_followers.json file.

        For each user/key in all_followers.json, you only have to check if the new-user is in that
        person's follower list. DO NOT check the follower lists of each follower of each user in
        all_followers.

        Also updates the mutuals list of people in all_followers.json, in mutual_followers.json
        Basically, their mutuals list is in mutual_followers.json, and this automatically updates it

        Args:
            new_user: A dictionary of the format {"insert-user's-username-here" : [follower1, follower2]}
        Returns:
            A dictionary of the format {"user's-username-here" : [mutualfollower1, mutualfollower2]}
        """
        new_user_username = list(new_user.keys())[0]
        mutuals = {new_user_username : []}

        #get the all_followers string
        with open("all_followers.json", 'r') as infile:
            contents = infile.read()
        #convert the string into a dictionary
        if (contents == ""):
            followers = {}
        else:
            followers = json.loads(contents)

        #for each user from all_followers
        for other_username, follower_list in followers.items():
            other_users_new_mutuals = []
            both_following = frozenset(follower_list) & frozenset(new_user[new_user_username])
            #if the new_user is in the user's follower list, and the user is in the new_user's flwr list
            if (new_user_username in follower_list) & (other_username in new_user[new_user_username]):
                #knowing that this is the one and only time the person represented by username will
                #have to update their mutual follower list during this function...

                #so update the new user's mutuals first
                mutuals[new_user_username].append(other_username)

                #then add the new user's username to the other user's slated mutuals
                other_users_new_mutuals.append(new_user_username)
                
            #if the new_user follows a same person as the other user (the user from the json)
            if len(both_following) != 0: 
                mutuals[new_user_username] = list(frozenset().union(*[frozenset(mutuals[new_user_username]), both_following]))
                #long list frozenset() yada yada call not ncessary for other_users_new_mutuals, because that's checked in
                #update_mutuals
                other_users_new_mutuals += list(both_following)
            
            #update the other user's mutuals list on mutual_followers.json, if not empty
            if len(other_users_new_mutuals) != 0:
                self.update_mutuals(other_username, other_users_new_mutuals)

        return mutuals


    def update_mutuals(self, username: str, new_mutuals: list):
        """
        HELPER FUNCTION
        ASSUMES: username is already a key in all_followers.json
        
        Updates the mutual followers of a user in mutual_followers.json

        Args:
            username: A string representing the person's username
            new_mutuals: A list representing the new mutuals that are to be added to the
                        mutual follower's list of the username, all to be done in mutual_followers.json
        Returns:
            void
        """
        #get the current mutual_followers dictionary from mutual_followers.json
        mutual_path = Path("mutual_followers.json")
        with mutual_path.open("r") as infile:
            old_mutual_flwrs = infile.read()
        
        #turn the json string into a dictionary
        if (old_mutual_flwrs == ""):
            parsed_old_mutual_flwrs = {}
        else:
            parsed_old_mutual_flwrs = json.loads(old_mutual_flwrs)

        #update the mutuals list of the username
        #if the username is not in the parsed old mutual followers keys
        if (username not in parsed_old_mutual_flwrs.keys()):
            parsed_old_mutual_flwrs[username] = new_mutuals
        else:
            #all this set math is done to prevent duplicate follower names in the follower's list
            #Add the new followers to the mutual followers list. Only new followers not currently
            #present in mutual followers list already.
            parsed_old_mutual_flwrs[username] = list(frozenset().union(*[frozenset(parsed_old_mutual_flwrs[username]), (frozenset(new_mutuals))]))

        #write it back into the file
        with mutual_path.open("w") as outfile:
            json.dump(parsed_old_mutual_flwrs, outfile)
            outfile.flush()


    def add_mutuals(self, new_mutuals: dict):
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
        if (old_mutual_flwrs == ""):
            parsed_old_mutual_flwrs = {}
        else:
            parsed_old_mutual_flwrs = json.loads(old_mutual_flwrs)

        #update the dictionary
        parsed_old_mutual_flwrs.update(new_mutuals)

        #write it back into the file
        with mutual_path.open("w") as outfile:
            json.dump(parsed_old_mutual_flwrs, outfile)
            outfile.flush()


def startup():
    central_account = CentralAccount()
    central_account.login_user()
    return central_account


def main_process_username(username: str, ctr_acc: CentralAccount):
    flwrs_dict = ctr_acc.get_followers(username)
    ctr_acc.update_all_followers(flwrs_dict)
    flwr_mutuals = ctr_acc.get_mutuals(flwrs_dict) #remember, this also updates the mutual follower lists of other accs
    ctr_acc.add_mutuals(flwr_mutuals)


###RUN EACH TIME YOU PULL FROM GITHUB### TODO: FIGURE OUT IF THIS WILL WORK WHEN YOU PUBLISH THE PROJECT
def first_time_login_user():
    cl = Client()
    cl.login(USERNAME, PASSWORD)
    cl.dump_settings("session.json")
    return cl



if __name__ == '__main__':
    pass
    #a = startup()
    #print(list(frozenset().union(*[frozenset(["a", "b"]), (frozenset(["c", "b"]))])))
    #b = {"bob" : ["sam", "steven"]}
    #a.update_all_followers(b)
    #a.add_mutuals(a.get_mutuals(b))
    #main_process_username("steveyivicious", a)

    #new_mutuals = {"jessica": ["steven"]}
    #print(a.get_mutuals(new_mutuals))

    # with Path("C:\\Programming\\IrvineHacks2025\\irvinehacks2025\\backend\\username_processing\\empty.json").open("r") as infile:
    #     empty_str = infile.read()
    # a.add_mutuals({"a" : ["b", "c"]})
    #print(a.central_account.user_followers(a.central_account.user_id)

