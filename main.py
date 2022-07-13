import webbrowser

import requests
from bs4 import BeautifulSoup
from Products import prod
import time
from win10toast import ToastNotifier
import lxml

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
    soup = BeautifulSoup(page.content, "lxml")
    # soup = bs4.BeautifulSoup(page.text, "html.parser")
    name = soup.find(class_="products_name")
    return name.text


def showNotif(URL):
    toast.show_toast("Item: " + getItemName(URL) + " is in stock! BUY NOW", URL +
                     " To Purchase the item click on the link now!!!", duration=20, threaded=True)
    webbrowser.open_new(URL)


if __name__ == '__main__':
    while True:
        sku = int(input("Please enter an Adafruit SKU number, enter 0 when finished\nSKU: "))
        if sku == 0:
            break
        prod.append(sku)
    instock = [True] * prod.__len__()
    while True:
        for i in range(0, prod.__len__()):
            hold = instock[i]
            URL = URLBASE + str(prod[i])
            instock[i] = (checkinstock(URL))
            if instock[i]:
                if not hold:
                    showNotif(URL)
                    print("Item: " + getItemName(URL) + "\tis in stock! BUY NOW\t" + str(time.localtime().tm_hour)
                          + ":" + str(time.localtime().tm_min))
                else:
                    print("Item: " + getItemName(URL) + "\twas in stock all along!\t" + str(time.localtime().tm_hour)
                          + ":" + str(time.localtime().tm_min))
            else:
                print("Item: " + getItemName(URL) + "\tis not in stock :(\t" + str(time.localtime().tm_hour) + ":" +
                      str(time.localtime().tm_min))

        time.sleep(30)


