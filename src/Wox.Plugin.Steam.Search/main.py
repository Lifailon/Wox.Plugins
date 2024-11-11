import os
import requests
import webbrowser
from wox import Wox
from concurrent.futures import ThreadPoolExecutor

CACHE_DIR = "cache"
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

def download_icon(icon_url, icon_path):
    try:
        # Загружаем иконку, если её нет в кэше
        if icon_url and not os.path.isfile(icon_path):
            response = requests.get(icon_url, timeout=5)
            response.raise_for_status()
            # Сохраняем иконку в файл
            with open(icon_path, 'wb') as handler:
                handler.write(response.content)
        # Проверяем размер файла
        if os.path.isfile(icon_path):
            file_size = os.path.getsize(icon_path)
            if file_size > 1:
                return icon_path
            else:
                return "logo.png"
        else:
            return "logo.png"
    except (requests.RequestException, ValueError) as e:
        return "logo.png"

def search_steam(query):
    results = []
    if len(query.strip()) < 3:
        results.append({
            "Title": "Enter at least 3 characters for search",
            "SubTitle": "",
            "IcoPath": "logo.png"
        })
        return results
    
    if query:
        url = f"https://store.steampowered.com/api/storesearch/?term={query}&cc=us&l=en"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            if 'items' in data:
                # Создаем пул потоков для скачивания изображений
                with ThreadPoolExecutor() as executor:
                    future_to_item = {}
                    for item in data['items']:
                        title = item['name']
                        # Получение цены
                        price = item.get('price', {})
                        initial_price = price.get('initial', 0) / 100  
                        final_price = price.get('final', 0) / 100
                        subtitle = f"Full price: ${initial_price:.2f}, Final price: ${final_price:.2f}"
                        # Путь к файлу в кэше
                        icon_filename = f"{title.replace(' ', '_')}.png"
                        icon_path = os.path.join(CACHE_DIR, icon_filename)
                        # Если иконка уже есть в кэше, используем её
                        future = executor.submit(download_icon, item.get('tiny_image', ""), icon_path)
                        future_to_item[future] = {
                            "Title": title,
                            "SubTitle": subtitle,
                            "IcoPath": icon_path,
                            "JsonRPCAction": {
                                "method": "openUrl",
                                "parameters": [f"https://store.steampowered.com/app/{item['id']}"],
                                "dontHideAfterAction": False
                            }
                        }
                    # Ожидаем завершения всех потоков
                    for future in future_to_item:
                        icon_path = future.result()
                        item_data = future_to_item[future]
                        item_data["IcoPath"] = icon_path
                        results.append(item_data)

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

class SteamSearch(Wox):
    def query(self, query):
        return search_steam(query)

    def openUrl(self, url):
        webbrowser.open(url)

if __name__ == "__main__":
    SteamSearch()