import pandas as pd
import sys

from environ import Env
from datetime import datetime
from pandas.core.frame import DataFrame
from pandas.errors import ParserError
from pathlib import Path
from selenium.webdriver.common.by import By

from browser import Browser
from gs_reader import sheet_reader

BASE_DIR = Path(__file__).resolve().parent
env = Env()
env.read_env(BASE_DIR / 'credentials.env')

UC_SITE_USERNAME = env('UC_SITE_USERNAME')
UC_SITE_PASSWORD = env('UC_SITE_PASSWORD')
UC_SITE_URL = 'https://www.universal-credit.service.gov.uk/sign-in'
UC_SITE_JOURNAL_URL = 'https://www.universal-credit.service.gov.uk/work-search'

DATE_FORMAT = env('DATE_FORMAT')


def main():
    applications = read_data()
    browser = Browser()
    print('Starting the UC job application logger...')
    login(browser)
    browser.sleep(60)  # input the SMS code manually
    got_to_journal(browser)

    add_jobs(browser, applications)
    browser.sleep(20)
    browser.close()

    print('All done.')


def read_data():
    try:
        if 'USE_GOOGLE_SHEETS' in env:
            if env('USE_GOOGLE_SHEETS') == 'True':
                data = sheet_reader()
        else:
            data = pd.read_csv('data.csv')
    except ParserError as pe:
        print(pe)
        sys.exit('The file appears to have a formatting issue')

    except FileNotFoundError:
        sys.exit('Could not find the file')

    except Exception as e:
        print(e)
        sys.exit('Something went wrong')

    return data


def login(browser: Browser):
    print('Logging into UC Website...')
    try:
        browser.open_page(UC_SITE_URL)
        browser.add_input(by=By.ID, id='id-userName', value=UC_SITE_USERNAME)
        browser.add_input(by=By.ID, id='id-password', value=UC_SITE_PASSWORD)
        browser.click_button(by=By.ID, id='id-submit-button')

        browser.sleep(10)

        submit_key = input(
            "Please input code from sms: ",
        ).strip()
        browser.add_input(by=By.ID, id='id-verificationToken', value=submit_key)
        browser.click_button(by=By.ID, id='id-submit-button')

    except Exception as e:
        print(e)
        sys.exit('Something went wrong')

    else:
        print('Login successful. Will continue in a minute...')


def got_to_journal(browser: Browser):
    browser.open_page(UC_SITE_JOURNAL_URL)


def add_jobs(browser: Browser, data: DataFrame):
    for index, row in data.iterrows():

        print(f'Processing record: {row.iloc[0]} - {row.iloc[1]}')

        browser.click_button(by=By.ID, id='add-job')

        browser.add_input(by=By.ID, id='id-jobTitle', value=row.iloc[0])
        browser.add_input(by=By.ID, id='id-employer', value=row.iloc[1])

        if row.iloc[2] == 'Applied':
            browser.click_button(by=By.ID, id='clickable-APPLIED')

            try:
                application_date = datetime.strptime(row.iloc[3], DATE_FORMAT)
            except ValueError:
                sys.exit('Wrong date format. The program will exit')

            browser.add_input(by=By.ID, id='id-applicationDate.day', value=str(application_date.day))
            browser.add_input(by=By.ID, id='id-applicationDate.month', value=str(application_date.month))
            browser.add_input(by=By.ID, id='id-applicationDate.year', value=str(application_date.year))

        elif row.iloc[2] == 'Unsuccessful':
            browser.click_button(by=By.ID, id='clickable-UNSUCCESSFUL')
        else:
            sys.exit('Wrong data. The program will exit')

        notes = row.iloc[7]
        if type(row.iloc[9]) is str:
            if len(row.iloc[9]) > 0:
                notes = notes + '\n' + row.iloc[9]
        browser.add_input(by=By.ID, id='id-notes', value=notes)

        browser.click_button(by=By.ID, id='id-submit-button')
        browser.sleep(3)


if __name__ == "__main__":
    main()
