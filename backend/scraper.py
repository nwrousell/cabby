from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import codecs
import re
from webdriver_manager.chrome import ChromeDriverManager
import time 
import json
import re
# from selenium.webdriver.chrome.options import Options

# chrome_options = Options()
# chrome_options.add_argument("--user-data-dir=Scraper")

## OPTIONS
department_value = "CSCI"
# TODO - input a valid brown username/password below
username = "nrousell" 
password = "Turkeydove84*"
blacklist_course_codes = ["CSCI 2450", "ECON 2450", "ECON 2950", "ECON 2930", "ECON 2960", "ECON 2970"]
driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 60) # max 15 second timeout

## Open cab.brown.edu
def scrape_all_courses(include_critical_review=False):
    url = "https://cab.brown.edu/"

    print("Done waiting")
    driver.get(url)
    get_url = driver.current_url
    print("got URL:", get_url)
    wait.until(EC.url_to_be(url)) # ! THIS LINE
    if get_url == url:
        page_source = driver.page_source

    print("URL is Correct: ", get_url)
    soup = BeautifulSoup(page_source, features="html.parser")
    print("title: ", soup.title.text)

    ## Select "Computer Science" under "Advanced Search"
    # dropdown = driver.find_element(By.ID, 'crit-dept')
    # select = Select(dropdown)
    # select.select_by_value(department_value)

    ## Select "Any Term (2023-2024)" in the first dropdown
    dropdown = driver.find_element(By.ID, 'crit-srcdb')
    select = Select(dropdown)
    select.select_by_value("999999") # '999999' is the option value for 'Any Term (2023-2024)'

    ## Click "Find Courses"
    button = driver.find_element(By.ID, 'search-button')
    button.click()
    print("clicked find courses")

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "result")))

    # For each course
    # results = driver.find_elements(By.CSS_SELECTOR, '.result--group-start a.result__link:nth-of-type(1)')
    results = driver.find_elements(By.CSS_SELECTOR, '.result--group-start .result__link')
    print(len(results), "Courses")
    COURSES = []
    first = True
    for result in results:
        try:
            time.sleep(2)
            result.click()
            course_data = scrape_course(include_critical_review, first=first)
            COURSES.append(course_data)
            first = False
        except:
            print("Failed to parse a course...")
    return COURSES


def scrape_course(include_critical_review=False, first=False):
    course_data = {}
    #  Click on course
    time.sleep(2)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "dtl-course-code")))

    non_clickable_section = driver.find_elements(By.CLASS_NAME, "dtl-section")
    if len(non_clickable_section) == 0:
        #  Click S01
        section_01 = driver.find_element(By.CSS_SELECTOR, "a.course-section.course-section--matched")
        section_01.click()
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "dtl-section")))
    
    # Grab course code
    course_data["code"] = driver.find_element(By.CLASS_NAME, "dtl-course-code").text

    if course_data["code"] in blacklist_course_codes:
        raise Exception("course in blacklist")
    if course_data["code"] in ["APMA 2990", "ECON 2990", "MATH 2970"]:
        raise Exception("course is 'Examination'")

    # Grab term
    course_data["term"] = driver.find_element(By.CLASS_NAME, "detail-srcdb").text
    
    # Grab title
    course_data["title"] = driver.find_element(By.CLASS_NAME, "detail-title").text

    # Grab description
    course_data["description"] = driver.find_element(By.CSS_SELECTOR, ".section--description .section__content").text

    # Grab instructor
    course_data["instructor"] = driver.find_element(By.CSS_SELECTOR, ".section--instructordetail_html").text

    # grab time & location
    try:
        course_data["schedule"] = driver.find_element(By.CSS_SELECTOR, ".section--meeting_html").text
    except:
        pass

    try:
        course_data["programs"] = driver.find_element(By.CSS_SELECTOR, ".section--attr_html").text
    except:
        pass

    # Add prereqs (split)
    # prereq_elements = driver.find_elements(By.CLASS_NAME, "prereq")
    # if len(prereq_elements) == 1:
    #     prereq_text = driver.find_element(By.CLASS_NAME, "prereq").text
    #     course_data["prereq_text"] = prereq_text
    #     prereq_text = prereq_text.split(": ")[1]
    #     remove = ["(",")"," or minimum score of WAIVE in 'Graduate Student PreReq",".","*","'","\n"," May be taken concurrently"]
    #     replace_with_comma = [" or ", " and "]
    #     for to_remove in remove:
    #         prereq_text = prereq_text.replace(to_remove, "")
    #     for to_replace in replace_with_comma:
    #         prereq_text = prereq_text.replace(to_replace, ", ")
    #     prereqs = prereq_text.split(", ")
    #     last_department = "NULL"
    #     processed_prereqs = []
    #     for prereq in prereqs:
    #         if len(prereq) == 4:
    #             processed_prereqs.append(last_department + " " + prereq)
    #         else:
    #             processed_prereqs.append(prereq)
    #             last_department = prereq.split(" ")[0]
    #     course_data["prereqs"] = processed_prereqs
    #     print(processed_prereqs)
    # else:
    #     course_data["prereqs"] = []
    #     course_data["prereq_text"] = "NA"

    if include_critical_review:
        data = scrape_course_on_critical_review(driver, wait, first=first)
        for key, value in data.items():
            course_data[key] = value

    print("Finished scraping course: ", course_data["code"], course_data["title"])
    return course_data

