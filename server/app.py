#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():

    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

    response = make_response(
        bakeries_serialized,
        200
    )
    return response


# Define a PATCH block inside of the /bakeries/<int:id> route that updates the name of the bakery in the database and returns its data as JSON. As with the previous POST block, the request will send data in a form. The form does not need to include values for all of the bakery's attributes.

@app.route('/bakeries/<int:id>', methods=["GET", "PATCH"])
def bakery_by_id(id):

    if request.method == "GET":
        bakery = Bakery.query.filter_by(id=id).first()
        bakery_serialized = bakery.to_dict()

        response = make_response(
            bakery_serialized,
            200
        )
        return response
    
    elif request.method == "PATCH":
        bakery = Bakery.query.filter_by(id=id).first()

        for name in request.form:
            setattr(bakery, name, request.form.get(name))

        db.session.add(bakery)
        db.session.commit()

        bakery_dict = bakery.to_dict()
        res = make_response(bakery_dict, 200)

        return res


# Define a POST block inside of a /baked_goods route that creates a new baked good in the database and returns its data as JSON. The request will send data in a form.
#Attributes in BakedGood class: id, name, price, bakery_id
@app.route('/baked_goods', methods=["GET", "POST"])
def baked_goods():
    # goodies = BakedGood.query.all()
    if request.method == "GET":
    
        goodies_dict = [goodie.to_dict() for goodie in BakedGood.query.all()]

        res = make_response(goodies_dict, 200)
        return res

    elif request.method == "POST":

        new_goodie = BakedGood(
            name=request.form.get("name"),
            price=request.form.get("price"),
            bakery_id=request.form.get("bakery_id")
        ) 

        db.session.add(new_goodie)
        db.session.commit()

        goodie_dict = new_goodie.to_dict()
        res = make_response(goodie_dict, 201)

        return res


# Define a DELETE block inside of a /baked_goods/<int:id> route that deletes the baked good from the database and returns a JSON message confirming that the record was successfully deleted.
@app.route('/baked_goods/<int:id>', methods=["GET", "DELETE"])
def baked_goodies(id):
    goodie = BakedGood.query.filter(BakedGood.id == id).first()
    if request.method == "GET":
        goodie_dict = goodie.to_dict()

        res = make_response(goodie_dict, 200)
        return res

    elif request.method == "DELETE":
        
        db.session.delete(goodie)
        db.session.commit()

        response_body={
            "delete_successful": True,
            "message":"Goodie has been deleted"
        }

        res = make_response(response_body, 200)
        return res


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    
    response = make_response(
        baked_goods_by_price_serialized,
        200
    )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()

    response = make_response(
        most_expensive_serialized,
        200
    )
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
