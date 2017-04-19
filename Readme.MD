<b>Purpose</b>

This is a simple scrapper application which is used to scrape every category page link on www.ajio.com

The intent of the program is to load home page of ajio.com, find all links in navigation menu and save in collection.
Once done,  only pattern '/c/' is matched and the Product listing pages for all such pages are loaded.

For the above operation program uses beautifulSoup module.

Using chromedriver, then it executes selenium module to load all the products in listing page as there is lazy loading enabled only on click of "Load more" button. The program loads this until there is no load more button and applies them into collection of products for that category.
Then the program gets to the next level into product details of every product to get price, size options and color options with the primary image used. The program also indexes the PDP link for the product outside of the category, category name, title, brand, short titles, category code.


<b> How to execute ?</b>

Download the program into a folder and enter the folder and hit:

```bash

python scrape.py

```
In case you have both python2 and python3, use:

```bash

python3 scrape.py


```
NOTE THAT THE URLLIB, REQUESTS AND OTHER MODULES USED ARE SUPPORTED ONLY IN PYTHON 3, SO THIS IS NOT SUPPORTED FOR PYTHON 2.X

<b>What is the output ?</b>


The output of this program will be products.csv with the following attributes scraped.

```bash

brand	bullets	category	categoryname	color	coloroptions	currency	description	groupid	img	link	mrp	price	productid	size	sizeoptions	sizetitle	subtitle	title
PERFORMAX	Boasting QuickDry technology, side slip pockets that extend to the back, and mesh panels, this high-neck knitted contour jacket creates a defining sporty look.,Pointelle mesh, back zip pocket, anti-static to remove static cling,Front zipper, printed branding along the sleeve,QuickDry technology pulls moisture and sweat for added comfort ,100% polyester,Slim Fit,The model is wearing a size larger for a comfortable fit,Machine Wash Cold,The colour of the actual product might marginally vary from the colour seen in the images, Product Code:Â 440720561005,About PERFORMAX	830216010	Jackets & Coats	Multicoloured	Multicoloured,Grey 	INR	Buy Multicoloured PERFORMAX QuickDry Cycling Contour Jacket Online only at AJIO in India	https://www.ajio.com/performax-quickdry-cycling-contour-jacket/p/440720561_white	https://www.ajio.com/medias/sys_master/root/h6f/h19/9950315413534/-286Wx359H-440720561-white-OUTFIT.jpg	https://www.ajio.com/performax-quickdry-cycling-contour-jacket/p/440720561005/sizeSelected/S		1499	4.40721E+11	S	[{'size': 'S', 'productid': '440720561005', 'href': 'https://www.ajio.com/performax-quickdry-cycling-contour-jacket/p/440720561005/sizeSelected/S', 'title': 'Small'}, {'size': 'M', 'productid': '440720561006', 'href': 'https://www.ajio.com/performax-quickdry-cycling-contour-jacket/p/440720561006/sizeSelected/M', 'title': 'Medium'}, {'size': 'L', 'productid': '440720561007', 'href': 'https://www.ajio.com/performax-quickdry-cycling-contour-jacket/p/440720561007/sizeSelected/L', 'title': 'Large'}, {'size': 'XL', 'productid': '440720561008', 'href': 'https://www.ajio.com/performax-quickdry-cycling-contour-jacket/p/440720561008/sizeSelected/XL', 'title': 'Extra Large'}]	Small	QuickDry Cycling Contour Jacket	QuickDry Cycling Contour Jacket

```

<b>Modules </b>

scrape.py - Core of scrapper

customerorderstib.py - generates customerorder.csv which gives dynamic orderdate, cartsize(qty), productid, userid for machine learning usecases.

<b>Uses ?</b>

This can be used for warmup of pages like PLP, PDP and also images during late hours to avoid more stress during peak.

Other use is to use another module which I have added i.e. 'Customerorderstub' which generates or simulates customer's Id and picks up the product id and dynamically generates orders which can then be used for any analysis required for Machine learning usecases.

<b>Debts</b>

Following debts are to be taken care in future:

1. Reading data in chunks

2. Giving an interactive option to user to select which category to scrape and which one to skip

3. Writing data in chunks

4. Optimization of chromedriver/selenium interfacing i.e. background mode and wait operations.

