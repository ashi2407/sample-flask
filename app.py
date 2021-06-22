from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import urllib
from flask import Flask, render_template, jsonify, request, redirect, url_for
import os
from flask_cors import CORS, cross_origin
import json
import time
app = Flask(__name__)
cors = CORS(app)



# By Deafult Flask will come into this when we run the file
@app.route('/')
def index():
    return ("index.html")  # Returns index.html file in templates folder.


# After clicking the Submit Button FLASK will come into this
def amaze(url,ext):
    r = Request(url,headers={'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1;+http://www.google.com/bot.html)'})
    web_url = urllib.request.urlopen(r)
    d = web_url.read().decode('utf-8','ignore')
    d = str(d)
    soup = BeautifulSoup(d,'html.parser')
    listu = []
    bloggy = soup.select('div.s-latency-cf-section')
    for x in bloggy:
        try:
            try:
                name = x.select('.a-size-base-plus')[0].text+ " "+x.select('.a-size-base-plus')[1].text
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
            img=img.split('UL')
            img=img[0]+'UL580_.jpg'
        except:
            img = ''
        try:
            rate = x.select('.aok-align-bottom')[0].text
        except:
            rate = ''

        plink=x.select('.s-line-clamp-4')[0].find_all('a')[0]['href']
        link='www.amazon.'+ext+plink
        try:
            g = {'name': name, 'price': price, 'image': img, 'rate': rate,'link':link}
        except:
            g = {}

        listu.append(g)
    return listu



def ebayed(url,ext):
    try:
        r = Request(url,headers={'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1;+http://www.google.com/bot.html)'})
        web_url = urllib.request.urlopen(r)
        d = web_url.read().decode('utf-8', 'ignore')
        d = str(d)
        soup = BeautifulSoup(d, 'html.parser')

        listu1 = []
        bloggy = soup.find_all('div', attrs={'class': 's-item__wrapper clearfix'})

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

            try:
                img = x.find_all('img', attrs={'class': 's-item__image-img'})[0]['src']
                print(img)
            except:
                img = ''
            reqlink = x.select('a.s-item__link')[0]['href']
            try:
                g = {'name': name[0].text, 'price': price, "img":img, "rate": 'null','link':reqlink}
                print(g)
            except:
                g = {}

            listu1.append(g)

        return listu1
    except Exception as es:
        return str(es)


def amapi(search):
    ku = []
    url = 'http://api.scraperapi.com/?api_key=06cb789e1afb5ae8df2d0affcd2bfb95&url=https://www.amazon.com/s?k=' + search + '&autoparse=true'
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
        di['link']=x['url']
        ku.append(di)
    return ku

