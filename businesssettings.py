import time
import datetime
import traceback

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

LOGIN_EMAIL = "user5684@mail.com"
LOGIN_PASSWORD = "12345678"

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

service = Service(CHROME_DRIVER_PATH)
driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 20)

def log(msg):
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {msg}")

# ----------------------------------------------------------
# LOGIN FUNCTION
# ----------------------------------------------------------
def login_to_system():
    log("Logging in...")
    driver.get("https://pos-stage.feelaxo.com/admin")
    wait.until(EC.visibility_of_element_located((By.ID, "login")))

    driver.find_element(By.ID, "login").send_keys(LOGIN_EMAIL)
    driver.find_element(By.ID, "password").send_keys(LOGIN_PASSWORD)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    wait.until(EC.url_contains("/admin/dashboard"))
    log("✅ Logged in successfully!")

# ----------------------------------------------------------
# OPEN BUSINESS SETTINGS PAGE
# ----------------------------------------------------------
def open_business_settings():

    log("📂 Opening Settings menu...")

    settings_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[contains(@class,'side-menu__label') and text()='Settings']")
    ))
    settings_btn.click()
    time.sleep(1)

    log("⚙ Clicking Business Settings...")

    business_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(@class,'slide-item') and contains(text(),'Business Settings')]")
    ))
    business_btn.click()

    wait.until(EC.visibility_of_element_located((By.XPATH, "//h4[text()='Business Details']")))
    log("✅ Business settings page loaded!")

# ----------------------------------------------------------
# EDIT BUSINESS SETTINGS — FULL FIXED VERSION
# ----------------------------------------------------------
def edit_business_settings():

    log("✏ Editing Business Name...")
    driver.find_element(By.NAME, "business_name").clear()
    driver.find_element(By.NAME, "business_name").send_keys("Test Automation Salon")

    log("✏ Editing Contact Name...")
    driver.find_element(By.NAME, "name").clear()
    driver.find_element(By.NAME, "name").send_keys("Automation User")

    log("✏ Editing Address...")
    addr = driver.find_element(By.NAME, "address")
    addr.clear()
    addr.send_keys("Auto Street 101, Automation City, India")

    # -------------------------------
    # FIX: FORCE BLUR BEFORE OPENING SELECT2
    # -------------------------------
    log("💱 Selecting Currency (INR)...")

    driver.execute_script("arguments[0].blur();", addr)
    time.sleep(1)

    select2_box = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[@class='select2-selection select2-selection--single']")
    ))

    # Real mouse events (Select2 fix)
    driver.execute_script("""
        arguments[0].dispatchEvent(new MouseEvent('mousedown', {bubbles:true}));
    """, select2_box)
    time.sleep(0.2)

    driver.execute_script("""
        arguments[0].dispatchEvent(new MouseEvent('click', {bubbles:true}));
    """, select2_box)
    time.sleep(1)

    currency_item = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//li[contains(text(),'Indian Rupee (INR)')]")
    ))
    driver.execute_script("arguments[0].click();", currency_item)

    log("✅ Currency updated to INR")

    # -------------------------------
    # SELECT STATE + CITY
    # -------------------------------
    log("🌏 Selecting State Maharashtra...")
    Select(driver.find_element(By.NAME, "state")).select_by_visible_text("Maharashtra")

    time.sleep(0.5)

    log("🏙 Selecting City Mumbai...")
    Select(driver.find_element(By.NAME, "city")).select_by_visible_text("Mumbai")

    # -------------------------------
    # ENABLE TAXES BEFORE GST
    # -------------------------------
    log("🟢 Enabling Taxes...")

    gst_toggle = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(@class,'btn-toggle')]")
    ))

    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", gst_toggle)
    time.sleep(0.5)
    driver.execute_script("arguments[0].click();", gst_toggle)

    time.sleep(1)

    # -------------------------------
    # UPLOAD LOGO BEFORE GST
    # -------------------------------
    log("🖼 Uploading Logo...")
    logo = driver.find_element(By.ID, "brand")
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", logo)
    logo.send_keys(r"C:\Users\bhavy\Pictures\logo.png")
    time.sleep(1)

    # -------------------------------
    # UPLOAD PROFILE BEFORE GST
    # -------------------------------
    log("🖼 Uploading Profile Photo...")
    profile = driver.find_element(By.ID, "profile")
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", profile)
    profile.send_keys(r"C:\Users\bhavy\Pictures\profile.jpg")
    time.sleep(1)

    # -------------------------------
    # NOW GST FIELDS ARE VISIBLE
    # -------------------------------
    log("📊 Updating GST...")

    gst_percent = driver.find_element(By.NAME, "gst_percentage")
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", gst_percent)
    time.sleep(0.5)
    gst_percent.clear()
    gst_percent.send_keys("12")

    gst_num = driver.find_element(By.NAME, "gst_number")
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", gst_num)
    time.sleep(0.5)
    gst_num.clear()
    gst_num.send_keys("123456789012345")

    # -------------------------------
    # SAVE SETTINGS
    # -------------------------------
    log("📝 Clicking Update Profile...")
    update_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Update Profile')]")
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", update_btn)
    driver.execute_script("arguments[0].click();", update_btn)

    time.sleep(2)
    log("🎉 Business settings updated successfully!")

# ----------------------------------------------------------
# RUN SCRIPT
# ----------------------------------------------------------
try:
    login_to_system()
    open_business_settings()
    edit_business_settings()

except Exception as e:
    log(f"❌ ERROR: {e}")
    traceback.print_exc()
    driver.save_screenshot("business_update_error.png")

finally:
    log("Closing browser...")
    time.sleep(2)
    driver.quit()
