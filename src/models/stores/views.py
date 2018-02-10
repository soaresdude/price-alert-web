from flask import Blueprint, render_template, request, json, redirect, url_for

from models.stores.store import Store

store_blueprint = Blueprint('stores', __name__)

@store_blueprint.route('/')
def index():
    stores = Store.all()
    return render_template('stores/store_index.jinja2', stores=stores)

@store_blueprint.route('/store/<string:store_id>')
def store_page(store_id):
    return render_template('stores/store.jinja2', store=Store.find_one_store(query_name="_id", query=store_id))


@store_blueprint.route('/new', methods=['POST', 'GET'])
def create_store():
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])   # converts the string from request into a python dictionary to be used with beautiful soup

        Store(name, url_prefix, tag_name, query).save_to_mongo()

        return redirect(url_for('.index'))
    return render_template('stores/new_store.jinja2')

@store_blueprint.route('/edit/<string:store_id>', methods=['POST', 'GET'])
def edit_store(store_id):
    store = Store.find_one_store(query_name="_id", query=store_id)

    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])

        store.name = name
        store.url_prefix = url_prefix
        store.tag_name = tag_name
        store.query = query

        store.save_to_mongo()

        return redirect(url_for('.index'))
    return render_template('stores/edit_store.jinja2', store=store)


@store_blueprint.route('/delete/<string:store_id>')
def delete_store(store_id):
    Store.find_one_store("_id", store_id).delete()
    return redirect(url_for('.index'))