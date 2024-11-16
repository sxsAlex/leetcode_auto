from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import logging
import json
import urllib.parse
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

logging.info("Script started.")

# Replace with your LeetCode credentials
load_dotenv()


app = Flask(__name__)
CORS(app)  # Allow all origins

@app.route("/")
def home():
    return "Home page"

@app.route("/trigger_script", methods=["POST"])
def trigger_script():
    print("script is triggered")
    # Get the problem text from the request
    data = request.get_json()
    solution_text = data.get("solution")

    if not solution_text:
        return jsonify({"error": "No problem text provided"}), 400

    try:
        print("solution:" + solution_text)
        chrome_options = Options()
        #chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36")
        chrome_options.add_argument("--headless")  # Run in headless mode if you don't want to see the browser
        #service = Service("D:\Program Files (x86)\\repos\leetcode\leetcode_auto\chromedriver-win64\chromedriver.exe")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        print("Launching browser...")
        # Launch browser
        #driver = webdriver.Chrome(service=service, options=chrome_options)
        print("opening leetcode...")
        driver.get("https://leetcode.com")
        time.sleep(5)
        
        print("loading cookies...")

        raw_cookies = os.getenv('RAW_COOKIES')
        cookies_list = raw_cookies.split(';')
        # Add cookies to the browser session
        # Add each cookie to the Selenium driver
        for cookie in cookies_list:
            cookie = cookie.strip()  # Remove any extra spaces
            cookie_name, cookie_value = cookie.split('=', 1)  # Split on the first '='

            # Add cookie to Selenium session
            driver.add_cookie({
                'name': cookie_name,
                'value': cookie_value,
                'domain': 'leetcode.com',  # Make sure this matches the domain
                'path': '/',  # Set to root path, or specify the path if needed
                'secure': True  # If the cookie is secure (https), set to True
            })

        # Reload the page to activate the session
        driver.refresh()

        print("opening the problem")
        # Go to the daily challenge
        driver.get("https://leetcode.com/problems/add-two-numbers/")
        time.sleep(3)

        # # Open the problem
        # daily_link = driver.find_element(By.CLASS_NAME, "daily-question").get_attribute("href")
        # driver.get(daily_link)
        # time.sleep(3)

        # Paste solution
        driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/div[4]/div/div/div[8]/div/div[1]/div[1]/div[1]/div/div/div[1]/div/button").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/div[4]/div/div/div[8]/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div/div[1]/div[6]").click()
        time.sleep(1)
        code_editor = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/div[4]/div/div/div[8]/div/div[2]/div[1]/div/div/div[1]/textarea")
        code_editor.click()
        time.sleep(1)
        code_editor.send_keys(Keys.CONTROL + "a")  # Select all
        code_editor.send_keys(Keys.DELETE)  # Clear existing code
        code_editor.send_keys(solution_text)  # Paste solution
        time.sleep(15)

        print("submitting solution")

        # # Submit solution
        # driver.find_element(By.CLASS_NAME, "submit__2ISl").click()
        # time.sleep(5)

        driver.quit()
        return jsonify({"message": "Script executed successfully!"})


    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
