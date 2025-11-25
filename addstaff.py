import os
import random
import datetime
import traceback
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# --------------------------------------------
# CONFIG
# --------------------------------------------
CHROME_DRIVER_PATH = r"C:\Users\bhavy\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
PROFILE_IMAGE = r"C:\Users\bhavy\Downloads\WhatsApp Image 2025-11-11 at 11.44.53 AM (1).jpeg"
ID_IMAGE = PROFILE_IMAGE

# Slow motion for testing
SLOW_MODE = True
SLOW_DELAY = 1.2

def slow():
    if SLOW_MODE:
        time.sleep(SLOW_DELAY)

def log(msg):
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Credentials for login (use existing account)
LOGIN_EMAIL = "user5684@mail.com"
LOGIN_PASSWORD = "12345678"

# Number of staff to add
NUM_STAFF_TO_ADD = 5

# --------------------------------------------
# Random Data Helpers
# --------------------------------------------
def random_phone():
    return "9" + "".join(str(random.randint(0,9)) for _ in range(9))

def random_name():
    first = ["Karan","Rohan","Amit","Dev","Priya","Anita"]
    last = ["Sharma","Patel","Yadav","Agarwal","Mehta"]
    return f"{random.choice(first)} {random.choice(last)}"

def random_staff_email(name):
    return f"{name.replace(' ','').lower()}{random.randint(100,999)}@gmail.com"

def random_salary():
    return str(random.randint(15000,40000))

def random_password():
    return f"Pass@{random.randint(1000,9999)}"

# --------------------------------------------
# Selenium Setup
# --------------------------------------------
service = Service(CHROME_DRIVER_PATH)
options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--start-maximized")
options.page_load_strategy = "eager"

driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 25)

# --------------------------------------------
# LOGIN FUNCTION
# --------------------------------------------
def login_to_system():
    """Login to Feelaxo POS system"""
    log("🔁 Logging in with existing account...")
    driver.get("https://pos-stage.feelaxo.com/admin")
    slow()

    wait.until(EC.visibility_of_element_located((By.ID, "login")))
    driver.find_element(By.ID, "login").send_keys(LOGIN_EMAIL)
    slow()
    driver.find_element(By.ID, "password").send_keys(LOGIN_PASSWORD)
    slow()

    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    slow()

    wait.until(EC.url_contains("/admin"))
    log("🎉 Login successful!")
    slow()

# --------------------------------------------
# ADD STAFF FUNCTION
# --------------------------------------------
def add_staff():
    driver.get("https://pos-stage.feelaxo.com/admin/users/create")
    wait.until(EC.visibility_of_element_located((By.NAME,"name")))

    name = random_name()
    phone = random_phone()
    staff_email = random_staff_email(name)
    pwd = random_password()

    driver.find_element(By.NAME,"name").send_keys(name)
    driver.find_element(By.NAME,"phone").send_keys(phone)
    driver.find_element(By.NAME,"password").send_keys(pwd)
    driver.find_element(By.NAME,"job_title").send_keys("Senior Barber")

    # ------------------------------------------------------
    # ⭐ SMART TIME PICKER - Types time and AM/PM
    # ------------------------------------------------------
    try:
        # ---- FROM TIME ----
        frm = driver.find_element(By.NAME, "work_time_from")
        frm.click()
        time.sleep(0.4)

        # Type the time directly
        frm.send_keys("0954")
        time.sleep(0.3)
        
        # Type 'a' for AM
        frm.send_keys("a")
        time.sleep(0.2)

        driver.execute_script("document.body.click();")
        time.sleep(0.3)

        log("✔ From time set: 09:54 AM")

        # ---- TO TIME ----
        to = driver.find_element(By.NAME, "work_time_to")
        to.click()
        time.sleep(0.4)

        # Type the time directly
        to.send_keys("0618")
        time.sleep(0.3)
        
        # Type 'p' for PM
        to.send_keys("p")
        time.sleep(0.2)

        driver.execute_script("document.body.click();")
        time.sleep(0.3)

        log("✔ To time set: 06:18 PM")
        log("✔ Working hours set successfully (09:54 AM → 06:18 PM)")

    except Exception as e:
        log(f"❌ Working hours failed: {e}")
        traceback.print_exc()
        driver.save_screenshot("timepicker_fail.png")

    Select(driver.find_element(By.NAME,"gender")).select_by_value("male")

    driver.find_element(By.NAME,"email").send_keys(staff_email)
    driver.find_element(By.NAME,"salary").send_keys(random_salary())
    driver.find_element(By.NAME,"address").send_keys("Mumbai")

    driver.find_element(By.NAME,"profile").send_keys(PROFILE_IMAGE)
    Select(driver.find_element(By.NAME,"identity_proof_type")).select_by_value("aadhar_card")
    driver.find_element(By.NAME,"identity_proof").send_keys(ID_IMAGE)

    # SAVE
    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH,"//button[@type='submit']")))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", save_btn)
    time.sleep(0.4)
    driver.execute_script("arguments[0].click();", save_btn)

    time.sleep(2)
    log(f"✔ Staff added: {name}")

# --------------------------------------------
# MAIN FLOW — LOGIN → ADD STAFF
# --------------------------------------------
try:
    # Step 1: Login
    login_to_system()

    # Step 2: Add multiple staff members
    log("➕ Adding staff members...")
    for i in range(1, NUM_STAFF_TO_ADD + 1):
        log(f"\n🧪 Adding Staff {i}/{NUM_STAFF_TO_ADD}")
        add_staff()
        time.sleep(1)

    log(f"\n🎯 DONE — Login + {NUM_STAFF_TO_ADD} Staff Added Successfully")

except Exception as e:
    log(f"❌ Script crashed: {e}")
    traceback.print_exc()
    driver.save_screenshot("crash_error.png")
    log("📸 Screenshot saved: crash_error.png")

finally:
    time.sleep(2)
    driver.quit()
    log("🛑 Browser closed")