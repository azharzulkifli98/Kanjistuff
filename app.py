from flask import Flask, render_template, request, url_for, redirect, abort
from pymongo import MongoClient
from bson import ObjectId
from pydoc import describe
import requests
import os

KANJIAPI = 'https://kanjiapi.dev/v1/kanji/'
USER = os.environ.get('Mongodb_user')
PASS = os.environ.get('Mongodb_admin_password')

app = Flask(__name__)

client = MongoClient('localhost', 27017, username=USER, password=PASS)

db = client.flask_db
all_kanji = db.kanjis
all_tags = db.tags


@app.errorhandler(404)
def error_not_found(e):
    problem = "<p>{0}</p><p>Id not valid or item has been deleted.</p>".format(e)
    return problem


@app.route('/')
def index():
    return redirect(url_for('get_list_kanji'))


@app.route('/login')
def login():
    pass


@app.route('/kanji')
def get_list_kanji():
    payload = request.args.get('tag', default='', type=str)
    if payload == '':
        # default page
        kanji_found = list(all_kanji.find({}))
    else:
        # user searches by tag
        kanji_found = list(all_kanji.find( {'tags': payload} ))

    # user gets page
    return render_template('search_kanji.html', filter=payload, tag_list=list(all_tags.find()), kanji_list=kanji_found)


@app.route('/tags')
def get_list_tag():
    payload = request.args.get('filter', default='', type=str)
    if payload == '':
        # default page
        tags_found = list(all_tags.find({}))
    else:
        # user searches by tag
        tags_found = list(all_tags.find( {'name': {'$regex': payload}} ))

    # user gets page
    return render_template('search_tag.html', filter=payload, tag_list=tags_found)


@app.route('/kanji/<id>')
def get_item_kanji(id):
    # ensure id actually exists
    if not ObjectId.is_valid(id) or all_kanji.find( {'_id': ObjectId(id)} ).count() == 0:
        abort(404)

    # load page with item
    item = all_kanji.find_one( {'_id': ObjectId(id)} )
        
    # get API info on kanji
    item['extra'] = requests.get(KANJIAPI + item['symbol']).json()
    return render_template('item.html', kanji=item)


@app.post('/tags/add')
def post_tag():
    return redirect(url_for('get_list_tag'))


@app.post('/tags/delete/<id>')
def delete_tag(id):
    return redirect(url_for('get_list_tag'))


@app.post('/kanji/<id>/add')
def post_kanji_tag(id):
    return redirect(url_for('get_item_kanji'))


@app.post('/kanji/<id>/delete/<tag>')
def delete_kanji_tag(id, tag):
    return redirect(url_for('get_item_kanji'))


def create_user():
    pass

def delete_user():
    pass