import requests
import subprocess
from wox import Wox

def check_grammar(text):
    results = []
    if len(text.strip()) < 5:
        results.append({
            "Title": "Enter at least 5 characters for check grammar",
            "SubTitle": "",
            "IcoPath": "logo.png"
        })
        return results
    if text:
        url_api = 'https://api.languagetoolplus.com/v2/check'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }
        data = {
            'text': text,
            'language': 'auto',
            'enabledOnly': 'false'
        }
        response = requests.post(url_api, headers=headers, data=data)
        data = response.json()
        if response.status_code == 200:
            if 'matches' in data and data['matches']:
                matches = data['matches']
                for match in matches:
                    replacements = [replacement['value'] for replacement in match['replacements']]
                    if replacements:
                        context = match['context']
                        error_word = context['text'][context['offset']:context['offset'] + context['length']]
                        for replacement in replacements:
                            results.append({
                                "Title": replacement,
                                "SubTitle": f'Source word: {error_word}',
                                "IcoPath": "logo.png",
                                "JsonRPCAction": {
                                    "method": "copyToClipboard",
                                    "parameters": [replacement],
                                    "dontHideAfterAction": True
                                }
                            })
            else:
                results.append({
                    "Title": "No grammar issues found",
                    "SubTitle": '',
                    "IcoPath": "logo.png"
                })
        else:
            error_message = data.get('message', 'Unknown error')
            results.append({
                "Title": error_message,
                "SubTitle": '',
                "IcoPath": "logo.png"
            })
    return results

class GrammarCheck(Wox):
    def query(self, query):
        return check_grammar(query)

    def copyToClipboard(self, text):
        process = subprocess.Popen('clip', stdin=subprocess.PIPE, shell=True)
        process.communicate(input=text.encode('utf-16'))

if __name__ == "__main__":
    GrammarCheck()