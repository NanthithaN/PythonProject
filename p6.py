from playwright.sync_api import sync_playwright
import time

# Constants
VIEW_TIME = 7 * 60 * 60  # 7 hours in seconds
REFRESH_INTERVAL = 6 * 60 * 60  # 6 hours in seconds

def open_and_refresh():
    print("Opening the webpage and setting up auto-refresh...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Keep browser visible
        page = browser.new_page()

        start_time = time.time()  # Track start time

        while time.time() - start_time < VIEW_TIME:
            print("Loading the page...")
            page.goto("https://www.hdfcsec.com/research/stock-market-ideas/investment-ideas?assetId=3&categoryCode=FUND&Sector=&RecoType=&CallType=OPEN&Target_Min=&Target_Max=&horizon_Max=&horizon_Min=&RecoDateRange=&BucketID=379&securityId=")
            page.wait_for_load_state("networkidle")

            print("Page loaded successfully. Waiting for next refresh...")

            # Wait for the refresh interval but ensure we don't exceed VIEW_TIME
            remaining_time = VIEW_TIME - (time.time() - start_time)
            sleep_time = min(REFRESH_INTERVAL, remaining_time)
            time.sleep(sleep_time)

        print("Closing browser after 7 hours.")
        browser.close()

# Run the function
open_and_refresh()
