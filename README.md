
# FH4-Mixer-Influence-Automation
This script will avoid influence farm channels (these channels are nerfed and do not give influence in-game) and automatically select channels that are currently streaming.


# Usage
 The first time a user uses the script they will be prompted to login, after logging in they should press enter in the python shell.
 This script will save the session cookies to a file and load them on startup. This prevents the user from having to login every time they start the script.
 
**Normal operation** 
`python3 main.py`
**Headless**
 `python3 main.py -h`


 

# Requirements
Please install the packages listed in requirements.txt </br>
Additionally, you'll need to have the ChromeDriver (https://chromedriver.chromium.org/downloads) accessible via PATH (system variable).


# Notes Regarding Linux (Debian)
**You'll need to run the script with GUI and log in at least once to generate the cookies.pkl file.**
1. copy the cookies.pkl file to your current directory
2. `sudo apt update`
3. `sudo apt upgrade`
4. `sudo apt-get install chromium-browser`
5. Download v76 of the [webdriver](https://chromedriver.storage.googleapis.com/index.html?path=76.0.3809.126/)
6. `unzip chromedriver_linux64.zip`
7. `sudo pwd` and copy the output
8. Add the directory containing the webdriver to the system $PATH variable: `export PATH=$PATH:[step 7 ouput]`
9. `python3 main.py -h`

