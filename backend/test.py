
from instagrapi import Client
import inspect


cl = Client()
cl.login("filthy_franks_partner", "1028571DV")

followers = cl.user_followers(cl.user_id, amount=1)
print(followers)
