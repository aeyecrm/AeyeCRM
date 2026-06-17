import requests
import os
import xml.etree.ElementTree as ET

# -----------------------------------------------------------------------------
# Extra URLs not auto-included in HubSpot's sitemap.xml.
# HubSpot Starter excludes Marketing Landing Pages from sitemap.xml,
# so we hard-code them here. Add new landing pages to this list as you build them.
# -----------------------------------------------------------------------------
EXTRA_LANDING_PAGES = [
    "https://aeyecrm.com/crm-services/industries/family-business",
    "https://aeyecrm.com/crm-services/industries/manufacturing",
    "https://aeyecrm.com/crm-services/industries/wholesale-distribution",
    "https://aeyecrm.com/crm-services/industries/retail",
    "https://aeyecrm.com/crm-services/industries/saas",
    "https://aeyecrm.com/crm-services/industries/professional-services",
    "https://aeyecrm.com/crm-services/industries/other",
]


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
        "host": "aeyecrm.com",
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
        elif response.status_code == 202:
            print(f"URLs accepted by IndexNow (202). ({len(url_list)} URLs)")
        else:
            print(f"Failed to submit URLs. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")


if __name__ == "__main__":
    API_KEY = os.getenv("INDEXNOW_API_KEY", "dc7517d82d734358904c44b7a17f3122")
    KEY_LOCATION = "https://aeyecrm.com/dc7517d82d734358904c44b7a17f3122.txt"
    SITEMAP_URL = "https://www.aeyecrm.com/sitemap.xml"
    BATCH_SIZE = 1000

    # 1. Pull everything from the official sitemap
    sitemap_urls = fetch_urls_from_sitemap(SITEMAP_URL)
    print(f"Found {len(sitemap_urls)} URLs in sitemap.")

    # 2. Add the manually-tracked landing pages (dedupe)
    all_urls = list(dict.fromkeys(sitemap_urls + EXTRA_LANDING_PAGES))
    extras_added = len(all_urls) - len(sitemap_urls)
    print(f"Added {extras_added} extra landing pages not in sitemap.")
    print(f"Total URLs to submit: {len(all_urls)}.")

    if not all_urls:
        print("No URLs found. Check sitemap URL or provide alternative URL source.")
    else:
        for i in range(0, len(all_urls), BATCH_SIZE):
            batch = all_urls[i:i + BATCH_SIZE]
            submit_urls_to_indexnow(batch, API_KEY, KEY_LOCATION)