def scrape_course_on_critical_review(driver, wait, first=False):
    data = {}
    # Open critical review link in new tab
    critical_review_link = driver.find_element(By.CSS_SELECTOR, ".detail-resources_critical_review_html a")
    data["critical_review_url"] = critical_review_link.get_attribute("href")
    critical_review_link.send_keys(Keys.CONTROL + Keys.RETURN)
    driver.switch_to.window(driver.window_handles[-1])
    if first:
        wait.until(EC.presence_of_element_located((By.ID, "brown-brand")))
        first = False

        # login to critical review
        print("FOUND brown band")
        username_field = driver.find_element(By.ID, "username")
        username_field.send_keys(username)
        time.sleep(0.5)
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password)
        time.sleep(0.5)
        button = driver.find_element(By.CSS_SELECTOR, "#login > fieldset > button")
        button.click()

    wait.until(EC.presence_of_element_located((By.ID, "logo")))

    course_title_elements = driver.find_elements(By.ID, "course_title")
    print("course title elements len:", len(course_title_elements))
    if len(course_title_elements) != 0:
        # Grab avg/max hours
        avg_hrs = driver.find_element(By.CSS_SELECTOR, "#statistics_panel > div.stats_without_header > table > tbody > tr:nth-child(2) > td:nth-child(1) > div > div.value").text
        max_hrs = driver.find_element(By.CSS_SELECTOR, "#statistics_panel > div.stats_without_header > table > tbody > tr:nth-child(2) > td:nth-child(2) > div > div.value").text
        
        # Grab ratings
        course_rating = driver.find_element(By.CSS_SELECTOR, "#statistics_panel > div.stats_without_header > table > tbody > tr:nth-child(1) > td:nth-child(1) > div > div.value").text
        professor_rating = driver.find_element(By.CSS_SELECTOR, "#statistics_panel > div.stats_without_header > table > tbody > tr:nth-child(1) > td:nth-child(2) > div > div.value").text
        
        # grab description
        desc = driver.find_element(By.CSS_SELECTOR, "#full_review_contents").text
        
        professor_and_term = driver.find_element(By.CSS_SELECTOR, ".course_code").text
        
        data = {"average_hours": avg_hrs, "max_hours": max_hrs, "course_rating": course_rating, "professor_rating": professor_rating, "description": desc, "professor_and_term": professor_and_term}
    else:
        print("No Critical Review entry")
        
    print("close tab!")
    # Close tab
    #obtain parent window handle
    p= driver.window_handles[0]
    #obtain browser tab window
    c = driver.window_handles[1]
    #switch to tab browser
    driver.switch_to.window(c)
    #close browser tab window
    driver.close()
    #switch to parent window
    driver.switch_to.window(p)
    
    return data

if __name__ == "__main__":
    courses = scrape_all_courses(include_critical_review=True)
    with open(f"./data/all_courses.json", "w") as f:
        json.dump(courses, f)
        
        
# TODO - some courses on cab don't have all the field so make everything in scrape course optional