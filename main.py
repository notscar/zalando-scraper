import cfscrape
import json
import time
import colorama
from datetime import datetime
from bs4 import BeautifulSoup

colorama.init()

REQUESTS_MANAGER = cfscrape.CloudflareScraper()
GET = REQUESTS_MANAGER.get
POST = REQUESTS_MANAGER.post
JSON_TO_TABLE = json.loads
TABLE_TO_JSON = json.dumps
COLOR = colorama.Fore

DISCORD_BASIC_LOGGING = False

LOGGING_WEBHOOK = 'https://discord.com/api/webhooks/895430214337826857/45aGFTs_MJLmRT7Vtv23BDEGXxO8iwsoCoFlRB5OAVvsK9y2gv3mPCFIEXLA9FNIiYQT'

WEBHOOKS = [
    # You can add as many webhooks as u want, diving them with ","
    'https://discord.com/api/webhooks/895422954404466790/UZZmbfvqnXjZCTqPc4Dt1vHuWifW4BD4IA6sPvPXXCiUj_SM0R6L56I31XB2r6R9POpb',
]

COUNTRY_LINKS = {
    'IT': 'https://www.zalando.it/release-calendar/sneakers-uomo/',
    'UK': 'https://www.zalando.co.uk/release-calendar/mens-shoes-sneakers/'
}

COUNTRY_BASE_URL = {
    'IT': 'https://www.zalando.it/',
    'UK': 'https://www.zalando.co.uk/'
}

LOGGING_COLORS = {
    "INFO": COLOR.CYAN,
    "LOG": COLOR.BLUE,
    "WARNING": COLOR.YELLOW,
    "ERROR": COLOR.RED,
}


def log(logType, message, details):
    logDate = str(datetime.now())

    logFile = open('logs.log', 'a+')

    if len(details) == 0:
        logFile.write(logDate + ' [%s] ' % (logType) + message + '\n')
        print(logDate + LOGGING_COLORS[logType] + ' [%s] ' %
              (logType) + message + COLOR.RESET)
    else:
        logFile.write(logDate + ' [%s] ' % (logType) +
                      message + ' | ' + TABLE_TO_JSON(details) + '\n')
        print(logDate + LOGGING_COLORS[logType] + ' [%s] ' %
              (logType) + message + ' | ' + TABLE_TO_JSON(details) + COLOR.RESET)

    logFile.close()

    detailsString = ''

    if (logType == 'LOG') and (DISCORD_BASIC_LOGGING == False):
        return

    for x in details:
        detailsString += '`%s = %s`\n' % (str(x), details[x])

    data = {
        "content": None,
        "embeds": [
            {
                "color": None,
                "fields": [
                    {
                        "name": "LOG TYPE",
                        "value": "`%s`" % (logType)
                    },
                    {
                        "name": "LOG MESSAGE",
                        "value": "`%s`" % (message)
                    },
                    {
                        "name": "LOG DETAILS",
                        "value": detailsString
                    },
                    {
                        "name": "TIME",
                        "value": "`%s`" % (logDate)
                    }
                ]
            }
        ],
        "username": "Zalando Scraper Logs",
        "avatar_url": "https://avatars.githubusercontent.com/u/1564818?s=280&v=4"
    }

    if len(details) == 0:
        data['embeds'][0]['fields'].remove(data['embeds'][0]['fields'][2])

    POST(LOGGING_WEBHOOK, json=data)


def save_external_articles(content):
    file = open('articles.json', 'w+')
    file.write(TABLE_TO_JSON(content))
    file.close()
    return content


def load_external_articles():
    open('articles.json', 'a+')
    file = open('articles.json', 'r')
    fileContent = file.read()
    if len(fileContent) < 2:
        save_external_articles([])
        return []
    try:
        file.close()
        return JSON_TO_TABLE(fileContent)
    except:
        save_external_articles([])
        return []


def validate_country(countryCode):
    return not (COUNTRY_LINKS[countryCode] == None)


def get_page_data(countryCode):

    if validate_country(countryCode):
        response = GET(COUNTRY_LINKS[countryCode])
        if response.status_code == 200:
            return response.content
        else:
            log('ERROR', 'Error while retrieving page',
                {'statusCode': response.status_code})
            return {'error': 'Invalid Status Code', 'status_code': response.status_code}
    log('ERROR', 'Invalid Country (get_page_data)',
        {'countryCode': countryCode})
    return {'error': 'Invalid Country'}


def filter_json(content):
    bs = BeautifulSoup(content, 'html.parser')
    foundScripts = bs.find_all('script')

    for script in foundScripts:
        if len(script.contents) == 1:
            if script.contents[0].startswith('window.feedPreloadedState='):
                script = script.contents[0]
                script = script[26:]
                script = script[:-1]
                return JSON_TO_TABLE(script)['feed']['items']


