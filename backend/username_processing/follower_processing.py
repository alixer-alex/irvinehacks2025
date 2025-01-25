from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import logging


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
    central_account = Client()

    def login_user():
        """
        Attempts to login to Instagram using either the provided session information
        or the provided username and password.
        """
        logger = logging.getLogger()

        central_account = Client()
        session = central_account.load_settings("session.json")

        login_via_session = False
        login_via_pw = False

        if session:
            try:
                central_account.set_settings(session)
                central_account.login(USERNAME, PASSWORD)

                # check if session is valid
                try:
                    central_account.get_timeline_feed()
                except LoginRequired:
                    logger.info("Session is invalid, need to login via username and password")

                    old_session = central_account.get_settings()

                    # use the same device uuids across logins
                    central_account.set_settings({})
                    central_account.set_uuids(old_session["uuids"])

                    central_account.login(USERNAME, PASSWORD)
                login_via_session = True
            except Exception as e:
                logger.info("Couldn't login user using session information: %s" % e)

        if not login_via_session:
            try:
                logger.info("Attempting to login via username and password. username: %s" % USERNAME)
                if central_account.login(USERNAME, PASSWORD):
                    login_via_pw = True
            except Exception as e:
                logger.info("Couldn't login user using username and password: %s" % e)

        if not login_via_pw and not login_via_session:
            raise Exception("Couldn't login user with either password or session")
        

    def get_followers(username):
        """
        Args:
            username: a string that represents the username from which to get the followers
        Returns:
            A dictionary that is of the format: {username_from_arg : [follower1name, follower2name]}
        """
        pass

    def write_followers():
        pass



    

if __name__ == '__main__':
    login_user()
    

