#Author: @Travis-Owens
#Date:   2019-9-25
#Description: Microsoft nerfed influence farms and this script will avoid those channel.

from selenium import webdriver
import requests
import json
import os.path
import pickle

class influence_farm_bot(object):
    def __init__(self):
        self.current_channel = {'token': 'null', 'userId': 'null'}
        self.blacklist = ['influence', 'farm', '24/7', 'hangout']

        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--mute-audio")


    def run(self):

        self.browser = webdriver.Chrome(chrome_options=self.chrome_options)       # Opens the browser window

        self.browser.get('https://mixer.com/')  # Load mixer.com

        # Checks if user has setup the cookies; load them, eles; create cookie file
        if(os.path.exists('cookies.pkl')):
            self.load_cookies()
        else:
            self.init_setup()

        self.get_fh4_stream()          # Sets current_channel values

        self.update_mixer_channel()    # Changes to the current channel

        while True:
            channel_online_status = self.check_stream_status()

            if(channel_online_status == True):
                pass
            else:
                self.get_fh4_stream()
                self.update_mixer_channel()

    def init_setup(self):
        # This function will wait for the user to login and then save the session cookies to a local file
        # Saving the cookie prevents the user from having to login everytime

        print('press <Enter> after you\'ve logged in')  # Wait for user to login
        login_prompt = input()                          # Block until user finishes login

        pickle.dump( self.browser.get_cookies() , open("cookies.pkl","wb"))

        return

    def load_cookies(self):
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            if 'expiry' in cookie:
                del cookie['expiry']
            self.browser.add_cookie(cookie)

    def update_mixer_channel(self):
        channel_url  = 'https://mixer.com/' + self.current_channel['token']
        self.browser.get(channel_url)
        return

    def get_fh4_stream(self):
        # This function will query the mixer API for FH4 streams, and return a channel name of one that is not a 'farm'

        # This route returns the top 50 streams for fh4
        api_request = 'https://mixer.com/api/v1/types/559325/channels?order=viewersCurrent:DESC&limit=50'

        r = requests.get(api_request)
        data = json.loads(r.content.decode('utf-8'))

        for channel in data:
            try:
                if not(bool([i for i in self.blacklist if(i in channel['name'].lower())])):
                    self.current_channel['token']   = channel['token']
                    self.current_channel['userId']  = channel['userId']
                    return
                else:
                    pass
            except UnicodeEncodeError as e:
                print(e)

        ## TODO: If the script reaches this point, it has not found any channels, need a solution to mitgate this
        return

    def check_stream_status(self):

        api_request = 'https://mixer.com/api/v1/channels/' + self.current_channel['token']

        r = requests.get(api_request)
        data = json.loads(r.content.decode('utf-8'))

        if(data['online'] == True):
            return True
        else:
            return False

influence_farm_bot().run()
