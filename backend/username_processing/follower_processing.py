from instagrapi import Client
from instagrapi.exceptions import (
    BadPassword, ReloginAttemptExceeded, ChallengeRequired,
    SelectContactPointRecoveryForm, RecaptchaChallengeForm,
    FeedbackRequired, PleaseWaitFewMinutes, LoginRequired
)
import instagrapi as i
import logging
from pathlib import Path
import json


USERNAME = "irvinehacks2025_2"
PASSWORD = "7Ysteveni*"
"""
Remember: A connection between nodes is only made when people follow each other

You'll be receiving the username of the new person that entered their username
"""



def example_func_to_show_documentation_style(a, b):
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
        ###YOU ADDED THIS BECAUSE YOU DIDN'T WANT TO PERMANENTLY FUCK OVER YOUR ACCOUNTS
        def handle_exception(client, e):
            if isinstance(e, PleaseWaitFewMinutes):
                print("TESTING TESTING TESTING")
                # self.freeze(str(e), hours=1)
            raise e
        self.central_account.handle_exception = handle_exception
        print("hi!")
        print(self.central_account.handle_exception)
        #END BLOCK OF ADDING SHIT


    def login_user(self):
        """
        Attempts to login to Instagram using either the provided session information
        or the provided username and password.
        """
        logger = logging.getLogger()

        self.central_account = Client()
        #use this line to add a delay range
        self.central_account.delay_range = [1, 3]
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
        user_id = (self.central_account.user_info_by_username_v1(username)).pk
        #adding <amount=100> to the parameters will limit the number of followers we try to take
        followers = self.central_account.user_followers(user_id, amount=0)
        #build up the result
        result = {username: []}
        for short in followers.values():
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
        #read the old data
        all_flwrs_path = Path("all_followers.json")
        with all_flwrs_path.open("r") as infile:
            old_users_and_flwrs = infile.read() #returns a string

        #parse the old data
        if (old_users_and_flwrs == ""):
            parsed_old_users_and_flwrs = {}
        else:
            parsed_old_users_and_flwrs = json.loads(old_users_and_flwrs)

        #put the new data into the old
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
        new_user_mutuals = {new_user_username : []}

        #get the all_followers string
        with open("all_followers.json", 'r') as infile:
            contents = infile.read()
        #convert the string into a dictionary
        if (contents == ""):
            followers = {}
        else:
            followers = json.loads(contents)

        #for each user, and their followers, from all_followers
        for other_username, other_followers in followers.items():
            #if the new user is the other user
            if other_username == new_user_username:
                pass
            else:
                #get the mutual followers of the new user and the other user
                other_users_new_mutuals = []
                mutual_followers = frozenset(other_followers) & frozenset(new_user[new_user_username])
                #if the new user is in the other user's follower list, and the other user is in the new user's follower list
                if (new_user_username in other_followers) & (other_username in new_user[new_user_username]):
                    #update the new user's mutuals first
                    new_user_mutuals[new_user_username].append(other_username)
                    #then add the new user's username to the other user's slated mutuals
                    other_users_new_mutuals.append(new_user_username)
                    
                #if the new user and the other user have mutual followers
                if len(mutual_followers) != 0:
                    #update the new user's mutuals
                    new_user_mutuals[new_user_username] = list(frozenset().union(*[frozenset(new_user_mutuals[new_user_username]), mutual_followers]))
                    #update the other user's mutuals
                    other_users_new_mutuals += list(mutual_followers)
                
                #if the other user has new mutuals, update the other user's mutuals list on mutual_followers.json
                if len(other_users_new_mutuals) != 0:
                    #the long list(frozenset()) yada yada call is unnecessary for this, because that's checked in
                    #update_mutuals
                    self.update_mutuals(other_username, other_users_new_mutuals)

        return new_user_mutuals


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
        #if we have no record of the username's mutuals in mutual_followers.json
        if (username not in parsed_old_mutual_flwrs.keys()):
            parsed_old_mutual_flwrs[username] = new_mutuals
        #otherwise, the username is already in mutual_followers.json
        else:
            ##all this set math is done to prevent duplicate follower names in the follower's list
            #Add the new followers to the mutual followers list. Only new followers not
            #already present in mutual followers list will be added.
            parsed_old_mutual_flwrs[username] = list(frozenset().union(*[frozenset(parsed_old_mutual_flwrs[username]), (frozenset(new_mutuals))]))

        #write it back into the file
        with mutual_path.open("w") as outfile:
            json.dump(parsed_old_mutual_flwrs, outfile)
            outfile.flush()


    def overwrite_mutuals(self, new_mutuals: dict):
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
    """
    Assumes that, if a username is not in the keys of all_followers, then it is not in the keys of
    mutual_followers either
    """
    #get the current all_followers in order to check if we already scraped the account
    with Path("all_followers.json").open("r") as infile:
        all_accounts = infile.read()
    if all_accounts == "":
        parsed_all_accounts = {}
    else:
        parsed_all_accounts = json.loads(all_accounts)
    #check if we already scraped the account 
    # TODO: WE MIGHT WANT TO CHANGE THIS SO THAT WE CAN RE-SCRAPE ACCOUNTS
    if (username not in parsed_all_accounts.keys()):
            flwrs_dict = ctr_acc.get_followers(username)
    else:
        flwrs_dict = {username: parsed_all_accounts[username]}
    
    ctr_acc.update_all_followers(flwrs_dict)
    flwr_mutuals = ctr_acc.get_mutuals(flwrs_dict) #remember, this also updates the mutual follower lists of other accs
    #we overwrite the mutuals because people may gain new followers,
    #meaning they may have gained new follower mutuals since the last time they entered their username
    ctr_acc.overwrite_mutuals(flwr_mutuals)
    


