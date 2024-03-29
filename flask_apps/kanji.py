from flask import Flask, render_template, request, url_for, redirect, abort
from pymongo import MongoClient
from bson import ObjectId
from pydoc import describe
import requests

KANJIAPI = 'https://kanjiapi.dev/v1/kanji/'

app = Flask(__name__)

client = MongoClient('localhost', 27017)

db = client.flask_db
all_kanji = db.kanjis
all_tags = db.tags

@app.route('/')
def index():
    return redirect(url_for('search'))


@app.errorhandler(404)
def error_not_found(e):
    problem = "<p>{0}</p><p>Id not valid or item has been deleted.</p>".format(e)
    return problem


@app.route('/app/kanji/', methods=('GET', 'POST'))
def search():
    payload = request.args.get('tag', default='', type=str)
    if payload == '':
        # default page
        kanji_found = list(all_kanji.find({}))
    else:
        # user searches by tag
        kanji_found = list(all_kanji.find( {'tags': payload} ))

    # user gets page
    return render_template('search_kanji.html', filter=payload, kanji_list=kanji_found)


@app.get('/app/tags/')
def get_tags():
    # user gets page
    return render_template('search_tag.html', tag_list=list(all_tags.find()))


@app.post('/app/kanji/insert/')
def insert_kanji():
    # user adds a kanji using input forms
    symbol = request.form['symbol']
    description = request.form['description']
    all_kanji.insert_one({'symbol': symbol, 'description': description, 'tags': ['new', 'free']})
    return redirect(url_for('search'))


@app.post('/app/kanji/delete/<id>/')
def delete_kanji(id):
    # user deletes a kanji using object button
    if ObjectId.is_valid(id):
        all_kanji.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('search'))


@app.route('/app/kanji/<id>', methods=('GET', 'POST'))
def item(id):
    # ensure id actually exists
    if not ObjectId.is_valid(id) or all_kanji.find( {'_id': ObjectId(id)} ).count() == 0:
        abort(404)

    # option to add a new tag
    if request.method == 'POST':
        new_tag = request.form['tag']
        if all_tags.find( {'name': new_tag} ).count() == 1:
            # increase count by one and append to list
            plus_one = all_tags.find_one( {'name': new_tag} )['count'] + 1
            all_tags.update_one( {'name': new_tag}, {'$set': {'count': plus_one}} )
            all_kanji.update_one( {'_id': ObjectId(id)}, {'$push': {'tags': new_tag}} )
        else:
            # throw error
            abort(404)

    # load page with item
    item = all_kanji.find_one( {'_id': ObjectId(id)} )
        
    # get API info on kanji
    item['extra'] = requests.get(KANJIAPI + item['symbol']).json()
    return render_template('item.html', kanji=item)


@app.post('/app/kanji/<id>/delete/<tag>')
def delete_tag(id, tag):
    # option to remove a tag
    if ObjectId.is_valid(tag):
        all_kanji.update_one( {'_id': ObjectId(id)}, { '$pull': { 'tags': tag }} )
    return redirect(url_for('item', id=id))


# make UI more appealing