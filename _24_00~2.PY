from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time

TWITTER_EMAIL = "YOUR_EMAIL"
TWITTER_PASSWORD = "YOUR_PASSWORD"

twitter_url = "https://twitter.com/"


def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{timestamp} - {message}")


def init_driver():
    chrome_options = Options()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    log_message("webdriver initialized.")
    return driver


from selenium.common.exceptions import NoSuchElementException


def login_twitter(driver, email, password):
    driver.get(twitter_url)
    log_message("Twitter page loaded.")

    wait = WebDriverWait(driver, 20)  # increased wait time
    try:
        sign_in_button_xpath = "/html/body/div/div/div/div[2]/main/div/div/div[1]/div/div/div[3]/div[5]/a/div/span/span"
        sign_in_button = wait.until(EC.element_to_be_clickable((By.XPATH, sign_in_button_xpath)))
        sign_in_button.click()
        log_message("Sign-in button clicked.")

        # list of potential selectors for the username input field
        selectors = [
            (By.XPATH, "//input[@name='session[username_or_email]']"),
            (By.CSS_SELECTOR, "input[autocomplete='username']"),
            (By.XPATH,
             "//*[@id='react-root']/div/div/div/main/div/div/div/div[2]/div[2]/div/div[5]/label/div/div[2]/div/input"),
            (
            By.XPATH, "/html/body/div/div/div/div/main/div/div/div/div[2]/div[2]/div/div[5]/label/div/div[2]/div/input")
        ]

        # try each selector until one works
        for by, value in selectors:
            try:
                email_field = wait.until(EC.presence_of_element_located((by, value)))
                break  # if the field is found, break out of the loop
            except (TimeoutException, NoSuchElementException):
                log_message(f"Failed to find email field using {by}='{value}'")

        email_field.send_keys(email)
        log_message("Email entered.")

        email_field.send_keys(Keys.RETURN)
        log_message("Email submitted.")

        time.sleep(2)

        # Layered Catch Mechanism for password field
        password_selectors = [
            (By.NAME, 'password'),
            (By.CSS_SELECTOR, 'input[type="password"][autocomplete="current-password"]'),
            (By.CSS_SELECTOR, '.r-30o5oe'),
            (By.XPATH, "//input[@autocomplete='current-password']"),
            (By.XPATH, "//input[@type='password']")
        ]


        # password field section:
        password_field = None
        for by, value in password_selectors:
            try:
                password_field = wait.until(EC.presence_of_element_located((by, value)))
                if password_field:
                    break
            except (NoSuchElementException, TimeoutException):
                log_message(f"Password field not found with {by}='{value}'")

        if password_field:
            password_field.send_keys(password)
            log_message("Password entered.")
            password_field.send_keys(Keys.RETURN)
            log_message("Login submitted.")
        else:
            log_message("Failed to find the password field with any method.")

    except Exception as e:
        log_message(f"An error occurred: {str(e)}")


def main():
    driver = init_driver()
    login_twitter(driver, TWITTER_EMAIL, TWITTER_PASSWORD)
    log_message("Browser will remain open until manually closed.")
    input("Press Enter to close the browser...")
    driver.quit()

if __name__ == "__main__":
    main()
