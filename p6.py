import time
from playwright.sync_api import sync_playwright
import os

def open_and_refresh():
    with sync_playwright() as p:
        # Check if running in CI environment (e.g., GitHub Actions)
        headless = os.getenv("CI", "false").lower() == "true"

        # Launch browser, headless=True for CI and headless=False for local testing
        browser = p.chromium.launch(headless=headless)  # Use headless mode based on environment
        page = browser.new_page()

        # Navigate to the webpage
        page.goto('https://www.hdfcsec.com/research/stock-market-ideas/investment-ideas?assetId=3&categoryCode=FUND&Sector=&RecoType=&CallType=OPEN&Target_Min=&Target_Max=&horizon_Max=&horizon_Min=&RecoDateRange=&BucketID=379&securityId=')  # Replace with your target URL

        # Print to confirm the page is loaded
        print("Page loaded, refreshing every 5 seconds...")

        # Refresh the page every 5 seconds for 10 minutes (600 seconds)
        start_time = time.time()
        while time.time() - start_time < 600:  # Run for 10 minutes
            page.reload()  # Reload the page
            time.sleep(5)  # Wait 5 seconds before refreshing again (adjust as necessary)

        # After 10 minutes, print a message and close the browser
        print("10 minutes passed, closing the browser.")
        browser.close()

if __name__ == "__main__":
    open_and_refresh()
