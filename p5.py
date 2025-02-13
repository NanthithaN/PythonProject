from playwright.sync_api import sync_playwright

def scrape_p4():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  
        page = browser.new_page()
        
        try:
            print("Starting the scraping process for p5.py...")
            page.goto("https://www.kotaksecurities.com/stock-research-recommendations/equity/longterm/")  # Change to your target URL
            page.wait_for_selector("table", timeout=30000)

            data = page.inner_text("table")
            print("Extracted Data:", data)

            # Save to a file
            with open("kotak_stock_long.xlsx", "w", encoding="utf-8") as file:
                file.write(data)
            print("Data saved")

        except Exception as e:
            print(f"Error occurred in p5.py: {e}")

        finally:
            browser.close()
            print("Scraping process completed for p5.py.")

if __name__ == "__main__":
    scrape_p4()
