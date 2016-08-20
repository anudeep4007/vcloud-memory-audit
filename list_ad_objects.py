import active_directory
from pyad import pyad
from vCloudLogger import vCloud_Logger

class list_ad_objects(object):



        #connection ad
        pyad.set_defaults(ldap_server="ad_server", username="username",password="password")

        def __init__(self):

            self.username = None

        def user_object(self, username):

            user = active_directory.find_user(username)

            #a little circus to convert to get computer name
            user = str(user)
            #match everything until first comma will return LDAP://CN=VM-OEVCDW8X86
            user = (user[0:user.find(',')])
            #cut everything from start to first 10 characters
            user = user[10:]
            user = user.rstrip()
            #append all the computer name to a list
            return user