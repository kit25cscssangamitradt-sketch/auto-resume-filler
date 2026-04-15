import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


print("🚀 Starting Auto Resume Form Filler...")


# ==================== CONFIGURATION ====================
# Change these with your real details
FIRST_NAME = "Sangami"
LAST_NAME = "YourLastName"          # ← Change this
EMAIL = "your.email@example.com"    # ← Change this
MOBILE = "9876543210"
GENDER = "Female"                   # Options: Male, Female, Other
CURRENT_ADDRESS = "123, Main Road, Ambattur, Tamil Nadu 600053"


# Resume file - MUST be absolute path (highly recommended)
# Example: r"C:\Users\Sangami\Documents\resume.pdf"
RESUME_PATH = r"./resume.pdf"       # ← CHANGE THIS to your actual full path


# =====================================================


# Chrome options for better stability
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
# chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Optional: hide automation flag


try:
    # Setup Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    wait = WebDriverWait(driver, 15)  # Explicit wait (recommended)


    # Open the demo form
    url = "https://demoqa.com/automation-practice-form"
    driver.get(url)
    print("✅ Opened the form page.")


    # Fill First Name
    wait.until(EC.presence_of_element_located((By.ID, "firstName"))).send_keys(FIRST_NAME)


    # Fill Last Name
    driver.find_element(By.ID, "lastName").send_keys(LAST_NAME)


    # Fill Email
    driver.find_element(By.ID, "userEmail").send_keys(EMAIL)


    # Select Gender (click on the label, not the hidden radio button)
    gender_xpath = f"//label[text()='{GENDER}']"
    wait.until(EC.element_to_be_clickable((By.XPATH, gender_xpath))).click()


    # Fill Mobile Number
    driver.find_element(By.ID, "userNumber").send_keys(MOBILE)


    # Upload Resume (Picture field in DemoQA - works for PDF/image)
    if os.path.exists(RESUME_PATH):
        try:
            upload_element = wait.until(EC.presence_of_element_located((By.ID, "uploadPicture")))
            upload_element.send_keys(RESUME_PATH)
            print(f"✅ Resume uploaded successfully from: {RESUME_PATH}")
        except Exception as e:
            print(f"⚠️ Upload failed: {e}")
    else:
        print(f"⚠️ Resume file not found at: {RESUME_PATH}")
        print("   Please update RESUME_PATH with the correct absolute path.")


    # Fill Current Address
    address_field = driver.find_element(By.ID, "currentAddress")
    address_field.send_keys(CURRENT_ADDRESS)


    # Optional: Scroll to Submit button
    submit_btn = driver.find_element(By.ID, "submit")
    driver.execute_script("arguments[0].scrollIntoView(true);", submit_btn)
    time.sleep(1)


    # Submit the form
    submit_btn.click()
    print("✅ Form submitted!")


    # Wait to see the success modal
    time.sleep(5)


except Exception as e:
    print(f"❌ Error occurred: {e}")
finally:
    # Close browser
    input("Press Enter to close the browser...")  # Keeps window open until you press Enter
    driver.quit()
    print("🎉 Automation completed! Browser closed.")
