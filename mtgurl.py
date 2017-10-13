import requests

r = requests.get('http://gatherer.wizards.com/Pages/Search/Default.aspx?name=%2b%5bSynod%20Sanctum%5d')
print(r.status_code)

with open('toto.html', 'w') as file_:
    file_.write(r.text)
