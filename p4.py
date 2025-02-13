from playwright.sync_api import sync_playwright
import pandas as pd
import os

URL = "https://www.kotaksecurities.com/stock-research-recommendations/equity/shortterm/"
EXCEL_FILE = "kotak_stock_data.xlsx"

def scrape_and_save_data():
    print("Starting the scraping process...")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)  # Headless mode for GitHub
            page = browser.new_page()

            page.goto(URL, timeout=90000)  # Increase timeout for slow loading
            print("Page loaded. Extracting data...")

            tables = page.query_selector_all("table")

            if len(tables) == 0:
                print("Error: No table found on the page.")
                return

            print(f"Found {len(tables)} tables, selecting the first relevant one.")

            target_table = tables[0]  # Pick the correct one based on index or refine selector

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
                    os.rename(EXCEL_FILE, EXCEL_FILE)  # Ensure the file is not open
                except PermissionError:
                    print(f"Error: The file '{EXCEL_FILE}' is open. Close it and try again.")
                    return

            with pd.ExcelWriter(EXCEL_FILE, mode="w") as writer:
                df.to_excel(writer, index=False, sheet_name="Short Term")

            print("Data saved successfully.")
            browser.close()

    except Exception as e:
        print(f"Error occurred: {e}")

scrape_and_save_data()
