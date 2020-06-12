from googlesearch import search
import requests
from bs4 import BeautifulSoup
from random import choice


def google(query):
    for r in search(query, tld='ca', lang='en', num=1, start=0, stop=1, pause=2.0):
        return r


def translate(query, target):
    url = "https://systran-systran-platform-for-language-processing-v1.p.rapidapi.com" \
          "/translation/text/translate"
    querystring = {"source": "auto", "target": target, "input": query}
    headers = {
        'x-rapidapi-host': "systran-systran-platform-for-language-processing-v1.p.rapidapi.com",
        'x-rapidapi-key': "8bef51c08bmsh96dc3702341e39ep14a15bjsn19a83064d62d"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    try:
        result = response.json()['outputs'][0]['output']
    except:
        result = ""
    return result


def wiki(query):
    link = "https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={}&prop=info&inprop=url&format=json"\
        .format(query.replace(" ", "_"))
    result = requests.get(link).json()['query']['search'][0]
    title = result['title']
    pid = result['pageid']
    info = requests.get("https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts"
                        "&exintro&explaintext&redirects=1&titles={}".format(title)).json()
    extract = info['query']['pages'][str(pid)]['extract']
    if "\n" in extract:
        extract = extract[:extract.find("\n")]
        extract += "..."
    while len(extract) > 1500:
        extract = extract[:extract.rfind(" ")]
        extract += "..."
    return extract


def weather(city="Burnaby"):
    url = "http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&APPID=6f68045e525e16f8232fb0e5f19987c4"\
        .format(city.replace(" ", "%20"))
    jsonurl = requests.get(url)
    info = jsonurl.json()
    response_text = "Weather for " + info['city']['name'] + ", " + info['city']['country']
    list = info['list'][0]
    response_text += ("\nTime: " + str(list['dt_txt']) +
                      "\nForecasted condition: " + str(list['weather'][0]['description']) +
                      "\nForecasted temperature: " + str(list['main']['temp']) + "ºC"
                      "\nFeels like: " + str(list['main']['feels_like']) + "ºC"
                      "\nMaximum temperature: " + str(list['main']['temp_max']) + "ºC"
                      "\nMinimum temperature: " + str(list['main']['temp_min']) + "ºC")
    try:
        link = "https://www.theweathernetwork.com/ca/search?q="
        link += city.replace(" ", "%20")
        webpage = requests.get(link)
        text = str(BeautifulSoup(webpage.text, 'html.parser').find("li", class_="result"))
        h = text.find("href")
        e = text[h:].find(">")
        r = text[h:h + e]
        link = "https://www.theweathernetwork.com" + r[6:-1]
        response_text += "\nMore info at " + link
    except:
        pass
    return response_text


def news(country):
    codes = {
        'argentina': "ar", 'australia': "au", 'austria': "at", 'belgium': "be", 'brazil': "br",
        'bulgaria': 'bg', 'canada': 'ca', 'china': "cn", 'colombia': "co", 'cuba': "cu",
        'czech republic': "cz", 'egypt': "eg", 'france': "fr", 'germany': "de", 'greece': "gr",
        'hong kong': "hk", 'hungary': "hu", 'india': "in", 'indonesia': "id", 'ireland': "ie",
        'israel': "il", 'italy': "it", 'japan': "jp", 'latvia': "lv", 'lithuania': "lt",
        'malaysia': "my", 'mexico': "mx", 'morocco': "ma", 'netherlands': "nl", 'new zealand': "nz",
        'nigeria': "ng", 'norway': "no", "phillipines": "ph", 'poland': "pl", 'portugal': "pt",
        'romania': "ro", 'russia': "ru", 'saudi arabia': "sa", 'serbia': "rs", 'singapore': "sg",
        'slovakia': "sk", 'slovenia': "si", 'south africa': "za", 'south korea': "kr",
        'sweden': "se", 'switzerland': "ch", 'taiwan': "tw", 'thailand': "th", 'turkey': "tr",
        'uae': "ae", 'united arab emirates': "ae", 'ukraine': "ua", 'united kingdom': "gb",
        'uk': "gb", 'united states': "us", 'venezuela': "ve"
    }
    if country == "":
        url = "https://newsapi.org/v2/top-headlines?language=en&apiKey=620bb40ce29b4ba6877ca164e3b9f008"
    elif country.lower() in codes:
        url = "https://newsapi.org/v2/top-headlines?country={}&language=en&apiKey=620bb40ce29b4ba6877ca164e3b9f008" \
            .format(codes[country.lower()])
    else:
        url = "https://newsapi.org/v2/top-headlines?country={}&language=en&apiKey=620bb40ce29b4ba6877ca164e3b9f008" \
            .format(country.lower())
    try:
        json = requests.get(url).json()['articles']
        info = choice(json)
        response_text = "Here is your headline!\n" + info['title'] + "\n" + info['url']
    except:
        response_text = ("Unable to find specified country. Supported countries and "
                         "their codes can be found at https://newsapi.org/sources.")
    return response_text
