#! /usr/bin/env python

import argparse
import requests
import mimetypes
from base64 import b64encode
from bs4 import BeautifulSoup
from butterfly.escapes import html
from json import loads
from tinydb import TinyDB,Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from tqdm import tqdm
from random import randint

latest_xkcd_url = 'http://xkcd.com/info.0.json'
xkcd_url_fmt = 'http://xkcd.com/{0}/info.0.json'

parser = argparse.ArgumentParser(description="Butterfly xkcd viewer")
parser.add_argument('-n','--number', action="store",dest='number',
                    help="specify number of random xkcd to view",
                    nargs=1,default=[1],type=int)

parser.add_argument('-u','--update', action="store_true",dest='update')
args = parser.parse_args()
number = args.number[0]
db = TinyDB('./xkcd_db.json',storage=CachingMiddleware(JSONStorage))

if args.update:
    r = requests.get(latest_xkcd_url)
    response = loads(r.text.decode('utf-8'))
    latest_num = response['num']
    for xkcd_num in tqdm(xrange(404,latest_num)):
        url = xkcd_url_fmt.format(xkcd_num)
        r = requests.get(url)
        try:
            data = loads(r.text)
            db.insert(data)
        except:
            pass
else:
    for x in xrange(number):
        random_xkcd = randint(1,len(db.all()))
        comic = Query()
        res = db.search(comic.num==random_xkcd)
        if len(res) != 0:
            stored_json = res[0]
            img_url = stored_json['img']
            title = stored_json['title']
            with html():
                print '<img src="{0}" alt="{1}"/>'.format(img_url,title)

db.close()


