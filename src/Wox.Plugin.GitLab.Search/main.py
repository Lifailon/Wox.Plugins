import requests
import webbrowser
from wox import Wox
from datetime import datetime

def search_gitlab(query):
    results = []
    if len(query.strip()) < 3:
        results.append({
            "Title": "Enter at least 3 characters for search",
            "SubTitle": "",
            "IcoPath": "logo.png"
        })
        return results

    if query:
        url = f"https://gitlab.com/api/v4/projects?search={query}"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            if isinstance(data, list) and data:
                for item in data:
                    #updated_at = datetime.fromisoformat(item['updated_at'].replace("Z", "+00:00"))
                    #formatted_date = updated_at.strftime("%H:%M %d.%m.%Y")
                    #title = f"{item['name']} (⭐ Stars: {item['star_count']} ⌚📅 Update: {formatted_date})"
                    #title = f"{item['name']} (⭐ Stars: {item['star_count']} ⌚📅 Update: {item['updated_at']})"
                    title = f"{item['name']} (⭐ Stars: {item['star_count']})"
                    subtitle = f"{item['description'] or 'No description available'}"
                    results.append({
                        "Title": title,
                        "SubTitle": subtitle,
                        "IcoPath": "logo.png",
                        "JsonRPCAction": {
                            "method": "openUrl",
                            "parameters": [item['web_url']],
                            "dontHideAfterAction": False
                        }
                    })
            else:
                results.append({
                    "Title": data.get('message', 'Unknown error'),
                    "SubTitle": '',
                    "IcoPath": "err.png"
                })
        else:
            results.append({
                "Title": 'No results found',
                "SubTitle": '',
                "IcoPath": "err.png"
            })
    return results

class GitlabSearch(Wox):
    def query(self, query):
        return search_gitlab(query)

    def openUrl(self, url):
        webbrowser.open(url)

if __name__ == "__main__":
    GitlabSearch()