# Universal Credit job application journal logger (Docker server based application)

If you live in the UK and happen to be receving Universal Credit (UC) while looking for work, you will need to log your job search activities into the UC website. If you are applying for a lot of jobs, this can be a very tedious, manual process. And the UC website is not particularly user friendly (they should hire a UI/UX specialist). This script will help you automate the process of logging the jobs that you have applied for into the UC website.

## Prerequisites
 Docker installed on your operating system to run the docker file [see](https://docs.docker.com/engine/install/).

## Setup and installation

### Google sheets automation

First things, first - git clone this repo to your machine:

    git clone https://github.com/VikSil/UC_journal_automation.git

Previously this automation script was deployed on a windows local machine and required a manual chromdriver install. However, with this update and the use of the [webdriver_manager](https://github.com/SergeyPirogov/webdriver_manager) package this is no longer required and is also automated.

All the user needs to do now is build dockerfile iamge by running the following command from within side the UC_journal_automation directory.

    docker build -t uc .    


Add `credentials.env` file into the root directory with the following content:

    UC_SITE_USERNAME=YourLoginNameForUCWebsite
    UC_SITE_PASSWORD=YourPasswordForUCWebsite

Make sure that there are no spaces on either line in the `credentials.env` file

Add into the roUC_journal_automation directory a `data.csv` file with the entries of job applications, that you want to submit to the UC website. The file should have the same format as `data_example.csv` file in this repo. 

🔴❗ IMPORTANT  🔴❗
* The names of the columns does not matter, but the sequence does.
* Make dure that APPLICATION DATE format is '%Y-%m-%d' or change DATE_FORMAT global variable in `main.py` file.
* STATUS column must contain `Applied` or `Unsuccessful`.
* Data from URL and NOTES columns will be submitted into the **Notes** field on the UC journal form.


## Execution

Before running this script, have your phone ready to receive an sms with the 2-factor authorisation code.

To start the docker run the following command from the within UC_journal_automation directory:

    docker run -it uc 3/3/2024

Because this is a docker contianer implementation for server no gui will pop and will be automated all required of the user is their sms submission-key input to the cli. 

🔴❗ This is the only manual step. Wait for the script to resume work. 🔴❗

In 60 seconds after logging in the script will navigate to the journal page and start submitting data from the `data.csv` file into the UC website. Once the end of the `data.csv` file is reached, the script will wait for 60 seconds and then close the website.

## Disclaimer
The script is operational as of the date of submission to GitHub. There are no guarantees of maintanence.