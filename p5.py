from playwright.sync_api import sync_playwright
import pandas as pd
import os

URL = "https://www.kotaksecurities.com/stock-research-recommendations/equity/longterm/"
EXCEL_FILE = "kotak_stock_data.xlsx"

def scrape_and_save_data():
    print("Starting the scraping process for p5.py...")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)  # Ensure headless mode
            page = browser.new_page()

            page.goto(URL, timeout=90000)  # Increased timeout
            print("Page loaded. Extracting data...")

            tables = page.query_selector_all("table")

            if len(tables) == 0:
                print("Error: No table found on the page.")
                return

            print(f"Found {len(tables)} tables, selecting the first relevant one.")

            target_table = tables[0]  # Pick the correct table

            rows = []
            for row in target_table.query_selector_all("tbody tr"):
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

            if rows:
                print(f"Extracted {len(rows)} rows.")

            df = pd.DataFrame(rows, columns=["Company Name", "Reco. Price", "Target Price", "Stop Loss", "Market Price"])

            if os.path.exists(EXCEL_FILE):
                try:
                    os.rename(EXCEL_FILE, EXCEL_FILE)  # Ensure file is not open
                except PermissionError:
                    print(f"Error: The file '{EXCEL_FILE}' is open. Close it and try again.")
                    return

            with pd.ExcelWriter(EXCEL_FILE, mode="a", if_sheet_exists="replace") as writer:
                df.to_excel(writer, index=False, sheet_name="Long Term")

            print("Data saved successfully.")
            browser.close()

    except Exception as e:
        print(f"Error occurred in p5.py: {e}")

    print("Scraping process completed for p5.py.")

scrape_and_save_data()