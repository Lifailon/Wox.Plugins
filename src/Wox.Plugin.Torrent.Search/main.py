import requests
from wox import Wox

providerList = {
    "1": "RuTracker",
    "2": "Kinozal",
    "3": "RuTor",
    "4": "NoNameClub"
}

def TorAPI(provider, query):
    results = []
    if provider and query:
        url = f"https://torapi.vercel.app/api/search/title/{provider}?query={query}&category=0&page=0"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for item in data:
                if provider == "rutracker":
                    endParam = f"Downloads: {item['Download_Count']}"
                else:
                    endParam = f"Comments: {item['Comments']}"
                title = f"{item['Name']}"
                subtitle = f"Date: {item['Date']} | Size: {item['Size']} | Seeds: {item['Seeds']} | Peers: {item['Peers']} | {endParam}"
                results.append({
                    "Title": title,
                    "SubTitle": subtitle,
                    "IcoPath": f"{provider}.png",
                    "JsonRPCAction": {
                        "method": "openUrl",
                        "parameters": [item['Url']],
                        "dontHideAfterAction": False
                    }
                })
        else:
            results.append({
                "Title": "Error retrieving data",
                "SubTitle": response.json().get('message', 'Unknown error'),
                "IcoPath": "err.png"
            })
    if not results:
        results.append({
            "Title": 'No results found',
            "SubTitle": '',
            "IcoPath": "err.png"
        })
    return results

class getProvider(Wox):
    def query(self, query):
        results = []
        # Если запрос пустой или не соответствует ключам в providerList, показываем список провайдеров
        if not query or query.split()[0] not in providerList.keys():
            for name in providerList:
                results.append({
                    "Title": name,
                    "SubTitle": f"Search on {providerList[name]}",
                    "IcoPath": f"{providerList[name].lower()}.png",
                    "JsonRPCAction": {
                        "parameters": [providerList[name]],
                        "dontHideAfterAction": True
                    }
                })
        else:
            provider, search_query = query.split(maxsplit=1)
            # Проверка на минимальное количество символов в поисковом запросе
            if len(search_query) < 3:
                results.append({
                    "Title": "Enter at least 3 characters to search",
                    "SubTitle": f"Search on {providerList[provider]}",
                    "IcoPath": f"{providerList[provider].lower()}.png"
                })
            else:
                results = TorAPI(providerList.get(provider).lower(), search_query)

        return results

    def openUrl(self, url):
        import webbrowser
        webbrowser.open(url)

if __name__ == "__main__":
    getProvider()