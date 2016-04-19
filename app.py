from flask import Flask, render_template, request, redirect, url_for, flash
from models.featurerequest import FeatureRequest, Client, ProductCategory
from models.basemodel import db
import peewee
import json
import datetime

app = Flask(__name__)
app.secret_key = "123" #this would be a more secure random string in a real application

def ensure_priorities(client, new_priority):
    requests = (FeatureRequest
                .select()
                .where(FeatureRequest.client == client,
                       FeatureRequest.client_priority >= new_priority)
                .order_by(FeatureRequest.client_priority))

    #shift all requests with the same or lower priority by 1,
    #so the new one can fit in the middle
    for request in requests:
        request.client_priority += 1
        request.save()

def create_feature_request(data):
        '''Validate form data and create a feature request while
        ensuring priority order is maintained'''
        error_occurred = False

        new_fr = FeatureRequest()
        new_fr.title = data.get('title')
        new_fr.description = data.get('description')

        try:
            new_fr.client = Client.get(Client.id == data.get('client'))
        except peewee.ClientDoesNotExist as e:
            flash('Selected client does not exist.', 'danger')
            error_occurred = True

        new_fr.client_priority = data.get('client_priority')

        try:
            new_fr.target_date = datetime.datetime.strptime(data.get('target_date'), "%m/%d/%Y")
        except ValueError:
            flash('Target date is invalid.', 'danger')
            error_occurred = True

        new_fr.ticket_url = data.get('ticket_url')

        try:
            new_fr.category = ProductCategory.get(ProductCategory.id == data.get('category'))
        except peewee.ProductCategoryDoesNotExist as e:
            flash('Selected category does not exist.', 'danger')
            error_occurred = True

        if not error_occurred:
            flash('Feature request added.', 'success')
            ensure_priorities(new_fr.client, new_fr.client_priority)
            new_fr.save()

        return error_occurred

@app.route('/')
def index():
    feature_requests = FeatureRequest.select()
    return render_template('index.html', feature_requests=feature_requests)

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
    ''' Initializes the database file and structure
        with example data. '''

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

