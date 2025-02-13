from playwright.sync_api import sync_playwright
import pandas as pd
import os

# URL to scrape
URL = "https://www.kotaksecurities.com/stock-research-recommendations/equity/longterm/"

# Excel file to save data
EXCEL_FILE = "kotak_stock_data.xlsx"

def scrape_and_save_data():
    print("Starting the scraping process...")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # ✅ Open browser to debug
            page = browser.new_page()

            # Navigate to the URL & wait for full load
            page.goto(URL, wait_until="load", timeout=120000)
            print("Page loaded. Extracting data...")

            # Wait for table to be fully populated
            page.wait_for_selector("table", timeout=120000)
            page.wait_for_function("document.querySelector('table tbody tr') !== null", timeout=120000)

            # Extract table rows
            rows = []
            for row in page.query_selector_all("table tbody tr"):
                cells = [cell.inner_text().strip() for cell in row.query_selector_all("td")]

                # Ensure the row has enough columns
                if len(cells) >= 5:
                    row_data = {
                        "Company Name": cells[0],
                        "Reco. Price": cells[1],
                        "Target Price": cells[2],
                        "Stop Loss": cells[3],
                        "Market Price": cells[4]
                    }
                    rows.append(row_data)

            print(f"Extracted {len(rows)} rows.")

            # Save data only if rows are found
            if rows:
                df = pd.DataFrame(rows)

                # Ensure Excel file is not open
                if os.path.exists(EXCEL_FILE):
                    try:
                        os.rename(EXCEL_FILE, EXCEL_FILE)  # Check if file is open
                    except PermissionError:
                        print(f"Error: Close '{EXCEL_FILE}' and try again.")
                        return

                # Save to Excel
                with pd.ExcelWriter(EXCEL_FILE, mode="w", engine="openpyxl") as writer:
                    df.to_excel(writer, index=False, sheet_name="Stock Data")

                print(f"Data successfully saved to {EXCEL_FILE}.")
            else:
                print("No data found.")

            browser.close()

    except Exception as e:
        print(f"Error occurred: {e}")

# Run the function
scrape_and_save_data()