def filter_articles(content):
    for articlesList in content:
        if articlesList['id'] == 'products':
            return articlesList['articles']


def filter_coming_soon(content):
    comingSoonList = []
    for article in content:
        if article['availability']['comingSoon'] == True:
            comingSoonList.append(article)
    return comingSoonList


def adjust_articles_info(content, countryCode):
    adjustedArticlesList = []
    for article in content:
        articleInfo = {}
        rSplit = article['availability']['releaseDate'].split(' ')
        rDate = rSplit[0].split('-')
        rTime = rSplit[1]
        articleInfo['zalandoId'] = article['id']
        articleInfo['releaseDate'] = '%s-%s-%s %s' % (
            rDate[2], rDate[1], rDate[0], rTime)
        articleInfo['productName'] = article['brand'] + ' ' + article['name']
        articleInfo['originalPrice'] = article['price']['original']
        articleInfo['currentPrice'] = article['price']['current']
        articleInfo['link'] = "%s%s.html" % (
            COUNTRY_BASE_URL[countryCode], article['urlKey'])
        articleInfo['imageUrl'] = article['imageUrl']

        adjustedArticlesList.append(articleInfo)

    return adjustedArticlesList


def compare_articles(articles):
    if len(oldArticles) == 0:
        return articles
    else:
        if len(articles) == len(oldArticles):
            return []
        else:
            articlesToReturn = []
            for article in articles:
                found = False

                for article_ in oldArticles:

                    if article['zalandoId'] == article_['zalandoId']:
                        found = True

                if found == False:
                    articlesToReturn.append(article)

            return articlesToReturn


def get_product_stock(link):
    response = GET(link)
    bs = BeautifulSoup(response.content, 'html.parser')
    sizeArray = []
    try:
        sizeArray = JSON_TO_TABLE(bs.find("script", {'id': 'z-vegas-pdp-props'}).contents[0][9:-3])['model']['articleInfo']['units']
    except:
        log('ERROR','Could not retrieve model units and sizes',{'URL' : link})

    sizeStockArray = []
    for x in sizeArray:
        sizeStockArray.append({
            'size': x['size']['local'],
            'sizeCountry': x['size']['local_type'],
            'stock': x['stock']
        })

    return sizeStockArray


def send_message(content):

    for article in content:

        stocks = get_product_stock(article['link'])

        sizeString = ''
        countryString = ''
        stockString = ''
        totalStock = 0

        for size in stocks:
            sizeString += size['size'] + '\n'
            countryString += size['sizeCountry'] + '\n'
            stockString += str(size['stock']) + '\n'
            totalStock += size['stock']

        data = {
            "content": None,
            "embeds": [
                {
                    "description": "[%s](%s)" % (article['productName'], article['link']),
                    "color": None,
                    "fields": [
                        {
                            "name": "Price",
                            "value": article['currentPrice'],
                            "inline": True
                        },
                        {
                            "name": "Release Date",
                            "value": article['releaseDate'],
                            "inline": True
                        },
                        {
                            "name": "Total Stock",
                            "value": totalStock,
                            "inline": True
                        }
                    ],
                    "author": {
                        "name": "Sneaker Drop",
                        "url": article['link']
                    },
                    "thumbnail": {
                        "url": article['imageUrl']
                    }
                },
                {
                    "color": None,
                    "fields": [
                        {
                            "name": "Sizes",
                            "value": sizeString,
                            "inline": True
                        },
                        {
                            "name": "Country",
                            "value": countryString,
                            "inline": True
                        },
                        {
                            "name": "Stock",
                            "value": stockString,
                            "inline": True
                        }
                    ]
                }
            ],
            "username": "᲼",
            "avatar_url": "https://avatars.githubusercontent.com/u/1564818?s=280&v=4"
        }

        if len(stocks) == 0:
            data['embeds'].remove(data['embeds'][1])
            data['embeds'][0]['fields'][2]['value'] = 'UNKNOWN'

        for webhook in WEBHOOKS:

            log('LOG', 'Article Message Sent', {
                'WEBHOOK': webhook, 'ARTICLE-ID': article['zalandoId']})
            POST(webhook, json=data)


oldArticles = load_external_articles()


def main():
    global oldArticles
    country = 'IT'
    articles = adjust_articles_info(filter_coming_soon(
        filter_articles(filter_json(get_page_data(country)))), country)
    newArticles = compare_articles(articles)
    send_message(newArticles)
    save_external_articles(articles)
    oldArticles = articles


if __name__ == '__main__':
    log('INFO', 'Zalando Scraper has been started', {})
    while True:
        main()
        time.sleep(2)
