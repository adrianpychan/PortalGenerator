from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pandas as pd
import os
from dotenv import load_dotenv

#Load .env file
load_dotenv(".env") #Change this to your .env file pathway

#Set Course Name here and Length of Courses here:
df = pd.read_csv("bootcamp.csv")
course_name = df["course_title"].unique()[0]
course_length = df.columns[-1].split("_")[0].split("lesson")[-1]

#File path of bootcamp.csv

filename = "bootcamp.csv"
current_folder = os.getcwd()
file_path = os.path.join(current_folder, filename)

#Setup
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options = chrome_options, service=Service(ChromeDriverManager().install()))

def creation(course_name, course_length):
    driver.maximize_window()
    driver.get("https://portal.preface.ai/users/sign_in")
    
    #Logging In
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="user_login"]'))).send_keys(os.getenv('PORTAL_USERNAME'))
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="user_password"]'))).send_keys(os.getenv('PORTAL_PASSWORD'))
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="new_user"]/input[3]'))).submit()

    #Create New Course
    driver.get("https://portal.preface.ai/courses/new")

    #Subject
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="course_subject_id"]/option[7]'))).click()

    #Title
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="course_title"]'))).send_keys(course_name) #change

    #Category
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="new_course"]/div[1]/div[4]/span/span[1]/span'))).click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/span/span/span[1]/input'))).send_keys("B2B")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/span/span/span[1]/input'))).send_keys(Keys.RETURN)

    #Ctype
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="course_ctype"]/option[7]'))).click()

    #Position
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="course_position"]'))).send_keys("999")

    #Adult Eligible
    sleep(1)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//input[@id="course_adult_eligible"]'))).location_once_scrolled_into_view
    sleep(2)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//input[@id="course_adult_eligible"]'))).click()

    #Default Number of Schedule of this Course
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="course_num_schedule"]'))).send_keys(course_length) #change

    #Submit
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="new_course"]/div[2]/input'))).submit()

    print("Course created on Portal!")
    sleep(3)

    #Import Business to business camp
    driver.get("https://portal.preface.ai/admin_dashboards/happenings/business_to_business/bulk_new")

    #Uploading bootcamp.csv using file path
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,  '//*[@id="happening_file"]'))).send_keys(file_path)

    #Clicking upload
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="new_happening"]/input[3]'))).submit()

creation(course_name = course_name, course_length = course_length)

# i am not adrian