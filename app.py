from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from html.parser import HTMLParser
import os
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
import json


# By Deafult Flask will come into this when we run the file
@app.route('/')
def index():
    return ("index.html")  # Returns index.html file in templates folder.


# After clicking the Submit Button FLASK will come into this
def amaze(soup):

    bloggy = soup.select('div.s-latency-cf-section')
    listu=[]
    for x in bloggy:
        try:
            try:
                name = x.select('.a-size-base-plus')[0].text + " " + x.select('.a-size-base-plus')[1].text
            except:
                name = x.select('.a-size-base-plus')[0].text
        except:
            name = x.select('.a-spacing-none.s-line-clamp-2')[0].text
        try:
            price = x.select('.a-price-whole')[0].text + x.select('.a-price-symbol')[0].text
        except:
            price = 'N/A'
        try:
            img = x.select('.s-image')[0]['src']
        except:
            img = ''
        try:
            rate = x.select('.aok-align-bottom')[0].text
        except:
            rate = ''

        try:
            g = {'name': name, 'price': price, 'image': img, 'rate': rate}
        except:
            g = {}
        listu.append(g)
    return listu



def ebayed(soup):
    listu1=[]
    bloggy=soup.find_all('div', attrs={'class': 's-item__wrapper clearfix'})
    for x in bloggy:
        try:
            name = x.find_all('h3', attrs={'class': 's-item__title'})
        except:
            name[0] = ''

        try:
            pri = x.find_all('span', attrs={'class': 's-item__price'})
            price = pri[0].text
        except:
            price = ''

        img = x.find_all('img', attrs={'s-item__image-img'})
        for c in img:
            (c['src'])
        try:
            g = {'name': name[0].text, 'price': price, "img": c['src'], "rate": 'null'}
            print(g)
        except:
            g = {}

        listu1.append(g)

    return listu1







@app.route('/api/', methods=['GET'])
@cross_origin()
def home():
    try:
        global output_data
        output_data = []
        if 'web' in request.args:
            id = str(request.args['web'])


        else:
            return "Error: No id field provided. Please specify an id."

        if 'search' in request.args:
            sr = str(request.args['search'])
            try:
                pg=str(request.args['search'])
                if int(pg)<0:
                    pg='1'
            except:
                pg='1'
            global baseURL
            if 'amazon' in id:
                baseURL = 'http://www.'+id+'/s?k='+sr+'&page='+pg
            elif 'ebay' in id:
                baseURL = 'https://www.'+id+'/sch/i.html?_nkw='+sr+'&page='+pg

        else:f
            return "Error: No id field provided. Please specify an id."
            # Create an empty list for our results

        # Loop through the data and match results that fit the requested ID.
        # IDs are unique, but other fields might return many results

        url = baseURL
        try:
            r = Request(url, headers={'User-Agent': 'Mozilla/5.0(compatible; Googlebot/2.1;+http://www.google.com/bot.html)'})
            web_url = urllib.request.urlopen(r)
            d = web_url.read().decode('utf-8', 'ignore')
            d = str(d)
            soup=BeautifulSoup(d,'html.parser')
        except Exception as es:
            return str(es)



        if 'amazon' in baseURL:
            return jsonify(amaze(soup))

        elif 'ebay' in baseURL:
            return jsonify(ebayed(soup))

        else:
            pass


        #if 'amazon' in baseURL:
            #return jsonify(listu)
        #else:
            #return jsonify(listu1)

    except Exception as es:
        if 'amazon' in baseURL:
            try:
                ku = []
                url = 'http://api.scraperapi.com/?api_key=06cb789e1afb5ae8df2d0affcd2bfb95&url=https://www.amazon.com/s?k=' + sr + '&autoparse=true'
                req = Request(url, headers={'User-Agent': 'Mozilla/8.0'})
                json_url = urllib.request.urlopen(req)
                d = json_url.read()
                data = json.loads(d)
                for x in data['results']:
                    di = {}
                    di['name'] = x['name']
                    di['img'] = x['image']
                    di['price'] = x['price_string']
                    di['rate'] = x['stars']
                    ku.append(di)
            except:
                ku = [{'name': "null", 'price': "null",
                       "img": "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.pngitem.com%2Fmiddle%2FiJJRbhw_no-profile-picture-available-hd-png-download%2F&psig=AOvVaw3xRSY0MPQM7NlJvyxSb4hC&ust=1624013108180000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCJj-ub2-nvECFQAAAAAdAAAAABAD",
                       "rate": 'null'}]
                return jsonify(ku)
        else:
            return (str(es))



if __name__ == '__main__':
    app.run(debug=True)


#if __name__ == "__main__":
    #port = int(os.environ.get("PORT", 5000))
    #app.run(host="0.0.0.0", port=port)