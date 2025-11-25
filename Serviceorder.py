from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime

# -------------------------------------------------
# Logger
# -------------------------------------------------
def log(msg):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(msg)
    with open("service_order_report.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")

# -------------------------------------------------
# Start Browser
# -------------------------------------------------
service = Service(
    r"C:\Users\bhavy\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
)

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.page_load_strategy = "eager"

driver = webdriver.Chrome(service=service, options=options)
wait = WebDriverWait(driver, 20)


# -------------------------------------------------
# LOGIN
# -------------------------------------------------
try:
    log("🌐 Opening Login Page...")
    driver.get("https://pos-stage.feelaxo.com/admin")

    wait.until(EC.presence_of_element_located((By.ID, "login")))
    log("✅ Login Page Loaded")

    driver.find_element(By.ID, "login").send_keys("clientdemo@feelaxo.com")
    driver.find_element(By.ID, "password").send_keys("feelaxo@24")
    log("🔐 Credentials Entered")

    driver.find_element(
        By.XPATH,
        "//button[@type='submit' or contains(text(),'Login') or contains(@class,'btn')]",
    ).click()

    wait.until(EC.url_contains("/admin"))
    log("🎉 Login Successful")

except Exception as e:
    log(f"❌ Login failed: {e}")
    driver.quit()
    exit()

time.sleep(2)


# -------------------------------------------------
# GO TO POS SERVICES
# -------------------------------------------------
try:
    pos_url = "https://pos-stage.feelaxo.com/admin/pos#services"
    log("🌐 Navigating to POS Services")
    driver.get(pos_url)

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".service-card, .card")))
    log("💇 Services Loaded")

except Exception as e:
    log(f"❌ Failed loading services: {e}")
    driver.quit()
    exit()

time.sleep(2)


# -------------------------------------------------
# SELECT FIRST SERVICE
# -------------------------------------------------
try:
    first_service = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".service-card, .card"))
    )
    first_service.click()
    log("💇 Selected first service")

except Exception as e:
    log(f"❌ Unable to select service: {e}")
    driver.quit()
    exit()

time.sleep(2)


# -------------------------------------------------
# SELECT CUSTOMER (Vue Multiselect)
# -------------------------------------------------
try:
    log("🧍 Selecting customer...")

    customer_input = wait.until(
        EC.presence_of_element_located((By.ID, "ajax"))
    )

    driver.execute_script("arguments[0].scrollIntoView(true);", customer_input)
    time.sleep(1)

    wrapper = customer_input.find_element(
        By.XPATH, "./ancestor::div[contains(@class,'multiselect')]"
    )
    wrapper.click()
    time.sleep(0.7)

    customer_input.send_keys("Walk")
    log("⌨️ Typed 'Walk' into customer search")
    time.sleep(1)

    option = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//li[contains(@id,'ajax-') and contains(@class,'multiselect__element')]")
        )
    )
    driver.execute_script("arguments[0].click();", option)
    log("👤 Customer selected: Walk-in Customer")

except Exception as e:
    log(f"❌ CUSTOMER SELECTION FAILED: {e}")
    driver.quit()
    exit()

time.sleep(2)


# -------------------------------------------------
# CLICK SAVE & CONTINUE
# -------------------------------------------------
try:
    save_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(),'Save') or contains(text(),'Continue')]")
        )
    )
    save_btn.click()
    log("💾 Clicked Save & Continue")

except Exception as e:
    log(f"❌ Failed to click Save & Continue: {e}")
    driver.quit()
    exit()

time.sleep(2)


# -------------------------------------------------
# FIXED → SELECT GENDER (MANDATORY)
# -------------------------------------------------
try:
    log("🎯 Waiting for checkout modal...")

    wait.until(EC.visibility_of_element_located(
        (By.CSS_SELECTOR, ".customer-summary, .modal-content, .checkout-modal")
    ))

    log("🎯 Locating gender options...")

    wait.until(EC.presence_of_element_located((By.ID, "genderMaleInline")))

    gender_male = driver.find_element(By.ID, "genderMaleInline")

    driver.execute_script("arguments[0].scrollIntoView(true);", gender_male)
    time.sleep(0.5)

    driver.execute_script("arguments[0].click();", gender_male)

    log("♂️ Gender selected: Male")

except Exception as e:
    log(f"❌ Failed selecting gender (modal not ready yet): {e}")
    driver.quit()
    exit()

time.sleep(1)


# -------------------------------------------------
# PAYMENT METHOD (CASH)
# -------------------------------------------------
try:
    log("💰 Selecting payment method: Cash")

    cash_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(),'Cash')]")
        )
    )
    driver.execute_script("arguments[0].click();", cash_button)
    log("💵 Payment method selected: Cash")

except:
    log("⚠ Cash button not found — maybe already selected.")

time.sleep(1)


# -------------------------------------------------
# FINAL ORDER PAYMENT
# -------------------------------------------------
try:
    final_pay_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(),'Confirm') or contains(text(),'Pay') or contains(text(),'Complete')]")
        )
    )
    final_pay_btn.click()

    log("🧾 Order submitted successfully!")

except Exception as e:
    log(f"❌ Failed completing order: {e}")
    driver.quit()
    exit()

log("🎉 SERVICE ORDER AUTOMATION COMPLETED SUCCESSFULLY!")
# driver.quit()
