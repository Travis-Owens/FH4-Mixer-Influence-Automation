#Author: @Travis-Owens
#Co-Author: @Mathisco-01
#Date:   2019-9-25
#Description: Microsoft nerfed influence farms and this script will avoid those channel.

from selenium import webdriver
import requests
import json
import sys
import os.path
import pickle
import time
import logging


class influence_farm_bot(object):
    def __init__(self):
        logging.basicConfig(filename='FH4-Mixer-Influence-Automation.log', format='%(asctime)s - %(message)s', level=logging.INFO)
        self.logger = logging.getLogger()


        self.logger.info('Startup')
        self.current_channel = {'token': 'null', 'userId': 'null'}
        self.blacklist = ['influence', 'farm', '24/7', 'hangout']

        self.arguments = []
        for i in range(1, len(sys.argv)):
            self.arguments.append(sys.argv[i])

        self.chrome_options = webdriver.ChromeOptions()

        #mute audio 
        #-nm stands for no mute because mute is default
        if("-nm" not in self.arguments): 
            self.chrome_options.add_argument("--mute-audio")

        #headless mode
        if("-h" in self.arguments):
            self.chrome_options.add_argument("--headless")
            self.chrome_options.add_argument("--no-sandbox")

        #print mode
        if("-p" in self.arguments):
            print("Current arguments: ")
            for arg in self.chrome_options.arguments:
                print(" " + arg)

            print("Current keyword blacklist: ")
            for word in self.blacklist:
                print(" " + word)

        self.logger.info("sys args: {}".format(self.arguments))
        self.logger.info("chromedriver args: {}".format(self.chrome_options.arguments))

    def run(self):

        self.browser = webdriver.Chrome(options=self.chrome_options)       # Opens the browser window

        self.browser.get('https://mixer.com/')  # Load mixer.com

        # Checks if user has setup the cookies; load them, eles; create cookie file
        if(os.path.exists('cookies.pkl')):
            print("cookies.pkl found!")
            self.logger.info("cookies.pkl found!")
            self.load_cookies()
        else:
            print("cookies.pkl not found! Please follow instructions in the readme!")
            self.logger.critical("cookies.pkl not found! Please follow instructions in the readme!")
            self.init_setup()

        self.get_fh4_stream()          # Sets current_channel values

        self.update_mixer_channel()    # Changes to the current channel

        while True:

            # This will automatically tune to the offical forza stream
            offical_forza_status  = self.check_stream_status("Forza")
            if(offical_forza_status):
                if(self.current_channel['token'] != "Forza"):
                    self.current_channel['token'] = "Forza"
                    self.update_mixer_channel()

            channel_online_status = self.check_stream_status(self.current_channel['token'])

            if(channel_online_status == True):
                pass
            else:
                self.get_fh4_stream()
                self.update_mixer_channel()

            time.sleep(60)

    def init_setup(self):
        # This function will wait for the user to login and then save the session cookies to a local file
        # Saving the cookie prevents the user from having to login everytime

        print('press <Enter> after you\'ve logged in')  # Wait for user to login
        login_prompt = input()                          # Block until user finishes login

        pickle.dump( self.browser.get_cookies() , open("cookies.pkl","wb"))
        self.logger.info("dumped cookies.pkl")

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
        print("{} | Now watching: {}".format(time.strftime('%H:%M:%S'), self.current_channel['token']))
        self.logger.info("watching: {}  {}".format(self.current_channel['token'], channel_url))
        return

    def get_fh4_stream(self):
        # This function will query the mixer API for FH4 streams, and return a channel name of one that is not a 'farm'

        # This route returns the top 50 streams for fh4
        api_request = 'https://mixer.com/api/v1/types/559325/channels?order=viewersCurrent:DESC&limit=50'

        r = requests.get(api_request)
        data = json.loads(r.content.decode('utf-8'))

        for channel in data:
            try:
                if not(bool([i for i in self.blacklist if(i in channel['name'].lower())])) and self.check_stream_status(channel['token']) == True:
                    self.current_channel['token']   = channel['token']
                    self.current_channel['userId']  = channel['userId']
                    return
                else:
                    pass
            except UnicodeEncodeError as e:
                print(e)
                self.logger.warning(e)

        ## TODO: If the script reaches this point, it has not found any channels, need a solution to mitgate this
        print("No online or valid channels!")
        self.logger.critical("no online or valid channels found!")
        return

    def check_stream_status(self, token):
        try:
            api_request = 'https://mixer.com/api/v1/channels/' + token

            r = requests.get(api_request)
            data = json.loads(r.content.decode('utf-8'))

            if(data['online'] == True):
                return True
            else:
                return False
        except Exception as e:
            print(e)
            self.logger.warning(e)
            return False 

try:
    influence_farm_bot().run()
except Exception as e:
    print(e)
    self.logger.critical(e)
    self.logger.critical("STOPPING!")
    exit()