# FH4-Mixer-Influence-Automation
This script will avoid influence farm channels (these channels are nerfed and do not give influence in-game) and automatically select channels that are currently streaming.


# Usage
 The first time a user uses the script they will be prompted to login, after logging in they should press enter in the python shell.
 This script will save the session cookies to a file and load them on startup. This prevents the user from having to login every time they start the script.

# Requirements
Please install the packages listed in requirements.txt </br>
Additionally, you'll need to have the ChromeDriver (https://chromedriver.chromium.org/downloads) accessible via PATH (system variable).


# Notes Regarding Linux
1. sudo apt-get install chromium-browser
2. Download v76 of the webdriver (https://chromedriver.storage.googleapis.com/index.html?path=76.0.3809.126/)
3. Add the directory containing the webdriver to the system $PATH variable
4. Add self.chrome_options.add_argument("--headless") and self.chrome_options.add_argument('--no-sandbox') to the init function
Note: You'll need to run the script with GUI at least once to generate the cookies.pkl file.
