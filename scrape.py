import urllib.request
import requests
import pandas as pd
import urllib
import bs4
from json import load
import json
import os
import logging
from selenium import webdriver as wd
from selenium import common as c
from bs4 import BeautifulSoup
from bs4 import Tag
from bs4 import ResultSet
from urllib.request import Request
from logging.handlers import RotatingFileHandler
from pyvirtualdisplay import Display

class scrape:
    ROOT = "https://www.ajio.com"

    req = []
    collectionlist = list()
    categorydict = dict()
    productlist = list()
    #proxy = "rilproxy.in.ril.com"
    webbrowser = []

    logger = logging.getLogger("ajioscrapper")
    handler = RotatingFileHandler("ajioscrapper.log",'a',maxBytes=10000,backupCount=1)
    logger.addHandler(handler)
    logger.setLevel("INFO")

    def scrapeit(self):
        try:

            html = requests.get(self.ROOT )
            soup = BeautifulSoup(html.text, 'html.parser')
            rootlinks = soup.find_all('div',{"class","fnl-FB-types"})

            logging.info("Started scraping")
            self._processroot(rootlinks)

            #index = 0
            for category in self.categorydict:
                plpurl = "{}{}".format(self.ROOT, self.categorydict[category])
                self._processplp(plpurl,category)
                #index = index + 1
                #if index > 1: break


            jsondata = "{}"
            jsondata = json.dumps(self.productlist)
            print(jsondata)
            df  = pd.DataFrame(self.productlist)
            df.to_csv('products.csv')


        except Exception as ex:
            self.logger.exception(ex)
        finally:
            if self.webbrowser:
                self.webbrowser.quit()

    def _processplp(self,plpurl,categoryid):
        '''This method will process the basic category and product attributes for each swatch of the product and in turn
        call the PDP page to capture details
        '''

        #html = requests.get(plpurl)
        soup = BeautifulSoup("<html/>", 'html.parser')
        self.logger.info("Started scraping for category - {}".format(categoryid))

        #display = Display(backend=True, visible=False,size=(100,100))
        #display.start()
        '''if we know number of pages, lets open them up by clicking load more so that we have all items opened up'''
        print("Path is in {}".format(os.path.join( os.path.dirname(__file__),'driver/chromedriver')))
        self.webbrowser = wd.Chrome(os.path.join( os.path.dirname(__file__) ,'driver/chromedriver'))
        self.webbrowser.get(plpurl)

        '''does loadmore exist'''
        #loadbtnelement = soup.find("button", {"class": "loadMoreBtn"})
        #numberOfPages = int(soup.find("input", {"name": "numberOfPages"}).get("value"))
        pageinput = self.webbrowser.find_element_by_name("numberOfPages")
        numberofpages = int(pageinput.get_attribute('value'))
        loadbtn = self.webbrowser.find_element_by_class_name("loadMoreBtn")
        for index in range(0,numberofpages):
            try:
                loadbtn.click()
            except c.exceptions.ElementNotVisibleException as elem:
                self.logger.info("Element missing")
            except Exception as ex:
                self.logger.error("Exception occurred in click of page - {} for href - {}".format(index+1,plpurl))
                pass
        '''After loading all buttons, get the html'''
        html = self.webbrowser.page_source.encode()
        self.webbrowser.close()
        #display.stop()

        soup = BeautifulSoup(html, 'html.parser')

        categoryname = soup.find('h1',{'class':'fnl-headline3 fnl-margin11'}).contents[2]

        rootlink = soup.find_all('a',{'id':'fnl-plp-producthov'})

        item = 0
        for link in rootlink:
            try:
                self.logger.info("processing for plp - {}".format(plpurl))
                href = link.get('href')
                title = link.get('title')

                self.logger.info("Processing for link - {}".format(href))

                proddetails = self._recursiveplpscraping(link,href)


                '''if there is no color options, just add the selected color as the only option'''
                if not proddetails["coloroptions"]:
                    proddetails["coloroptions"] = proddetails["color"]

                colorarray = proddetails["coloroptions"]
                sizearray = proddetails["sizeoptions"]

                '''create product for every size'''
                if sizearray:
                    for size in sizearray:
                        self.productlist.append({'category': categoryid, 'link': size["href"],
                                                 'categoryname': categoryname,
                                                 'title': title, 'img': proddetails['img'],
                                                 'brand': proddetails['brand'], 'subtitle': proddetails['subtitle'],
                                                 'productid': size['productid'],
                                                 'price': proddetails['price'],
                                                 'color': proddetails['color'],
                                                 'sizetitle' :size['title'],
                                                 'size':size['size'],
                                                 'coloroptions': proddetails['coloroptions'],
                                                 'bullets': proddetails['bullets'],
                                                 'groupid':"{}{}".format(self.ROOT, href),
                                                 'mrp': proddetails['mrp'],
                                                 'sizeoptions': proddetails["sizeoptions"],
                                                 'description': proddetails['description'],
                                                 'currency': proddetails['currency']
                                                 })
                else:
                    self.productlist.append({'category': categoryid, 'link': "{}{}".format(self.ROOT, href),
                                             'categoryname': categoryname,
                                             'title': title, 'img': proddetails['img'],
                                             'brand': proddetails['brand'], 'subtitle': proddetails['subtitle'],
                                             'productid': proddetails['productid'],
                                             'price': proddetails['price'],
                                             'color': proddetails['color'],
                                             'sizetitle': "",
                                             'size': "",
                                             'coloroptions': proddetails['coloroptions'],
                                             'bullets': proddetails['bullets'],
                                             'groupid': "{}{}".format(self.ROOT, href),
                                             'mrp': proddetails['mrp'],
                                             'sizeoptions': proddetails["sizeoptions"],
                                             'description': proddetails['description'],
                                             'currency': proddetails['currency']
                                             })
                item = item + 1
                if item > 20: break
                '''self.productlist.append({'category': categoryid, 'link': "{}{}".format(self.ROOT, href),
                                 'categoryname': categoryname,
                                 'title': title, 'img': proddetails['img'],
                                 'brand': proddetails['brand'], 'subtitle': proddetails['subtitle'],
                                 'productid': proddetails['productid'],
                                 'price': proddetails['price'],
                                 'color': proddetails['color'],
                                 ''
                                 'coloroptions': proddetails['coloroptions'],
                                 'bullets': proddetails['bullets'],
                                 'mrp': proddetails['mrp'],
                                 'sizeoptions': proddetails["sizeoptions"],
                                 'description': proddetails['description'],
                                 'currency': proddetails['currency']
                                 })
                '''

            except Exception as ex:
                logging.exception(ex)
                logging.info("Skipping the link - {}".format(href))


    def _recursiveplpscraping(self,link,href):
        for child in link.children:
            if isinstance(child, bs4.element.Tag):
                imgnodes = child.find_all('img', {'class': 'plp-lazy-product sitespinner-plp fnl-pdp-img product-view'})
                img =[]
                if imgnodes:
                    for node in imgnodes:
                        img = node.get('data-original')

                brand =""
                subtitle =""

                brandnode = child.find('div', {'class': 'fnl-plp-title'})
                if brandnode: brand = brandnode.text.strip()

                subtitlenode = child.find('div', {'class': 'fnl-plp-subtitle'})
                if subtitlenode: subtitle =subtitlenode.text.strip()

                proddetails = self._getpdp("{}{}".format(self.ROOT, href))

                proddetails["subtitle"] = subtitle

                proddetails["img"] = "{}{}".format(self.ROOT,img)

                proddetails["brand"] = brand

                self.logger.info("Processed recursiveplpscraping for {}".format(subtitle))

        self.logger.info("Processed for {}".format(href))

        return proddetails


    def _getpdp(self, url):
        '''Given a PDP URL this method will initialize and read all variant information, price and also bullet points'''
        colorvars = []
        sizevars = []
        selectedcolor = ""
        price=""
        mrp = ""
        bullets=[]

        html = requests.get(url)
        soup = BeautifulSoup(html.text,'html.parser')

        productid = soup.find('span',{'id':'pdetailsCode'}).text
        price = soup.find('span',{'class':'fnl-cart-finprc-amt'}).text.strip()
        price = price.split(".")[1].strip().replace(",","")
        self.logger.info("Price processed")

        '''this will be overriden in case mrp exists'''
        mrp = price
        mrpnode = soup.find('span',{'class':'fnl-pdp-priceStrike'})

        if mrpnode:
            for mrpn in mrpnode.descendants:
                if isinstance (mrpn, bs4.element.Tag) and len(mrp)>0:
                    mrp = mrpn.text.strip()
        self.logger.info("MRP processed")

        '''Get all size and color variants'''
        sizevariants = soup.find_all('a',{'data-sizeflag':'true'})
        colorvariants = soup.find_all('a',{'class':'colorVariant'})

        colornode = soup.find('span',{'class':'fnl-sizecolorspec'})

        '''meta tags'''
        description = soup.find('meta',{'name':'description'}).get('content')
        self.logger.info("Description processed")

        '''Current colr node value'''
        if colornode:
            selectedcolor = colornode.text

        self.logger.info("Colornode processed")

        '''The size variant details with productid is captured'''
        varsize=""
        for var in sizevariants:
            '''Get the code which is used for size'''
            for child in var.children:
                if isinstance(child,bs4.element.Tag):
                    varsize = child.text
            '''Title for the code'''
            vartitle = var.get('data-optionstr')
            varhref = var.get('href')
            varcode = var.get('data-code')
            sizevars.append({"size":varsize,"productid": varcode,"href":"{}{}".format(self.ROOT,varhref),"title":vartitle} )
        self.logger.info("Size variant processed")

        '''Get the color variant details'''
        for col in colorvariants:
            img = col.find('img')
            if img :
                color = img.get('title')
                colorvars.append(color)
        self.logger.info("Color variant processed")

        '''Get all bullets which we will curate'''
        pdpbullets = soup.find_all("ul",{"class":"fnl-pdp-bullets"})
        for bullet in pdpbullets:
            points = bullet.find_all('li')
            for point in points:
                bullets.append(point.text)
        self.logger.info("Bullet points processed")

        '''List of color variants'''
        colorvariations =""
        sizevariations = ""
        if colorvars:
            colorvariations = ",".join(colorvars)


        '''List of all bullet points'''
        bulletpoints = ""
        if bullets:
            bulletpoints = ",".join(bullets)


        '''Get the currency to use'''
        currency = soup.find("span",{"itemprop":"priceCurrency"}).get("content")

        proddetails = { "price" : price, "mrp":mrp,
                        "color":selectedcolor ,"coloroptions": colorvariations, "sizeoptions":sizevars, "bullets":bulletpoints,
                            "description": description,"productid":productid, "currency":currency
                        }

        self.logger.info("Processed PDP for {}".format(url))

        return proddetails



    def _processroot(self,rootlinks):
        '''This method scans the home page to pick the menu links for all categories'''
        for rootlink in rootlinks:
            alinks = rootlink.find_all('a')
            for a in alinks:
                href = str(a.get('href'))
                '''This means its collection page, so will ignore for now'''
                if href.startswith("/cp"):
                    self.collectionlist.append(href)
                elif href.startswith("/c"):
                    '''this means category or plp page'''
                    if href.split("/")[2].isdigit():
                        self.categorydict[href.split("/")[2]] = href
                    else:
                        print("ignored {}".format(href.split("/")[2]))

                self.logger.info("Processed for link - {}".format(href))


if __name__ == "__main__":
    scr = scrape()
    scr.scrapeit()