# Bruteforce_Wordle_Bot
Python bot created with Selenium that finds the word of the day through process of elimintaiton. 
* 70% of the time the bot should find the word within the 6 attempts. 
* If it does not, a new browser session is launched to continue solving. 

</img>
<img src = "demo.gif", alt = "wordle", height = "350">

# Running and Installation
## Install and Setup
1. Clone or fork the repo.
2. pip install the requirements.txt file. (You may want to create a new virtual environment as well.)
```shell
python -m pip install -r requirements.txt
```
3. Create a `.env` file in the project folder.
    * The `.env` file is required to have the file path to your selenium chrome webdriver. See [here](https://chromedriver.chromium.org/getting-started) for more details on seleniums chrome webdrivers. 
```
CHROME_DRIVER="path/to/your/chromedriver.exe"
```
## Running the Module
* Running `--help` or `-h` will show the available arguments and default values. 
```shell
python -m wordle_bot -help
```
* To run the module with the chrome instance hidden simply run the below.
command:
```shell
python -m wordle_bot
```
* To run the module with the chrome instance visible run enter the `--display` or `-d` argument as True
```shell
python -m wordle_bot -d True
```
* To run the module and get results as an SMS pass `textbelt` or `twillo` to the `--sms` or `-s` argument. <i>Note: You will need to have a `textbelt` or `twillo` account and have the appropriate `.env` variables set. See below for the details.</i>
```shell
python -m wordle_bot -s textbelt
```
## <i>Optional `.env` file contents:</i>

* `send_twillo_sms_notification` Will send a text message to your default number.  
* Dependencies: 
    * Twillo function is deppendent on the .env file saved in root folder. 
    * You will need to set up a Twillo Account. See [Twillo SMS](https://www.twilio.com/docs/sms) for more information.
    * Contents of .env file below:
```
TWILIO_ACCOUNT_SID=Your_Twillo_Account_SID
TWILIO_AUTH_TOKEN=Your_Twillo_Auth_Token
TWILLO_FROM=Your_Tiwllo_From_Number
TO_NUMBER=Your_Twillo_To_Number
```
* `send_textbelt_sms_notification` Will send a text message to your number in the `.env` file.
* Dependencies: 
    * Textbelt function is deppendent on the .env file saved in root folder.
    * You will need to create a Textbelt account. See [Textbelt](https://textbelt.com/) for more details.
    * Contents of .env file below:
```
TO_NUMBER=Your_Mobile_Number
```

# Code Overview
Bruteforce Algorithm:
----------------------

Algorithm is handled in the WordHandler class. 
The process is as follow: 
1) The first two guess are optimized words for elimination, words sourced from [wired.com's article here.](https://www.wired.com/story/best-wordle-tips/#:~:text=If%20you%20start,with%20SENOR%2C%20DUCAT)
2) iterate through word list, for each word:
    * If the word does not contain a known value at the known index, remove it from the list.
    * If the word does not contian a present letter, remove it form the list.
    * If the word contains a absent letter, remove it form the list.
3) Use random.choice to select the new word form the filtered list. 
* Note: There is a lot of room for improvement here, such as not using random and calculating probability, but that was not the intent of this project. 

Web Driver
----------
The WordleWebDriver class handles all interactions with the site.
An instance of the WordHandler class is encapsulated here for ease of updating known letter indexes, present letters and absent letters. 
* display_page boolean toggles wether the chrome driver should run in the background or not.
* Web Driver handles all the interactions with the page, such as sending words and extracting data. 

Word Lists
----------
The word list is all 5 letter words downloaded from [The Stanford GraphBase: A Platform for Combinatorial Computing](https://www-cs-faculty.stanford.edu/~knuth/sgb.html). 
I thought it would be two easy to use the same words as Wordle.

References
---
* [www.wired.com](https://www.wired.com/story/best-wordle-tips/#:~:text=If%20you%20start,with%20SENOR%2C%20DUCAT)
* [The Stanford GraphBase: A Platform for Combinatorial Computing](https://www-cs-faculty.stanford.edu/~knuth/sgb.html). 

