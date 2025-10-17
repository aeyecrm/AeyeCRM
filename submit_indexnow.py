import requests
import os
import xml.etree.ElementTree as ET

def fetch_urls_from_sitemap(sitemap_url):
    """Parse XML sitemap and extract <loc> URLs."""
    try:
        response = requests.get(sitemap_url, timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        urls = [elem.text for elem in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        return [url for url in urls if "aeyecrm.com" in url]  # Filter to your domain
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return []

def submit_urls_to_indexnow(url_list, api_key, key_location, host="https://api.indexnow.org/indexnow"):
    payload = {
        "host": "www.aeyecrm.com",
        "key": api_key,
        "keyLocation": key_location,
        "urlList": url_list
    }
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    try:
        response = requests.post(host, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            print(f"URLs successfully submitted to IndexNow. ({len(url_list)} URLs)")
        else:
            print(f"Failed to submit URLs. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    # Use the provided API key and key location
    API_KEY = os.getenv("INDEXNOW_API_KEY", "dc7517d82d734358904c44b7a17f3122")
    KEY_LOCATION = "https://aeyecrm.com/dc7517d82d734358904c44b7a17f3122.txt"
    SITEMAP_URL = "https://www.aeyecrm.com/sitemap.xml"  # Your sitemap URL
    BATCH_SIZE = 1000  # URLs per submission (adjust as needed)

    # Fetch URLs from sitemap instead of hardcoding
    urls = fetch_urls_from_sitemap(SITEMAP_URL)
    print(f"Found {len(urls)} URLs in sitemap.")

    if not urls:
        print("No URLs found. Check sitemap URL or provide alternative URL source.")
    else:
        for i in range(0, len(urls), BATCH_SIZE):
            batch = urls[i:i + BATCH_SIZE]
            submit_urls_to_indexnow(batch, API_KEY, KEY_LOCATION)
