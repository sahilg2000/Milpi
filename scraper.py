from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from extractor import clean_event_data

URL = "https://sccl.bibliocommons.com/v2/events?q=Dungeons%20and%20Dragons&locations=MI"

def scrape_library():
    events = []
    with sync_playwright() as p:
        # launch a headless browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        print("Opening browser and loading library events...")
        page.goto(URL, wait_until="networkidle")

        # wait specifically for a title
        try:
            page.wait_for_selector(".cp-event-title", timeout=10000)
        except:
            print("Timed out waiting for page to load.")
            browser.close()
            return "The library site is lagging like a level 1 goblin. Try again in a minute."

        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')

        # main container - list of search results
        results = soup.find_all('div', class_='cp-events-search-item')

        print(f"\n--- FOUND {len(results)} EVENTS ---")
        for item in results:
            # get event title
            title_elem = item.find('div', class_='cp-event-title')
            title = title_elem.get_text(strip=True) if title_elem else "Unknown Title"
            
            # get date 
            date_text = item.find('span', class_='cp-event-date-time').get_text(strip=True)
            # print(f"Raw text; {date_text}")
            event_date, event_time = clean_event_data(date_text)
            
            # Get event URL
            link_elem = title_elem.find('a') if title_elem else None
            event_url = f"{link_elem['href']}" if link_elem else "No URL Found"

            events.append({
                "title": title,
                "date": event_date,
                "time": event_time,
                "url": event_url
            })
            print(f"⚔️  {title}")
            print(f"📅 {event_date} @ {event_time}")
            print(f"🔗  {event_url}")
            print("-" * 30)

        browser.close() 
        return events


if __name__ == "__main__":
    scrape_library()