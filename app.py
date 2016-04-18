from flask import Flask, render_template, request, redirect, url_for, flash
from models.featurerequest import FeatureRequest, Client, ProductCategory
from models.basemodel import db
import peewee
import json
import datetime

app = Flask(__name__)
app.secret_key = "123"

def create_feature_request(data):
        new_fr = FeatureRequest()
        new_fr.title = data.get('title')
        new_fr.description = data.get('description')
        new_fr.client = Client.select(Client.id == data.get('client'))
        new_fr.client_priority = data.get('client_priority')

        try:
            new_fr.target_date = datetime.datetime.strptime(data.get('target_date'), "%m/%d/%Y")
        except ValueError:
            flash('Target date is invalid.', 'error')

        new_fr.ticket_url = data.get('ticket_url')
        new_fr.category = ProductCategory.select(ProductCategory.id == data.get('category'))
        new_fr.save()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/feature_request/create', methods=["GET", "POST"])
def feature_request_create():
    if request.method == "POST":
        create_feature_request(request.form)

        return redirect(url_for('feature_request_create'))
    else:
        clients = Client.select()
        categories = ProductCategory.select()
        return render_template('create_feature_request.html',
                               clients=clients,
                               categories=categories)

@app.route('/client/create', methods=["GET", "POST"])
def client_create():
    return render_template('create_client.html')

@app.route('/category/create', methods=["GET", "POST"])
def category_create():
    return render_template('create_category.html')

@app.route('/init')
def init():
    try:

        db.create_tables([FeatureRequest, Client, ProductCategory])

        for i in range(3):
            client_name = "Client {}".format(chr(ord('A') + i))
            temp_client = Client.create(name=client_name)

        categories = ['Policies', 'Billing', 'Claims', 'Support']

        for category in categories:
            ProductCategory.create(name=category)

        return "Database initialized."

    except peewee.OperationalError as e:
        if 'already exists' in str(e):
            return redirect(url_for('index'))
        else:
            raise e

if __name__ == '__main__':
    app.debug = True
    app.run()

