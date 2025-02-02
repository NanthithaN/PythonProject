import time
from playwright.sync_api import sync_playwright
import os

def open_and_refresh():
    start_total_time = time.time()  # Start tracking the total time
    with sync_playwright() as p:
        # Check if running in CI environment (e.g., GitHub Actions)
        headless = os.getenv("CI", "false").lower() == "true"

        print("Launching browser...")
        launch_start_time = time.time()
        browser = p.chromium.launch(headless=headless)  # Use headless mode based on environment
        launch_end_time = time.time()
        print(f"Browser launched in {launch_end_time - launch_start_time} seconds.")

        page = browser.new_page()

        # Navigate to the webpage
        page.goto('https://www.hdfcsec.com/research/stock-market-ideas/investment-ideas?assetId=3&categoryCode=FUND&Sector=&RecoType=&CallType=OPEN&Target_Min=&Target_Max=&horizon_Max=&horizon_Min=&RecoDateRange=&BucketID=379&securityId=')  # Replace with your target URL
        print("Page loaded, refreshing every minute...")

        # Refresh the page every minute for 3 minutes (180 seconds)
        start_time = time.time()
        while time.time() - start_time < 180:  # Run for 3 minutes
            page.reload()  # Reload the page
            time.sleep(60)  # Wait 60 seconds (1 minute) before refreshing again

        # After 3 minutes, print a message and close the browser
        print("3 minutes passed, closing the browser.")
        browser.close()

    end_total_time = time.time()
    print(f"Total time taken for execution: {end_total_time - start_total_time} seconds.")

if __name__ == "__main__":
    open_and_refresh()
