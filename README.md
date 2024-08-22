# Universal Credit job application journal logger

If you live in the UK and happen to be receving Universal Credit (UC) while looking for work, you will need to log your job search activities into the UC website. If you are applying for a lot of jobs, this can be a very tedious, manual process. And the UC website is not particularly user friendly (they should hire a UI/UX specialist). This script will help you automate the process of logging the jobs that you have applied for into the UC website.

## Demo

<p align = "center">
<img height= "400" src ="https://raw.githubusercontent.com/VikSil/UC_journal_automation/trunk/assets/GIF_demo.gif" alt="Universal Credit Website Journal Automation Demo GIF"/>&nbsp;&nbsp;
</p>

## Prerequisites

The following assumptions are made about the user of this script:

* You are running this script on a Windows machine (might work on Mac and Linux as well, but has not been tested). 
* You have Chrome web browser installed on your machine.
* You have Python, pip and git installed on your machine.

## Setup and configuration

Clone this repo to your machine:

    
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

## Data source
 
There is an option to either use a .csv file or source the data from a Google Sheets spreadsheet.
Whichever option you choose, add a configuration into `credentials.env` file for the date format that is used in the data source, e.g.:

    DATE_FORMAT=%Y-%m-%d

Make sure that APPLICATION DATE column format in your data source uses the same format.

### Local datasource

Add into the root folder a `data.csv` file with the entries of job applications, that you want to submit to the UC website. The file should have the same format as `data_example.csv` file in this repo. When using local datasource:

* The names of the columns does not matter, but the sequence does.
* STATUS column must only contain values `Applied` or `Unsuccessful`.
* The file must contain only the new applications that you want to add into the UC journal (all lines will be processed). 

### Google Sheets datasource

Applications must be listed in Google Sheets spreadsheet in the following format:
![Google Sheet example](assets/gs_example.png)

Click on the "Share" button on upper right corner of the spreadsheet to be taken to this options page. 

![Google Sheet sharebox](assets/share_gs.png) 

Here, access must be configured to `Anyone with the link`.

Add configuration into `credentials.env` file to switch on this functionality and point the script to the Google Sheet to use.

    USE_GOOGLE_SHEETS=True
    GS_SHEET_ID=l0nG-AnD-S00ph1stiCAT3d-URL-T0_Th3-Work5h33t

The value for GS_SHEET_ID can be obtained either from the URL bar of the browser, or by clicking on the `Copy link` button in the screenshot above. The URL will look something like this:

    https://docs.google.com/spreadsheets/d/GS_SHEET_ID/edit?usp=sharing

When using Google Sheets as the data source:
 * STATUS and APPLICATION DATE columns have to be named exactly that.
 * STATUS column can contain different values, but only rows with values `Applied` or `Unsuccessful` will be processed.
 * If there are multiple tabs on the Google Sheet, the data must be in the first tab.
 * It is possible to configure the earliest application date to process.

 In order to configure the earliest application date, add configuration to  `data_example.csv` file, e.g.:

    START_DATE=2024-08-14

With `START_DATE` configured, the script will ignore all earlier application dates in the Google spreadheet. The format of `START_DATE` must match that of the `DATE_FORMAT` variable. `START_DATE` will only have effect if `USE_GOOGLE_SHEETS=True` is configured.  Configuring `START_DATE` will superceed comadline `--threshold-date` argument (see below).

## Execution

Before running this script, have your phone ready to receive an sms with the 2-factor authorisation code.

To start the script run the following command from the root folder:

    python main.py


If use of Google Sheets is configured and `START_DATE` variable is **not** configured, optional comandline argument can be passed to signal to the script the earliest application date to process. Either of these are permissable:

    python main.py -d 2024-08-14
    python main.py --threshold-date 2024-08-14

This will cause a Chrome web browser to pop up. UC website will open, your credentials will be entered and login button will be pressed automatically. At this point you should receive an sms on your phone with a  2-factor authorisation code. You have 60 seconds to enter it into the UC website and click the button to continue.

🔴❗ This is the only manual step. Wait for the script to resume work. ❗🔴

In 60 seconds after logging in the script will navigate to the journal page and start submitting data from the the data source into the UC website. Once the end of the data is reached, the script will wait for 20 seconds and then close the website.

## Disclaimer
The script is operational as of the date of the last commit to GitHub. There are no guarantees of maintanence.