@app.route('/api/', methods=['GET'])
@cross_origin()
def home():
    try:
        if 'web' in request.args:
            id = str(request.args['web'])
            ext=str(request.args['ext'])
            id=id.replace(" ",'')
        else:
            return "Error: No id field provided. Please specify an id."
        if 'search' in request.args:
            sr = str(request.args['search'])
            try:
                pg=str(request.args['page'])
                if int(pg)<0:
                    pg='1'
                else:
                    pass
            except:
                pg='1'
            global baseURL
            if 'amazon' in id:
                baseURL = 'https://www.'+id+'.'+ext+'/s?k='+sr+'&page='+pg
            elif 'ebay' in id:
                baseURL = 'https://www.'+id+'.'+ext+'/sch/i.html?_nkw='+sr+'&page='+pg

        else:
            return "Error: No id field provided. Please specify an id."
            # Create an empty list for our results

        # Loop through the data and match results that fit the requested ID.
        # IDs are unique, but other fields might return many results

        url = baseURL
        if 'amazon' in baseURL:
            try:
                gh = amaze(url,ext)
                time.sleep(10)
                return jsonify(gh)
                
            except Exception as es:
                try:
                    #hg = amapi(sr)
                    #return jsonify(hg)
                    return str(es)
                except:
                    ku = [{'name': "null", 'price': "null",

                           "img": "data:image/png;base64,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",

                           "rate": 'null'}]

                    return jsonify(ku)

        elif 'ebay' in baseURL:
            print('****************************************************************************************************************************')
            kl=ebayed(url,ext)
            print(kl)
            return jsonify(kl)

        else:
            pass

    except Exception as es:
        ku = [{'name': "null", 'price': "null",

               "img": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMIAAAEDCAMAAABQ/CumAAAARVBMVEX///+ysrKtra2fn5/y8vLMzMz6+vrc3NzJycmsrKy/v7+dnZ2hoaHu7u7S0tLGxsbn5+fY2NjR0dG3t7fg4ODq6uqVlZWPPfCzAAAGNUlEQVR4nO2ci5bqKBBFCSQkPPLG/v9PHaogtrZR+zrODc46u1cvE8BYB4pHkagQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADgE2m7V2nao21neikrQl5T/QpZ1UfbL4TejLXNJfZ3EiJHCxBiyBLkfJUcftkMlTzel7bq3pcgzUOoSHeQ4d88lPCsij9AwjNHL0tC7M6Xo6XdkXVLYRJuB1X5dLQpSEKzP3OFZ28uR8L66psh4U1AQikSquZFCpLwYAn0dNFatgRppLV2fayiZAnSBp3K1O16X0S5EuR6uiw23RVRrASz/CzY3dFQqgSzs7aYzSdJOCvo23kOW3g87LZDmRJkk/LaytCgatasaPwcCXm2tudaNyMn6I+RICfOWenQpJFIWk5qd1ypSAnrdwZ5UJKVLP0QCSncnOSmJftST8fNh0joc7qMk3M7rjmZu8PO9lKJEgwla8OtMX6bLCm5/gwJbGv0I1mL6WI2kzw93E5vJUrgfYvoMUaL+aLSk399lgQZ9GXmJ0ngvtBLCneukmnlrT9EAkcJt/2WUvsP6c48OXc/UwdK3ZmeS5SQjKp/uIzUj0ofyt4aia1trzQYbpqdaaFQCewzYrjQYNKNhp/eVayEPIvFgXW7iVWltetpL+YpU8IWMOh5lcZIm+/17IYLpUqo7Dlf6/Phulu0VAnS3hTU+wqKlRDpr8tN98oVLMGMFzf2e3t3O69gCbShN0y11vU0PNiPLFvC9y3ER2UKkSBfpBwJaxw6X6IkCS8CCW/i/yKhfpFyJPyrEak5WsHuTu+fkPeQD+XO6u23Cm7Xg38fbc2rfiSlKUGBoLtRrxIKeMQTAAAAAAAAAAAA4JNox5Pou7xB2nS8R9eP21PDUzcutOESOvrmRTccY+MTrGtFUIqfjtxerfecpytFxLRFeReRBxp6H6uiBJ9sNt6TBB1PuTUqX019410tFj/2p9Opf3ipo9gkRB9pfZIwq9nThmNQ/KDYHKgVjt/IvkuSsFIzeF+xBOnFqjT509n3Yyvoui50G5IlqHFRc6u6kST0bhQtdYBKRXfSbdtOUQL1hS/9/HoHkCRY4Y3xsd7pMVsVXZ58aPXRheovF3MXv9KIdLSx+2wSBu+bJIEr3KuTaLhH1JokFN8XopHCR/cnCa2vhmGw0XytqBnE6EnCzXd8yuEsoe8FS6jY7mi+jj3Cr6NRJMFXljja2l1oamvd9v0RN9fO8WHl4nAUvHI+OCsaR3Oc8wcaeh9da/7fTrbj/EoDKZdIHGYmAACUwdSkwXHmQKweujme62Vglu154IZym4WL6mXh9/EI2s8TlT5fLpXMF1goqhiWPCKnay7vH3gbxaFW4Nlr5BmqFf1XXAXFaWub0mJQJmhi41XEzKlGjelkFPXFlNZxSaEdvds7WlK5ZHRKcl9XX5d+C3GZnMIXy58/TzEKCyKEqfLDFPLnxXAtVu4phTiS1thTDuTmqKRO6UwO6OL6YwrTSGWMyhLiNaYQwvsX5EsKxUhCrTx9WpuMW9W5viY3+FTzcZ1Upxbxgwq3EoJbuEZ0agyvriS83fhNQuWjZYEX/emLs4aqOQU0Ceu0JUMG1eUYU0dnUtWthFWJ1VFn4qSg1isJNT09+R9IUHPjvSYJ1qfey1HBhQSyN7gmV6Qh357j4m8l264l1NHmVg3cCtHvOf1CAvWF/yCuoJV+5avgbTb9VgK7jCdzrJp6xS7lqY6bnxKarWSUMI7j6q9bISaNT3/V5zUJ2ngZJcw+DUDkWJcSjKc/6qaTGtnKk09JPyXkkqfsSLGhwt/oCxRv1Z7GJe1zFMbD7FnCpAz92hx3U7JQUDvRT9HJWPxKwuS3krk7r374WxKiU5CFrVK2ib27vpKQ9lo0BZ40fnXbMbdalkAuMvbJAymgi/8sxp2iakuZs0iONL7/scMmdbCO5yuKwlT+4cHKpQ/TLs1NK3doPhlclXN0ntqoo7rFOZ3eOcR5jLozifeKM63IpZ79ztifU/fJ4u1lqs8ZOTzr+/xKOXyyZfW95tQ+UV+UTCmpUMrcDsrcawIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAfwD6FBO0p+vobQAAAAASUVORK5CYII=",

               "rate": 'null'}]

        return jsonify(ku)




#if __name__ == '__main__':
    #app.run(debug=True)


#if __name__ == "__main__":
    #port = int(os.environ.get("PORT", 5000))
    #app.run(host="0.0.0.0", port=port)
