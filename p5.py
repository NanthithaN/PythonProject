from playwright.sync_api import sync_playwright
import pandas as pd
import os
import time

# URL to scrape
URL = "https://www.kotaksecurities.com/stock-research-recommendations/equity/longterm/"

# Excel file to save data
EXCEL_FILE = "kotak_stock_data.xlsx"

def scrape_and_save_data():
    print("Starting the scraping process...")

    try:
        with sync_playwright() as p:
            # Use persistent context to mitigate bot detection
            browser = p.chromium.launch_persistent_context(user_data_dir="/tmp/playwright", headless=True)
            page = browser.new_page()

            # Navigate to the URL
            page.goto(URL)
            print("Page loaded. Extracting data...")

            # Take a screenshot for debugging
            page.screenshot(path="debug.png")
            print("Screenshot taken. Check debug.png for UI verification.")

            # Wait for the table to be visible
            page.wait_for_selector("table", state="visible", timeout=120000)

            # Sleep to allow all elements to load
            time.sleep(5)

            # Extract table rows
            rows = []
            for row in page.query_selector_all("table tbody tr"):
                cells = [cell.inner_text().strip() for cell in row.query_selector_all("td")]

                if len(cells) >= 5:
                    row_data = {
                        "Company Name": cells[0],
                        "Reco. Price": cells[1],
                        "Target Price": cells[2],
                        "Stop Loss": cells[3],
                        "Market Price": cells[4]
                    }
                    rows.append(row_data)

            # Debugging: Print extracted rows
            print(f"Extracted {len(rows)} rows. Example row: {rows[0] if rows else 'No rows found'}")

            # Create a DataFrame
            df = pd.DataFrame(rows, columns=["Company Name", "Reco. Price", "Target Price", "Stop Loss", "Market Price"])

            # Ensure Excel file is not open
            if os.path.exists(EXCEL_FILE):
                try:
                    os.rename(EXCEL_FILE, EXCEL_FILE)
                except PermissionError:
                    print(f"Error: The file '{EXCEL_FILE}' is open. Please close it and run again.")
                    return
