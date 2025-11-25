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

# Slow motion for testing
SLOW_MODE = True
SLOW_DELAY = 0.8

def slow():
    if SLOW_MODE:
        time.sleep(SLOW_DELAY)

def log(msg):
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# Credentials for login
LOGIN_EMAIL = "clientdemo@feelaxo.com"
LOGIN_PASSWORD = "feelaxo@24"

# Services to add per category
SERVICES_DATA = {
    "Waxing": [
        {
            "service": "Full Body Wax",
            "price": 2500,
            "onlinePrice": 2700,
            "duration": 90,
            "gender": "Female",
            "isOnline": True,
            "description": "Complete full body waxing service for smooth skin"
        },
        {
            "service": "Half Body Wax",
            "price": 1500,
            "onlinePrice": 1700,
            "duration": 60,
            "gender": "Female",
            "isOnline": True,
            "description": "Half body waxing including legs and underarms"
        },
        {
            "service": "Facial Wax",
            "price": 800,
            "onlinePrice": 900,
            "duration": 30,
            "gender": "Female",
            "isOnline": True,
            "description": "Facial hair removal waxing service"
        }
    ],
    "Massage": [
        {
            "service": "Swedish Massage",
            "price": 3000,
            "onlinePrice": 3200,
            "duration": 60,
            "gender": "Unisex",
            "isOnline": True,
            "description": "Traditional Swedish massage for muscle relaxation"
        },
        {
            "service": "Aromatherapy Massage",
            "price": 3500,
            "onlinePrice": 3800,
            "duration": 75,
            "gender": "Unisex",
            "isOnline": True,
            "description": "Relaxing massage with aromatic oils"
        }
    ],
    "Facials": [
        {
            "service": "Hydrating Facial",
            "price": 1200,
            "onlinePrice": 1400,
            "duration": 45,
            "gender": "Female",
            "isOnline": True,
            "description": "Deep hydration facial treatment for dry skin"
        },
        {
            "service": "Anti-Aging Facial",
            "price": 2000,
            "onlinePrice": 2200,
            "duration": 60,
            "gender": "Female",
            "isOnline": True,
            "description": "Advanced anti-aging facial with collagen boost"
        }
    ]
}

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
    """Login to Feelaxo admin"""
    log("🔁 Logging in to Feelaxo...")
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
    log("✅ Login successful!")
    time.sleep(1)

# --------------------------------------------
# NAVIGATE TO SERVICES PAGE
# --------------------------------------------
def navigate_to_services():
    """Navigate to services management page"""
    log("📍 Navigating to Services Management...")
    driver.get("https://pos-stage.feelaxo.com/admin/services-type")
    slow()

    wait.until(EC.visibility_of_element_located((By.ID, "service")))
    log("✅ Services page loaded!")
    time.sleep(1)

# --------------------------------------------
# ADD SERVICE FUNCTION
# --------------------------------------------
def add_service(service_data):
    """Add a single service with the provided data"""
    try:
        log(f"  ➕ Adding service: {service_data['service']}")
        time.sleep(0.5)

        # Service Name
        service_input = driver.find_element(By.ID, "service")
        service_input.clear()
        service_input.send_keys(service_data['service'])
        time.sleep(0.3)

        # Price
        price_input = driver.find_element(By.ID, "price")
        price_input.clear()
        price_input.send_keys(str(service_data['price']))
        time.sleep(0.3)

        # Online Price
        online_price_input = driver.find_element(By.ID, "onlinePrice")
        online_price_input.clear()
        online_price_input.send_keys(str(service_data['onlinePrice']))
        time.sleep(0.3)

        # Duration
        duration_input = driver.find_element(By.ID, "duration")
        duration_input.clear()
        duration_input.send_keys(str(service_data['duration']))
        time.sleep(0.3)

        # Gender
        gender_select = Select(driver.find_element(By.ID, "gender"))
        gender_select.select_by_value(service_data['gender'])
        time.sleep(0.3)

        # Online Booking Toggle
        if service_data['isOnline']:
            toggle_btn = driver.find_element(By.ID, "isOnlineToggle")
            is_active = toggle_btn.get_attribute("data-is_active")
            
            # Click only if not already active
            if is_active != "1":
                driver.execute_script("arguments[0].click();", toggle_btn)
                time.sleep(0.3)
        
        time.sleep(0.3)

        # Description
        desc_textarea = driver.find_element(By.ID, "description")
        desc_textarea.clear()
        desc_textarea.send_keys(service_data['description'])
        time.sleep(0.3)

        # Submit Form
        submit_btn = driver.find_element(By.XPATH, "//button[@type='submit' and contains(text(), 'Add Service')]")
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", submit_btn)
        time.sleep(0.3)
        driver.execute_script("arguments[0].click();", submit_btn)
        
        log(f"  ✅ Service '{service_data['service']}' added successfully!")
        time.sleep(1)

        return True

    except Exception as e:
        log(f"  ❌ Error adding service: {e}")
        traceback.print_exc()
        driver.save_screenshot(f"service_error_{service_data['service']}.png")
        return False

# --------------------------------------------
# CLICK CATEGORY TAB
# --------------------------------------------
def click_category_tab(category_name):
    """Click on a category tab to switch to that category"""
    try:
        log(f"\n🏷️  Switching to category: {category_name}")
        
        # Find the button with the category name
        category_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//button[@type='button' and contains(normalize-space(), '{category_name}')]")
        ))
        
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", category_btn)
        time.sleep(0.3)
        driver.execute_script("arguments[0].click();", category_btn)
        
        log(f"  ✓ Category tab clicked")
        time.sleep(1)
        
        # Wait for the form to update
        wait.until(EC.visibility_of_element_located((By.ID, "service")))
        time.sleep(0.5)
        
        return True

    except Exception as e:
        log(f"  ❌ Error clicking category tab: {e}")
        traceback.print_exc()
        return False

# --------------------------------------------
# MAIN TEST FLOW
# --------------------------------------------
try:
    # Step 1: Login
    login_to_system()

    # Step 2: Navigate to Services Page
    navigate_to_services()

    # Step 3: Add services for each category
    for category_name, services_list in SERVICES_DATA.items():
        log(f"\n{'='*60}")
        log(f"📦 Adding services for category: {category_name}")
        log(f"{'='*60}")

        # Click the category tab
        if click_category_tab(category_name):
            # Add each service in this category
            for idx, service_data in enumerate(services_list, 1):
                log(f"\n  Service {idx}/{len(services_list)}")
                add_service(service_data)
        else:
            log(f"❌ Failed to switch to {category_name} category, skipping...")

    log(f"\n{'='*60}")
    log("🎉 ALL SERVICES ADDED SUCCESSFULLY!")
    log(f"{'='*60}")

except Exception as e:
    log(f"\n❌ SCRIPT FAILED: {e}")
    traceback.print_exc()
    driver.save_screenshot("add_services_error.png")
    log("📸 Screenshot saved: add_services_error.png")

finally:
    time.sleep(2)
    driver.quit()
    log("🛑 Browser closed")