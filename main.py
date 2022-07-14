import datetime
import webbrowser

import requests
from bs4 import BeautifulSoup
from Products import prod
import time
from win10toast import ToastNotifier

tmeSince = datetime.datetime.now()
URLBASE = "https://www.adafruit.com/product/"
toast = ToastNotifier()


def checkinstock(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "lxml")
    avail = soup.find(itemprop="availability")
    try:
        if avail.text.lower().__contains__("in stock"):
            return True
        else:
            return False
    except:
        print(page)


def getItemName(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    name = soup.find(class_="products_name")
    return name.text


def showNotif(URL):
    toast.show_toast("Item: " + getItemName(URL) + " is in stock! BUY NOW", URL +
                     " To Purchase the item click on the link now!!!", duration=20, threaded=True)
    webbrowser.open_new(URL)


def displayTime():
    tme = str(time.localtime().tm_hour)
    tme += ":" + str(time.localtime().tm_min).rjust(2, '0')
    tme += ':' + str(time.localtime().tm_sec).rjust(2, '0')
    return tme


def logProduct(stockAvail, URL):
    global tmeSince
    file = open('inStockLog', 'a')
    if stockAvail:
        file.write(getItemName(URL) + " became in stock as of\t\t " + displayTime() + '\n')
        tmeSince = datetime.datetime.now()
    else:
        file.write(getItemName(URL) + " is now out of stock as of\t\t " + displayTime() + '\n')
        file.write(getItemName(URL) + " Lasted for\t\t " + (datetime.datetime.now() - tmeSince).__str__() + "\n")


if __name__ == '__main__':
    while True:
        sku = int(input("Please enter an Adafruit SKU number, enter 0 when finished\nSKU: "))
        if sku == 0:
            break
        prod.append(sku)
    instock = [False] * len(prod)
    for x in range(0, len(prod)):
        URL = URLBASE + str(prod[x])
        instock[x] = (checkinstock(URL))
    while True:
        for i in range(0, prod.__len__()):
            hold = instock[i]
            URL = URLBASE + str(prod[i])
            instock[i] = (checkinstock(URL))
            if instock[i]:
                if not hold:
                    showNotif(URL)
                    print("Item: " + getItemName(URL) + " is in stock! BUY NOW\t\t" + displayTime())
                    logProduct(True, URL)
                else:
                    print("Item: " + getItemName(URL) + " was in stock all along!\t\t" + displayTime())
            else:
                if hold:
                    logProduct(False, URL)
                print("Item: " + getItemName(URL) + " is not in stock :(\t\t" + displayTime())

        time.sleep(30)


