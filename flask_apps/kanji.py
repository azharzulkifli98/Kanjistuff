from pydoc import describe
from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

client = MongoClient('localhost', 27017)

db = client.flask_db
all_kanji = db.kanjis

@app.route('/')
@app.route('/app/')
def index():
    return redirect('/app/all')


@app.route('/app/<tag>', methods=('GET', 'POST'))
def search(tag):
    payload = request.args.get('tag', default='', type=str)
    if tag == 'all' or tag == '':
        # default page
        kanji_found = list(all_kanji.find({}))
    else:
        # user searches by tag
        kanji_found = list(all_kanji.find( {'tags': payload} ))

    # user gets page
    return render_template('search.html', kanji_list=kanji_found)


@app.post('/app/add/')
def insert():
    # user adds a kanji using input forms
    symbol = request.form['symbol']
    description = request.form['description']
    all_kanji.insert_one({'symbol': symbol, 'description': description, 'tags': ['new', 'free']})
    return redirect('/app/all')


@app.post('/app/delete/<id>/')
def delete(id):
    # user deletes a kanji using object button
    all_kanji.delete_one({'_id': ObjectId(id)})
    return redirect('/app/all')


@app.route('/app/kanji/<id>', methods=('GET', 'POST'))
def item(id):
    # option to load page with new tag

    # option to load page without a tag
    item = all_kanji.find_one( {'_id': ObjectId(id)} )
    return render_template('item.html', kanji=item)



# add tag
# delete tag
# search by tag
# go home
# make UI more appealing
# add to github