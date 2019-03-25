#Author: Nathan Roehl
#Fall 2018

import urllib
from bs4 import BeautifulSoup

def getWebPage(url):
    try:
        headers = {}
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36 Edge/12.0'
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req)
        soup = BeautifulSoup(resp, 'html.parser')
        return soup
    except Exception as e:
        print("Error")
        print(str(e))


def removeHTML(label):

    s = label.find('>') + 1
    e = label.find('<', s)
    return label[s:e]


print("Start Scrapper.")

while True:
    print("Copy and paste the address")
    url = str(input())
    if url == 'quit':
        break

    soup = getWebPage(url)

    #find all main data
    combo = soup.findAll('div', {'class': ['fact-label','fact-value']})

    all_Data = []
    extra_Data = []

    address = soup.title.string
    loc = address.find("|")
    address = address[:loc -1]
    all_Data.append(address)
    combolength = len(combo)
    valueCounter = 0
    runContinueCounter = False
    continueCounter = 0

    for i in range(combolength):

        if runContinueCounter and continueCounter != 0:
            continueCounter = continueCounter - 1
            continue

        runContinueCounter = False

        nextTerm = str(combo[i])

        if "value" in nextTerm:
            continue

        l = removeHTML(nextTerm).replace(":","")
        v = removeHTML(str(combo[i + 1]))

        combined = '{}: {}'.format(l,v)

        all_Data.append(combined)

        if i+2 >= combolength:
            continue

        valueCounter = i + 2
        extra = str(combo[valueCounter])

        #if extra information with no matching, add to list as extra information
        while valueCounter < combolength and "value" in extra:
            runContinueCounter = True
            continueCounter = continueCounter + 1
            extraTerm = removeHTML(extra)
            combined = '{}: {}'.format('Extra Information', extraTerm)
            extra_Data.append(combined)
            valueCounter = valueCounter + 1
            if valueCounter >= combolength:
                break
            extra = str(combo[valueCounter])

    try:
        saveFile = open(address + ".txt", 'w')
        for data in all_Data:
            saveFile.write(data + "\n")
        for data in extra_Data:
            saveFile.write(data + "\n")

        saveFile.close()
    except Exception as e:
        print("Error opening file")


print("Goodbye")