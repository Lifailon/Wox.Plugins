import requests
import webbrowser
from wox import Wox
from datetime import datetime

def search_npm(query):
    results = []
    if len(query.strip()) < 3:
        results.append({
            "Title": "Enter at least 3 characters for search",
            "SubTitle": "",
            "IcoPath": "logo.png"
        })
        return results
    if query:
        url = f"https://registry.npmjs.org/-/v1/search?text={query}"
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            if 'objects' in data:
                for item in data['objects']:
                    pkg = item['package']
                    updated_at = datetime.fromisoformat(pkg['date'].replace("Z", "+00:00"))
                    formatted_date = updated_at.strftime("%d.%m.%Y")
                    title = f"{pkg['name']} (Version: {pkg['version']} 🕐 Date: {formatted_date})"
                    subtitle = f"{pkg['description'] or 'No description available'}"
                    results.append({
                        "Title": title,
                        "SubTitle": subtitle,
                        "IcoPath": "logo.png",
                        "JsonRPCAction": {
                            "method": "openUrl",
                            "parameters": [pkg['links']['npm']],
                            "dontHideAfterAction": False
                        }
                    })
        else:
            results.append({
                "Title": data.get('message', 'Unknown error'),
                "SubTitle": '',
                "IcoPath": "err.png"
            })
    if not results:
        results.append({
            "Title": 'No results found',
            "SubTitle": '',
            "IcoPath": "err.png"
        })
    return results

class NpmSearch(Wox):
    def query(self, query):
        return search_npm(query)

    def openUrl(self, url):
        webbrowser.open(url)

if __name__ == "__main__":
    NpmSearch()