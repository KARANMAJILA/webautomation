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
PROFILE_IMAGE = r
ID_IMAGE = PROFILE_IMAGE"C:\Users\bhavy\Downloads\WhatsApp Image 2025-11-11 at 11.44.53 AM (1).jpeg"

# Slow motion for registration & login
SLOW_MODE = True
SLOW_DELAY = 1.2

def slow():
    if SLOW_MODE:
        time.sleep(SLOW_DELAY)

def log(msg):
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# --------------------------------------------
# Random Data Helpers
# --------------------------------------------
def random_phone():
    return "9" + "".join(str(random.randint(0,9)) for _ in range(9))

def random_name():
    first = ["Karan","Rohan","Amit","Dev","Priya","Anita"]
    last = ["Sharma","Patel","Yadav","Agarwal","Mehta"]
    return f"{random.choice(first)} {random.choice(last)}"

def random_email():
    return f"user{random.randint(1000,9999)}@mail.com"

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
# MAIN FLOW — REGISTRATION → LOGIN → ADD 5 STAFF
# --------------------------------------------
try:
    # ---------------------------
    # 1) REGISTRATION
    # ---------------------------
    log("🌐 Opening registration...")
    driver.get("https://pos-stage.feelaxo.com/admin/register")
    slow()

    wait.until(EC.visibility_of_element_located((By.ID,"name")))

    reg_email = random_email()
    reg_password = "12345678"

    # STEP 1
    driver.find_element(By.ID,"name").send_keys("John Doe")
    slow()
    driver.find_element(By.ID,"email").send_keys(reg_email)
    slow()
    driver.find_element(By.ID,"password").send_keys(reg_password)
    slow()
    driver.find_element(By.ID,"password_confirmation").send_keys(reg_password)
    slow()

    driver.find_element(By.XPATH,"//button[contains(text(),'Next')]").click()
    slow()


    # STEP 2
    wait.until(EC.visibility_of_element_located((By.ID,"business_name")))
    driver.find_element(By.ID,"business_name").send_keys("My Automated Salon Business")
    slow()

    driver.find_element(By.ID,"owner_phone").send_keys(random_phone())
    slow()
    driver.find_element(By.ID,"designation").send_keys("Owner")
    slow()
    driver.find_element(By.ID,"phone").send_keys(random_phone())
    slow()

    driver.find_element(By.ID,"business_type").send_keys("Salon")
    slow()
    driver.find_element(By.ID,"staff_count").send_keys("5")
    slow()
    driver.find_element(By.ID,"country").send_keys("India")
    slow()

    # State
    state = driver.find_element(By.ID,"state")
    for _ in range(20):
        opts = state.find_elements(By.TAG_NAME,"option")
        if len(opts) > 1:
            break
        time.sleep(0.3)

    for o in opts:
        if o.get_attribute("value"):
            state.send_keys(o.text)
            break
    slow()

    # City
    city = driver.find_element(By.ID,"city")
    for _ in range(20):
        opts = city.find_elements(By.TAG_NAME,"option")
        if len(opts) > 1:
            break
        time.sleep(0.3)

    for o in opts:
        if o.get_attribute("value"):
            city.send_keys(o.text)
            break
    slow()

    driver.find_element(By.ID,"area").send_keys("Sector 62")
    slow()
    driver.find_element(By.ID,"address").send_keys("Business Street")
    slow()
    driver.find_element(By.ID,"zipcode").send_keys("201301")
    slow()

    next_btn = driver.find_element(By.XPATH,"//button[contains(text(),'Next')]")
    driver.execute_script("arguments[0].click();", next_btn)
    slow()


    # STEP 3 – 180-word description
    wait.until(EC.visibility_of_element_located((By.ID,"description")))

    description_text = (
        "This automated test business is created specifically to evaluate the complete workflow, "
        "performance, and reliability of the salon management system under different real-world "
        "operational conditions. The objective is to replicate day-to-day activities of an actual "
        "salon, including customer appointment handling, staff schedule management, service "
        "tracking, and data processing. By simulating realistic business operations, this environment "
        "helps verify that crucial functionalities—such as booking, billing, service selection, "
        "customer history, staff availability, notifications, and time-slot allocation—work without "
        "errors. The system is tested for consistency, user experience, responsiveness, and stability "
        "during various scenarios like high-traffic usage, multiple user interactions, and complex "
        "workflow transitions. The test business also evaluates form validations, error handling, file "
        "uploads, image processing, and backend API reliability. It further ensures that new updates "
        "or feature integrations do not affect existing capabilities of the platform. This automated "
        "setup enables comprehensive quality assurance, allowing developers and testers to identify "
        "potential issues before they impact real users. By using this controlled simulation, the goal "
        "is to provide a smooth, efficient, and error-free experience for actual salon owners, staff "
        "members, and clients who rely on the platform for daily operations."
    )

    driver.find_element(By.ID,"description").send_keys(description_text)
    slow()

    driver.find_element(By.ID,"business_document").send_keys(
        r"C:\Users\bhavy\Downloads\Feelaxotest.pdf"
    )
    slow()

    driver.find_element(By.XPATH,"//button[contains(text(),'Next')]").click()
    slow()


    # STEP 4
    wait.until(EC.visibility_of_element_located((By.ID,"mondayToggle")))
    driver.find_element(By.XPATH,"//button[contains(text(),'Next')]").click()
    slow()


    # STEP 5
    wait.until(EC.presence_of_element_located((By.ID,"business_thumbnail")))
    driver.find_element(By.ID,"business_thumbnail").send_keys(PROFILE_IMAGE)
    driver.find_element(By.ID,"gallery_images").send_keys(
        f"{PROFILE_IMAGE}\n{PROFILE_IMAGE}\n{PROFILE_IMAGE}\n{PROFILE_IMAGE}"
    )
    slow()

    driver.find_element(By.XPATH,"//button[contains(text(),'Next')]").click()
    slow()


    # STEP 6
    wait.until(EC.visibility_of_element_located((By.ID,"formSummary")))
    driver.find_element(By.XPATH,"//button[contains(text(),'Confirm')]").click()
    slow()


    # STEP 7 — DONE
    wait.until(EC.presence_of_element_located((By.ID,"plansContainer")))
    log("🎉 Registration completed!")
    slow()


    # ---------------------------
    # 2) LOGIN
    # ---------------------------
    log("🔁 Logging in with new account...")
    driver.get("https://pos-stage.feelaxo.com/admin")
    slow()

    wait.until(EC.visibility_of_element_located((By.ID,"login")))
    driver.find_element(By.ID,"login").send_keys(reg_email)
    slow()
    driver.find_element(By.ID,"password").send_keys(reg_password)
    slow()

    driver.find_element(By.XPATH,"//button[@type='submit']").click()
    slow()

    wait.until(EC.url_contains("/admin"))
    log("🎉 Login successful!")
    slow()


    # ---------------------------
    # 3) ADD 5 STAFF
    # ---------------------------
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
        # ⭐ FINAL TIME PICKER INSERTED HERE (WORKING)
        # ------------------------------------------------------
        try:
            # ---- FROM TIME ----
            frm = driver.find_element(By.NAME, "work_time_from")
            frm.click()
            time.sleep(0.4)

            driver.find_element(By.XPATH, "//span[normalize-space()='09']").click()
            time.sleep(0.2)

            driver.find_element(By.XPATH, "//span[normalize-space()='00']").click()
            time.sleep(0.2)

            container = driver.find_element(By.XPATH, "//div[contains(@class,'v-time-picker')]")
            driver.execute_script("arguments[0].scrollLeft = arguments[0].scrollWidth;", container)
            time.sleep(0.3)

            driver.find_element(By.XPATH, "//span[normalize-space()='AM']").click()
            time.sleep(0.2)

            driver.execute_script("document.body.click();")
            time.sleep(0.2)

            # ---- TO TIME ----
            to = driver.find_element(By.NAME, "work_time_to")
            to.click()
            time.sleep(0.4)

            driver.find_element(By.XPATH, "//span[normalize-space()='06']").click()
            time.sleep(0.2)

            driver.find_element(By.XPATH, "//span[normalize-space()='00']").click()
            time.sleep(0.2)

            container = driver.find_element(By.XPATH, "//div[contains(@class,'v-time-picker')]")
            driver.execute_script("arguments[0].scrollLeft = arguments[0].scrollWidth;", container)
            time.sleep(0.3)

            driver.find_element(By.XPATH, "//span[normalize-space()='PM']").click()
            time.sleep(0.2)

            driver.execute_script("document.body.click();")
            time.sleep(0.2)

            log("✔ Working hours set successfully (09:00 AM → 06:00 PM)")

        except Exception as e:
            log(f"❌ Working hours failed: {e}")
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

    log("➕ Adding 5 staff...")
    for _ in range(5):
        add_staff()

    log("🎯 DONE — Registration + Login + 5 Staff Added Successfully")

except Exception as e:
    log(f"❌ Script crashed: {e}")
    driver.save_screenshot("crash_error.png")
    log("📸 Screenshot saved: crash_error.png")
