from django.shortcuts import render
from django.http import HttpResponse
import random
import requests
from bs4 import BeautifulSoup as bs
# Create your views here.

def get_html_content_r(product):
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    
    product = product.replace(' ','+')
    r_html_content = session.get(f'https://www.reliancedigital.in/search?q={product}').text
    return r_html_content

def get_html_content_f(product):
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    
    product = product.replace(' ','+')
    f_html_content =  session.get(f'https://www.flipkart.com/search?q={product}').text
    return f_html_content

def get_html_content_a(product):
    user_agent_list = [ 
	'Mozilla/5.0 (Windows 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36', 
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36', 
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15', 
    ] 
    for i in range(1,4):
        USER_AGENT = random.choice(user_agent_list)
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    
    product = product.replace(' ','+')
    a_html_content = session.get(f'https://www.amazon.in/s?k={product}').text
    return a_html_content

def home(request):
    product_data = None
    if 'product' in request.GET:
        product = request.GET.get('product')
        product_data = dict()

        #Amazon
        a_html_content = get_html_content_a(product)
        #print(html_content)
        soup = bs(a_html_content,'html.parser')
        title = soup.find('div',class_='a-section a-spacing-none puis-padding-right-small s-title-instructions-style')
        product_data['title_a'] = title.find('span',class_='a-size-medium a-color-base a-text-normal').text[0:115]
        if product_data['title_a'] == ' ':
            product_data['title_a']= product
        #print(title)
        amz_prize = soup.find('div',attrs={"data-component-type":"s-impression-logger"})
        product_data['price_a'] = amz_prize.find('span',class_='a-price-whole').text
        #print(product_data['price'])
        image_div = soup.find('div',class_='a-section aok-relative s-image-fixed-height')
        image_img = image_div.find('img')
        image_src = image_img.get('src')
        product_data['image_a'] = (f'{image_src}')
        product = product.replace(' ','+')
        product_data['link_a'] = (f'https://www.amazon.in/s?k={product}')


        #RelianceDigital
        r_html_content = get_html_content_r(product)
        #print(html_content)
        soup = bs(r_html_content,'html.parser')
        main_div = soup.find('li',class_='grid pl__container__sp blk__lg__3 blk__md__4 blk__sm__6 blk__xs__6')
        text = main_div.find('div',class_='slider-text')
        product_data['title_r']=text.find('p',class_='sp__name').text[0:115]
        price=text.find('span',class_='TextWeb__Text-sc-1cyx778-0')
        
        if price:
            inner_spans = price.find_all('span')
            inner_texts = [span.text for span in inner_spans]
        
        product_data['price_r']=(''.join(inner_texts))
           
        product_img = soup.find('div',class_='sp__productbox')
        product_img_1 = product_img.find('img')
        url_img= product_img_1.get('data-srcset')
        if url_img.startswith('/'):
            product_data['image_r']=(f'https://www.reliancedigital.in' + url_img)
        else:
            product_data['image_r']=url_img
        
        product = product.replace(' ','+')
        product_data['link_r'] = (f'https://www.reliancedigital.in/search?q={product}')
        """ product_link = soup.find('div',class_='sp grid')
        product_link_1 = product_link.find('a',attrs={'attr-tag':'anchor'})
        url_link = product_link_1.get('href')
        if url_link.startswith('/'):
            product_data['link_r']=(f'https://www.reliancedigital.in' + url_link)
        else:
            product_data['link_r']=url_link """

        #Flipcart
        f_html_content = get_html_content_f(product)
        #print(html_content)
        soup = bs(f_html_content,'html.parser')
        title = soup.find('div',class_='_3pLy-c row')
        #print(title)
        product_data['title_f'] = title.find('div',class_='_4rR01T').text [0:115]
        product_data['price_f'] = soup.find('div',class_='_30jeq3 _1_WHN1').text
        image_div = soup.find('div',class_='CXW8mj')
        image_img = image_div.find('img')
        image_src = image_img.get('src')
        product_data['image_f'] = (f'{image_src}')
        product = product.replace(' ','+')
        product_data['link_f'] = (f'https://www.flipkart.com/search?q={product}')


        pass
    return render(request,'home.html',{'data':product_data})

def contact(request):
    return render(request,'contact.html')