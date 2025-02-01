from playwright.sync_api import sync_playwright
import pandas as pd
import os

# URL to scrape
URL = "https://trendlyne.com/research-reports/all/?"

# Excel file to save data
EXCEL_FILE = "f1.xlsx"

def scrape_and_save_data():
    print("Starting the scraping process...")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)  # Use Chromium browser
            page = browser.new_page()

            # Navigate to the URL
            page.goto(URL)
            print("Page loaded. Extracting data...")

            # Wait for the table to load completely
            page.wait_for_selector("table")

            # Extract table headers (first 8 columns)
            headers = [
                "DATE", "STOCK", "AUTHOR", "LTP", "TARGET",
                "PRICE AT RECO (CHANGE SINCE RECO%)", "UPSIDE(%)", "TYPE"
            ]
            print(f"Headers: {headers}")

            # Extract table rows
            rows = []
            for row in page.query_selector_all("table tbody tr"):
                cells = [cell.inner_text().strip() for cell in row.query_selector_all("td")]

                # Ensure that the row has at least 9 cells
                if len(cells) >= 9:
                    row_data = {
                        "DATE": cells[1],
                        "STOCK": cells[2],
                        "AUTHOR": cells[3],
                        "LTP": cells[4],
                        "TARGET": cells[5],
                        "PRICE AT RECO (CHANGE SINCE RECO%)": cells[6],
                        "UPSIDE(%)": cells[7],
                        "TYPE": cells[8]
                    }
                    rows.append(row_data)

            # Debugging: Print extracted rows
            print(f"Extracted {len(rows)} rows. Example row: {rows[0] if rows else 'No rows found'}")

            # Create a DataFrame
            df = pd.DataFrame(rows, columns=headers)

            # Check if the file exists and close it if open
            if os.path.exists(EXCEL_FILE):
                try:
                    os.rename(EXCEL_FILE, EXCEL_FILE)  # Try renaming to check if it's open
                except PermissionError:
                    print(f"Error: The file '{EXCEL_FILE}' is open. Please close it and run again.")
                    return

            # Save data to Excel (append if the file exists)
            with pd.ExcelWriter(EXCEL_FILE, mode="a", if_sheet_exists="replace") as writer:
                df.to_excel(writer, index=False, sheet_name="Sheet1")

            print("Data successfully updated in Excel.")

            browser.close()
    except Exception as e:
        print(f"Error occurred: {e}")

# Call the function to scrape data
scrape_and_save_data()
