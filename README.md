# Universal Credit job application journal logger

If you live in the UK and happen to be receving Universal Credit (UC) while looking for work, you will need to log your job search activities into the UC website. If you are applying for a lot of jobs, this can be a very tedious, manual process. And the UC website is not particularly user friendly (they should hire a UI/UX specialist). This script will help you automate the process of logging the jobs that you have applied for into the UC website.

## Demo

<p align = "center">
<img height= "400" src ="https://raw.githubusercontent.com/VikSil/UC_journal_automation/trunk/GIF_demo.gif" alt="Universal Credit Website Journal Automation Demo GIF"/>&nbsp;&nbsp;
</p>

## Prerequisites

The following assumptions are made about the user of this script:

* You are running this script on a Windows machine (might work on Mac and Linux as well, but has not been tested). 
* You have Chrome web browser installed on your machine.
* You have Python, pip and git installed on your machine.

## Setup and installation

First things, first - git clone this repo to your machine:

    
    git clone https://github.com/VikSil/UC_journal_automation.git

In order to run this script you will need to find out which version of Chrome browser do you use and get a driver for it. [Here](https://www.youtube.com/watch?v=Yh4CnDL44O8) is a video tutorial on how to get the driver (watch up to 2:00). Alternatively  you may follow these steps:

1. In your Chrome browser go to this url: `chrome://settings/help` and note down the version
1. Go to [this](https://chromedriver.chromium.org/downloads) page and find the ChromeDriver for your Chrome version. If the version is new, you may have to read the text in red at the top of the page and go to **Chrome for Testing availability dashboard** to find the appropriate driver. N.B. The dashboard is frequently unavailable, if it does not work - check back later.
1. Download the appropriate driver for your Chrome version, operating system (Windows) and processor.
1. Unzip the `chromedriver.exe` file into the root folder of your project (where the main.py file is). 

Run the following command to install dependencies (this will take several minutes to complete):

    pip install -r requirements.txt

Add `credentials.env` file into the root directory with the following content:

    UC_SITE_USERNAME=YourLoginNameForUCWebsite
    UC_SITE_PASSWORD=YourPasswordForUCWebsite

Make sure that there are no spaces on either line in the `credentials.env` file

Add into the root folder a `data.csv` file with the entries of job applications, that you want to submit to the UC website. The file should have the same format as `data_example.csv` file in this repo. 

🔴❗ IMPORTANT  🔴❗
* The names of the columns does not matter, but the sequence does.
* Make dure that APPLICATION DATE format is '%d/%m/%Y' or change DATE_FORMAT global variable in `main.py` file.
* STATUS column must contain `Applied` or `Unsuccessful`.
* Data from URL and NOTES columns will be submitted into the **Notes** field on the UC journal form.


## Execution

Before running this script, have your phone ready to receive an sms with the 2-factor authorisation code.

To start the script run the following command from the root folder:

    python main.py

This will cause a Chrome web browser to pop up. UC website will open, your credentials will be entered and login button will be pressed automatically. At this point you should receive an sms on your phone with a  2-factor authorisation code. You have 60 seconds to enter it into the UC website and click the button to continue.

🔴❗ This is the only manual step. Wait for the script to resume work. 🔴❗

In 60 seconds after logging in the script will navigate to the journal page and start submitting data from the `data.csv` file into the UC website. Once the end of the `data.csv` file is reached, the script will wait for 60 seconds and then close the website.

## Disclaimer
The script is operational as of the date of submission to GitHub. There are no guarantees of maintanence.