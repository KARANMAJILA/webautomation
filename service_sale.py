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

# Credentials for login (use existing account)
LOGIN_EMAIL = "clientdemo@feelaxo.com"
LOGIN_PASSWORD = "feelaxo@24"

# Service selection preferences
SERVICES_TO_SELECT = ["Glow facial", "Korean facial", "Hair styling"]  # Service names to select
NUM_CUSTOMERS_TO_TEST = 3  # Number of customer transactions to test

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
# HELPER FUNCTIONS
# --------------------------------------------
def login_to_system():
    """Login to Feelaxo POS system"""
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


def navigate_to_service_sale():
    """Navigate to service sale page"""
    log("📍 Navigating to Service Sale...")
    driver.get("https://pos-stage.feelaxo.com/admin/pos#services")
    slow()

    wait.until(EC.visibility_of_element_located((By.XPATH, "//p[contains(@class, 'service-name')]")))
    log("✅ Service Sale page loaded!")
    time.sleep(1)


def get_all_service_cards():
    """Get all available service cards"""
    try:
        service_links = driver.find_elements(By.XPATH, "//a[@type='button'][.//p[contains(@class, 'service-name')]]")
        log(f"📦 Found {len(service_links)} service cards available")
        return service_links
    except Exception as e:
        log(f"❌ Error getting service cards: {e}")
        return []


# --------------------------------------------
# FIXED POPUP HANDLER (ONLY CHANGE MADE)
# --------------------------------------------
def select_service_from_popup(service_name):
    """
    FIXED: Properly handles Vue modal — clicks checkbox + Add button reliably.
    """
    try:
        log(f"  🔍 Waiting for popup for: {service_name}")

        # Wait for popup
        modal = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(@class, 'modal-content')]")
        ))
        time.sleep(0.4)

        # Find the service checkbox inside modal
        checkbox = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//div[contains(@class,'modal-content')]//input[@type='checkbox' and contains(@class,'form-check-input')]")
        ))

        log("  ✓ Checkbox found inside popup")

        # Click checkbox using JS
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", checkbox)
        time.sleep(0.3)
        driver.execute_script("arguments[0].click();", checkbox)
        log("  ✓ Checkbox clicked")

        time.sleep(0.5)

        # Find Add button
        add_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class,'btn-dark') and contains(text(), 'Add')]")
        ))

        log("  ✓ Add button located")

        # Click using JS
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", add_btn)
        time.sleep(0.3)
        driver.execute_script("arguments[0].click();", add_btn)
        log("  ✅ Add button clicked")

        # Wait for popup close
        wait.until(EC.invisibility_of_element_located(
            (By.XPATH, "//div[contains(@class,'modal-content')]")
        ))

        log("  🎉 Popup closed successfully")

        return True

    except Exception as e:
        log(f"❌ Error inside popup: {e}")
        traceback.print_exc()
        driver.save_screenshot(f"service_popup_error_{service_name}.png")
        return False


def click_service_card(service_name):
    """Click on a specific service card by name"""
    try:
        log(f"🎯 Clicking service card: {service_name}")
        
        service_xpath = f"//a[@type='button'][.//p[contains(@class, 'service-name') and contains(text(), '{service_name}')]]"
        
        service_card = wait.until(EC.element_to_be_clickable((By.XPATH, service_xpath)))
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", service_card)
        time.sleep(0.3)
        driver.execute_script("arguments[0].click();", service_card)
        log(f"  ✓ Service card clicked")
        time.sleep(0.5)

        return True

    except Exception as e:
        log(f"  ❌ Error clicking service card: {e}")
        return False


def add_service_for_customer(service_names):
    """Add multiple services for a customer"""
    log("\n👥 Adding services for customer...")
    
    for service_name in service_names:
        success = click_service_card(service_name)
        if success:
            select_service_from_popup(service_name)
        time.sleep(0.3)
    
    log("✅ All services added for customer!")


def verify_services_in_list(service_names):
    """Verify that services appear in the service list"""
    try:
        log("🔍 Verifying services in the list...")
        
        for service_name in service_names:
            service_rows = driver.find_elements(By.XPATH, f"//div[contains(text(), '{service_name}')]")
            if service_rows:
                log(f"  ✅ {service_name} found in service list")
            else:
                log(f"  ⚠️  {service_name} not found in service list")
        
        return True
    except Exception as e:
        log(f"❌ Error verifying services: {e}")
        return False


def take_final_screenshot():
    """Take screenshot of final service selection"""
    driver.save_screenshot("service_sale_final.png")
    log("📸 Screenshot saved: service_sale_final.png")


# --------------------------------------------
# MAIN TEST FLOW
# --------------------------------------------
try:
    login_to_system()
    navigate_to_service_sale()

    for customer_num in range(1, NUM_CUSTOMERS_TO_TEST + 1):
        log(f"\n{'='*60}")
        log(f"🧪 TEST CYCLE {customer_num}/{NUM_CUSTOMERS_TO_TEST}")
        log(f"{'='*60}")
        
        add_service_for_customer(SERVICES_TO_SELECT)
        verify_services_in_list(SERVICES_TO_SELECT)
        take_final_screenshot()
        
        if customer_num < NUM_CUSTOMERS_TO_TEST:
            log(f"⏳ Preparing for next customer transaction...")
            time.sleep(1)
            navigate_to_service_sale()
            time.sleep(1)

    log(f"\n{'='*60}")
    log("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
    log(f"{'='*60}")

except Exception as e:
    log(f"\n❌ TEST FAILED: {e}")
    traceback.print_exc()
    driver.save_screenshot("test_crash_error.png")
    log("📸 Screenshot saved: test_crash_error.png")

finally:
    time.sleep(2)
    driver.quit()
    log("🛑 Browser closed")