###RUN EACH TIME YOU PULL FROM GITHUB TODO: MAY NOT BE NECESSARY. THIS MAY ALSO BE THE 
# ##ROOT CAUSE OF A LOT OF OUR PROBLEMS...BECAUSE WE ARE MAKING INSTAGRAM THINK WE'RE DOING
# BRAND NEW LOGINS FROM MULTIPLE DEVICES ALL AT THE SAME TIME### 
# TODO: FIGURE OUT IF THIS WILL WORK WHEN YOU PUBLISH THE PROJECT
def first_time_login_user():
    cl = Client()
    cl.login(USERNAME, PASSWORD)
    cl.dump_settings("session.json")
    return cl



if __name__ == '__main__':
    #THE OVERALL TEST
    # main_process_username("steveyilicious", startup())

    #THE FINAL, BIGGEST TEST
    # main_process_username("janepwp", startup())

    ###YOU ADDED THIS BECAUSE YOU WANTED TO TEST OUT THE EXCEPTION HANDLER, BUT IT DOESN'T WORK
    a = startup()
    a.central_account.handle_exception(a, PleaseWaitFewMinutes)
    #END BLOCK OF BULLSHIT


    #print(a.central_account.user_followers_v1(a.central_account.user_info_by_username_v1("filthy_franks_partner").pk))
    
    #main_process_username("filthy_franks_partner", a)

    # a = {"a" : ["b", "c"]}
    # a.update({"a" : ["b"]})
    # print(a)
    #a = startup()
    #b = {"jad_umb": ["natbagel", "frank.yeh808", "anshuxs", "therealaidanvara", "justin.siek", "maiiithy", "the_awesome_akam_khinda", "sushikirbz", "nguyenxjason", "pentium.girl", "thia.io", "neeraj_savd", "leen.ramesh", "mark.zshao", "dylandsd", "maria.wroblewska007", "daniel.in.motion", "stefany_ruan", "kim_ssangmin", "joseap.t", "aarushi_poo", "armanoid_creature", "g_ls07", "yum_my023", "hrishi.meh", "uci_oit", "novytsang", "koko_okrunch", "rizzyizzie_", "mister.shem", "sicazy", "uci_elp", "peter__ou", "notiwah", "hdola_ewy", "lucaschin_", "nick_vuong", "gabecpz_", "ayaka.nakamura_", "kswagger098", "ivvan._", "bon.nie.man", "kginac", "sicazhang", "leading2succeed_", "dqfuq", "eric.l30", "jasen5196", "anth.tm", "ji.wonh", "alixer_alex", "allegro.sostenuto", "furby.duck", "ssarah.yuan", "janicezhxng", "novy.tsang", "sara.uchida", "boomin.alex", "maximilian_fkonrad", "izel.sanchez", "asiantimo", "littlepeace2005", "yum_ni_023", "jamesu.park", "isabellayi111", "ranrannn_0307", "michael_ashfo", "te_evan", "jiwooplays2k", "akshira._", "coltjmcguire", "jenna._.peng", "kellyallexa", "efhta", "emilio_lim", "harrisxu_", "medhab3", "vajraaang", "vincent.liu1", "samsammy184", "howtobecomelakshgupta", "_katelynbellows", "crusadercrisp", "josephd13_", "elaineliu__", "sanjaysvelan", "mushmooshroom", "annishpattani04", "gabcel1ne", "babyyodz_z", "tofu_birdie", "matthewgraygublersbiggestfan", "em_mazuo", "samuel.wang12", "aishahid786", "lord_ingram", "davidwanggggggg", "realestthugsri", "kayeeeechen", "chloemmeyer", "adeeba.mohammed", "abhinavtiruveedhula", "halcyankeh", "poojadave22", "sai.my.guy", "sohajashwant", "justin_yang_148", "kristennnnnsss", "amrit.addanki", "henryliu8", "goofy_goomber", "soha_jashwant", "practice.with.wyatt", "jshinkart.aiart", "doubleaa02", "jiwoo.h.yung", "dsarthak_19", "shivaniarya_", "rishavs01", "joeyc_skt", "calamarho", "abhi.someswar", "brand_new.song", "ellla.li", "moreortess", "timtamotheus", "stevozeng", "elsa.joy", "jennyxun_", "5elina.he", "armaanchadha__", "highonjuice_", "harshith.sadhu", "rishikhott", "_lia_ah__", "rbeccalee", "guobropro", "trannguyen_225", "stirfryfood", "gautham.inq", "ianmbeamer", "kaushish.kebab", "ryanchennnnnn", "downisdown1", "choppsthicc", "koryoboi", "jjojoof", "joyce.liang0", "shwetananaaware", "danielxzhao", "crustalyang", "elleenie.kim", "ramenking333", "isabellliu", "luharok06", "_elisabeth.mathis_", "allisonn.kim", "a.kimchi_", "guava.ram", "greydanv", "qwertywiejxndb_742", "presidentsamlu", "numberlinksnumber1", "francis_li1", "ian_vo_7", "jakeshin9", "jongyunshin229", "bo.nguyxn", "russ_c4", "tiff.anyluong", "lqurq.l", "alexhshi", "abhiritdas", "hitstarana", "disar_ray_", "harshinisriniv", "theultrahdgamer", "_rohansrinivas_", "_kennethyao", "seter_pong", "sanjanaaap", "un.ecorn", "nicolexxuu", "maya.kookie97", "its.eugene", "mwathayu__k100", "matt22k_", "stegosaurus_in_highschool", "sahillalaniii", "rikiszstudio", "chanev_05", "ht_wuwu", "braandonalee", "diegojs2005", "13r4dy", "rachael.yna", "a.terry__", "gallardoalexis4", "jam_bakrin", "hongdou_taro", "marcus_goobie", "abhiritdas2", "wholesome_memes13", "duncantlynch", "superstorm202", "mixerstreamerscentral", "a.das_13", "thiccpapibreadloaf", "_________nayao", "prmdyaputra_77", "loneranger_808", "jack_g.j", "thespicyvariety", "shivaay22"]}
    #main_process_username("steveyilicious", a)
    #print(list(frozenset().union(*[frozenset(["a", "b"]), (frozenset(["c", "b"]))])))
    #b = {"bob" : ["sam", "steven"]}
    #a.update_all_followers(b)
    #a.overwrite_mutuals(a.get_mutuals(b))
    #main_process_username("steveyivicious", a)

    #new_mutuals = {"jessica": ["steven"]}
    #print(a.get_mutuals(new_mutuals))

    # with Path("C:\\Programming\\IrvineHacks2025\\irvinehacks2025\\backend\\username_processing\\empty.json").open("r") as infile:
    #     empty_str = infile.read()
    # a.overwrite_mutuals({"a" : ["b", "c"]})
    #print(a.central_account.user_followers(a.central_account.user_id)

