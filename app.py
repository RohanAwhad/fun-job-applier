import functools
import os
import time

from playwright.sync_api import Playwright, sync_playwright
from loguru import logger

ASURITE_PWD = os.environ['ASURITE_PWD']
GIVEN_DATE = os.environ['DATE']  #'07-Sep-2023'
SLEEP_TIME = 2
APPLIED_JOBS = './applied_job_id_list.txt'
with open(APPLIED_JOBS, 'r') as f: ALREADY_APPLIED_JOB_IDS = [x.strip() for x in f.read().split('\n') if x]

def search_joblist(page, job_id_to_title_dict):
  time.sleep(SLEEP_TIME)
  jobs = page.locator('.jobList').locator('li')
  for x in jobs.all():
    inner_text = [y for y in x.inner_text().split('\n') if y]
    if len(inner_text) == 7:
      date, position_title, job_id = inner_text[1], inner_text[2], inner_text[4]
      if date == GIVEN_DATE: job_id_to_title_dict[job_id] = position_title

def apply_to_job(page, job_id, job_title, already_applied_set):
  print(f'job id: {job_id}')
  if job_id in already_applied_set:
    print('  - skipping. already applied')
    return -1
  print('  - searching')
  jobs = page.locator('.jobList').locator('li')
  for x in jobs.all():
    inner_text = [y for y in x.inner_text().split('\n') if y]
    if (len(inner_text) == 7) and inner_text[4] == job_id:
      print('  - applying')
      try:
        x.get_by_role('link', name=job_title).nth(0).click()
        autofill()
        print('  - successful')
        with open(APPLIED_JOBS, 'a') as f: f.write(job_id+'\n')
        time.sleep(SLEEP_TIME)
        return 0
      except Exception as e:
        logger.error(str(e), exc_info=True)
        return 2

  return 1

def autofill():
    # =========================================================
    # Recorded using codegen
    page.get_by_role("button", name="Apply to job").click()
    page.get_by_role("button", name="Let's get started").click()
    page.get_by_role("button", name="Save and continue").click()
    page.get_by_role("group", name="Are you currently eligible to work in the United States without ASU sponsorship?").get_by_label("Yes").check()
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


# === Main ===
with sync_playwright() as playwright:
  browser = playwright.chromium.launch(headless=False)
  context = browser.new_context()
  try:

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

    applied_this_session = set()
    job_id_to_title_dict = dict()
    while True:
      search_joblist(page, job_id_to_title_dict)
      for job_id, job_title in job_id_to_title_dict.items():
        res = apply_to_job(page, job_id, job_title, applied_this_session.union(ALREADY_APPLIED_JOB_IDS))
        if res == -1: applied_this_session.add(job_id)
        elif res == 1: print('  - was unable to apply to this job for unknown reasons')
        elif res == 2: print('  - was unable to apply to this job. cause should be printed above')
        elif res == 0:
          applied_this_session.add(job_id)
          break

      if len(applied_this_session) == len(job_id_to_title_dict): break
      else: logger.debug(f'len of dict: {len(job_id_to_title_dict)}  |  len of applied set: {len(applied_this_session)}')

  except Exception as e:
    logger.error(f'Error: {e}', exc_info=True)

  finally:
    context.close()
    browser.close()
