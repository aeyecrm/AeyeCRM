import requests
import os

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

    response = requests.post(host, json=payload, headers=headers)
    if response.status_code == 200:
        print("URLs successfully submitted to IndexNow.")
    else:
        print(f"Failed to submit URLs. Status code: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    # Use the provided API key and key location
    API_KEY = os.getenv("INDEXNOW_API_KEY", "dc7517d82d734358904c44b7a17f3122")
    KEY_LOCATION = "https://48132577.fs1.hubspotusercontent-na1.net/hubfs/48132577/Indexnow.txt"

    # List URLs you want to submit
    urls = [
        "https://www.aeyecrm.com/",
        "https://www.aeyecrm.com/ai-welcome",
        "https://www.aeyecrm.com/faq-salesforce-smb-family-business"
    ]

    submit_urls_to_indexnow(urls, API_KEY, KEY_LOCATION)