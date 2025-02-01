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
            browser = p.chromium.launch(headless=True)  # Use Chromium browser
            page = browser.new_page()

            # Navigate to the URL
            page.goto(URL)
            print("Page loaded. Extracting data...")

            # Wait for the table to load completely
            page.wait_for_selector("table")

            # Extract table rows
            rows = []
            for row in page.query_selector_all("table tbody tr"):
                cells = [cell.inner_text().strip() for cell in row.query_selector_all("td")]

                # Ensure the row has enough columns to extract
                if len(cells) >= 5:
                    row_data = {
                        "Company Name": cells[0],  # Company name
                        "Reco. Price": cells[1],   # Recommendation price
                        "Target Price": cells[2],  # Target price
                        "Stop Loss": cells[3],     # Stop loss
                        "Market Price": cells[4]   # Current market price
                    }
                    rows.append(row_data)

            # Debugging: Print extracted rows
            print(f"Extracted {len(rows)} rows. Example row: {rows[0] if rows else 'No rows found'}")

            # Create a DataFrame
            df = pd.DataFrame(rows, columns=["Company Name", "Reco. Price", "Target Price", "Stop Loss", "Market Price"])

            # Check if the file exists and close it if open
            if os.path.exists(EXCEL_FILE):
                try:
                    os.rename(EXCEL_FILE, EXCEL_FILE)  # Try renaming to check if it's open
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

# Call the function to scrape data
scrape_and_save_data()
