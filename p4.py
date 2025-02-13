from playwright.sync_api import sync_playwright
from playwright_stealth import stealth 
import pandas as pd
import os
import time

# URL to scrape
URL = "https://www.kotaksecurities.com/stock-research-recommendations/equity/shortterm/"

# Excel file to save data
EXCEL_FILE = "kotak_stock_data.xlsx"

def scrape_and_save_data():
    print("Starting the scraping process...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        page = context.new_page()
        stealth(page)  # Apply stealth mode to avoid bot detection

        try:
            # Navigate to the page
            page.goto(URL, timeout=120000)
            print("Page loaded. Extracting data...")

            # Debugging Screenshot
            page.screenshot(path="debug.png")
            print("Screenshot taken. Check debug.png for UI verification.")

            # Wait until at least one table is visible
            page.wait_for_selector("table", state="visible", timeout=120000)

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

            # Debugging
            print(f"Extracted {len(rows)} rows. Example row: {rows[0] if rows else 'No rows found'}")

            # Create DataFrame
            df = pd.DataFrame(rows, columns=["Company Name", "Reco. Price", "Target Price", "Stop Loss", "Market Price"])

            # Ensure Excel file is not open
            if os.path.exists(EXCEL_FILE):
                try:
                    os.rename(EXCEL_FILE, EXCEL_FILE)
                except PermissionError:
                    print(f"Error: The file '{EXCEL_FILE}' is open. Please close it and run again.")
                    return

            # Save data to Excel
            with pd.ExcelWriter(EXCEL_FILE, mode="w") as writer:
                df.to_excel(writer, index=False, sheet_name="Stock Data")

            print("Data successfully saved in Excel.")
            browser.close()

        except Exception as e:
            print(f"Error occurred: {e}")
            browser.close()

# Run the scraper
scrape_and_save_data()
