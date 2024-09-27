import requests
from wox import Wox

def search_github(query):
    results = []
    if query:
        url = f"https://api.github.com/search/repositories?q={query}"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            if 'items' in data:
                for item in data['items']:
                    title = f"{item['name']} (Language: {item['language']} ⭐ Stars: {item['stargazers_count']})"
                    subtitle = f"{item['description'] or 'No description available'}"
                    results.append({
                        "Title": title,
                        "SubTitle": subtitle,
                        "IcoPath": "logo.png",
                        "JsonRPCAction": {
                            "method": "openUrl",
                            "parameters": [item['html_url']],
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

class GithubSearch(Wox):
    def query(self, query):
        return search_github(query)

    def openUrl(self, url):
        import webbrowser
        webbrowser.open(url)

if __name__ == "__main__":
    GithubSearch()
