import webbrowser
import requests
from wox import Wox

# Целевой язык перевода (по умолчанию русский)
LANGUAGE = 'ru'

def translate(query):
    query_modified = query.strip().lower()
    results = []

    if query_modified:
        # Массив из английских букв
        en = set(chr(i) for i in range(ord('a'), ord('z') + 1))
        # Определяем язык перевода (с английского на русский или наоборот)
        from_lang, to_lang = ('en', LANGUAGE) if query_modified[0] in en else (LANGUAGE, 'en')
        
        # Выполняем запрос к API MyMemory
        url_api = "https://api.mymemory.translated.net/get?q={query}&langpair={from_lang}|{to_lang}&mt=1"
        response = requests.get(url_api.format(query=query_modified, from_lang=from_lang, to_lang=to_lang))
        data = response.json()

        # Проверяем результат и добавляем его в список
        if 'matches' in data:
            for match in data['matches']:
                if match['translation']:
                    results.append({
                        "Title": match['translation'],
                        "SubTitle": f"Original: {match['segment']}",
                        "IcoPath": "logo.png",
                        "JsonRPCAction": {
                            'method': 'openUrl',
                            'parameters': [f'https://mymemory.translated.net/en/{from_lang}/{to_lang}/{(match["segment"].replace(" ", "-"))}'],
                            'dontHideAfterAction': False
                        }
                    })
    
    if not results:
        results.append({
            "Title": 'Translation not found',
            "SubTitle": '',
            "IcoPath": "logo.png"
        })

    return results

class Translate(Wox):
    def query(self, query):
        return translate(query)

    def openUrl(self, url):
        webbrowser.open(url)

if __name__ == "__main__":
    Translate()
