import functools
import os
import time

from playwright.sync_api import Playwright, sync_playwright

ASURITE_PWD = os.environ['ASURITE_PWD']
SLEEP_TIME = int(os.environ['SLEEP_TIME'])

def old_click(page, s):
    page.click(s)
    page.wait_for_load_state('load')

def autofill():
    '''
    click('text="Apply to job"')
    click('text="Let\'s get started"')
    time.sleep(SLEEP_TIME)
    click('button[id="shownext"]')
    time.sleep(SLEEP_TIME)

    page.click('input[id="radio-44674-No"][type="radio"][value="No"]')
    page.click('input[id="radio-61829-No"][type="radio"][value="No"]')
    page.click('span[id="custom_44925_1291_fname_slt_0_44925-button_text"]')
    page.click('li[role="option"][aria-label="Searching ASU Website"]')
    click('button[id="shownext"]')

    page.click('a[id="AddResumeLink"]')
    popup = page.wait_for_popup()
    print(popup)
    pass
    '''
    
    # =========================================================
    # Recorded using codegen
    page.get_by_role("button", name="Apply to job").click()
    page.get_by_role("button", name="Let's get started").click()
    page.get_by_role("button", name="Save and continue").click()
    page.get_by_role("group", name="Are you currently eligible to work in the United States without ASU sponsorship?").get_by_label("No").check()
    page.get_by_role("group", name="Are you eligible for Federal Work Study?").get_by_label("No").check()
    page.get_by_role("listbox", name="How did you find out about this job? Choose...").locator("span").first.click()
    page.get_by_role("option", name="Searching ASU Website").get_by_text("Searching ASU Website").click()
    page.get_by_role("button", name="Save and continue").click()
    page.get_by_role("link", name="requiredRésumé/CV Add résumé/CV").click()
    page.frame_locator("iframe[title=\"Add résumé\\/CV\"]").get_by_role("button", name="Upload a file from Saved résumés/CVs").click()
    page.frame_locator("iframe[title=\"Add résumé\\/CV\"]").get_by_label("Resume-3.pdf").check()
    page.frame_locator("iframe[title=\"Add résumé\\/CV\"]").get_by_role("button", name="Add file").click()
    page.get_by_role("link", name="requiredCover Letter Add cover letter").click()
    page.frame_locator("iframe[title=\"Add Cover Letter\"]").get_by_role("button", name="Upload a file from Saved cover letters").click()
    page.frame_locator("iframe[title=\"Add Cover Letter\"]").get_by_label("Cover_Letter-4.pdf").check()
    page.frame_locator("iframe[title=\"Add Cover Letter\"]").get_by_role("button", name="Add file").click()
    page.get_by_role("button", name="Save and continue").click()
    time.sleep(SLEEP_TIME)
    page.get_by_role("button", name="Save and continue").click()
    time.sleep(SLEEP_TIME)
    page.get_by_role("button", name="Save and continue").click()
    time.sleep(SLEEP_TIME)
    page.get_by_role("button", name="Save and continue").click()
    time.sleep(SLEEP_TIME)
    page.get_by_role("button", name="Save and continue").click()
    time.sleep(SLEEP_TIME)
    page.get_by_role("button", name="Send my application").click()
    time.sleep(SLEEP_TIME)
    page.get_by_role("link", name="Job search").click()
    page.get_by_role("button", name="Search").click()

    # =========================================================

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    try:
        context = browser.new_context()

        # login
        page = context.new_page()
        page.goto('https://weblogin.asu.edu/cas/login?service=https%3A%2F%2Fweblogin.asu.edu%2Fcgi-bin%2Fcas-login%3Fcallapp%3Dhttps%253A%252F%252Fwebapp4.asu.edu%252Fmyasu%252F%253Finit%253Dfalse')

        page.fill('input[name=username]', 'rawhad')
        page.fill('input[name=password]', ASURITE_PWD)
        page.click('input[type=submit]')
        page.wait_for_load_state('load')
        
        page.get_by_role("link", name="Campus Services").click()
        page.get_by_role("link", name="Student Employment - Job Search").click()
        page.get_by_role("button", name="Search On-Campus Jobs").click()
        page.get_by_role("button", name="Search").click()

        while True:
            should_i_autofill = input('Autofill or Exit? (a/e) : ')

            if should_i_autofill == 'a': autofill()
            elif should_i_autofill == 'e': break


    except Exception as e:
        print(e)

    finally:
        context.close()
        browser.close()
