import json

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.json.ensure_ascii


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text(50), nullable=False)
    last_name = db.Column(db.Text(50))
    age = db.Column(db.Integer)
    email = db.Column(db.Text(100))
    role = db.Column(db.Text(50), nullable=False)


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text(50), nullable=False)
    description = db.Column(db.Text(250), nullable=False)
    start_date = db.Column(db.Text(50), nullable=False)
    end_date = db.Column(db.Text(50))
    address = db.Column(db.Text(200), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer)
    executor_id = db.Column(db.Integer)


class Offer(db.Model):
    __tablename__ = 'offers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer)
    executor_id = db.Column(db.Integer)


db.drop_all()
db.create_all()

with open('data/orders_to_add.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    for line in data:
        order = Order(
            id=line["id"],
            name=line["name"],
            description=line["description"],
            start_date=line["start_date"],
            end_date=line["end_date"],
            address=line["address"],
            price=line["price"],
            customer_id=line["customer_id"],
            executor_id=line["executor_id"]
        )
        db.session.add(order)
        db.session.commit()

with open('data/offers_to_add.json', 'r', encoding='utf-8') as file:
    data = json.loads(file.read())
    for line in data:
        offer = Offer(
            id=line["id"],
            order_id=line["order_id"],
            executor_id=line["executor_id"]
        )
        db.session.add(offer)
        db.session.commit()

with open('data/users_to_add.json', 'r', encoding='utf-8') as file:
    data = json.loads(file.read())
    for line in data:
        user = User(
            id=line["id"],
            first_name=line["first_name"],
            last_name=line["last_name"],
            age=line["age"],
            email=line["email"],
            role=line["role"]
        )
        db.session.add(user)
        db.session.commit()

USERS = User.query.all()
ORDERS = Order.query.all()
OFFERS = Offer.query.all()


@app.route("/users", methods=["GET"])
def get_all_users():
    result = []
    for user_to_add in USERS:
        result.append(
            {
                "id": user_to_add.id,
                "first_name": user_to_add.first_name,
                "last_name": user_to_add.last_name,
                "age": user_to_add.age,
                "email": user_to_add.email,
                "role": user_to_add.role
            }
        )
    return jsonify(result)


@app.route("/users", methods=["POST"])
def add_user():
    user_data = request.json
    new_user = User(
                id=user_data.get("id"),
                first_name=user_data.get("first_name"),
                last_name=user_data.get("last_name"),
                age=user_data.get("age"),
                email=user_data.get("email"),
                role=user_data.get("role")
    )
    db.session.add(new_user)
    db.session.commit()


@app.route("/users/<int:uid>", methods=["GET"])
def get_user_by_id(uid):
    user_by_id = User.query.get(uid)
    result = [
        {
            "id": user_by_id.id,
            "first_name": user_by_id.first_name,
            "last_name": user_by_id.last_name,
            "age": user_by_id.age,
            "email": user_by_id.email,
            "role": user_by_id.role,
        }
    ]
    return jsonify(result)


@app.route("/users/<int:uid>", methods=["PUT"])
def update_user(uid):
    user_by_id = User.query.get(uid)
    with db.session.begin():
        user_by_id.id = request.form["id"]
        user_by_id.first_name = request.form["first_name"]
        user_by_id.last_name = request.form["last_name"]
        user_by_id.age = request.form["age"]
        user_by_id.email = request.form["email"]
        user_by_id.role = request.form["role"]


@app.route("/users/<int:uid>", methods=["DELETE"])
def delete_user(uid):
    user_by_id = User.query.get(uid)
    db.session.delete(user_by_id)
    db.session.commit()


@app.route("/orders", methods=["GET"])
def get_all_orders():
    result = []
    for order_to_add in ORDERS:
        result.append(
            {
                "id": order_to_add.id,
                "name": order_to_add.name,
                "description": order_to_add.description,
                "star_date": order_to_add.start_date,
                "end_date": order_to_add.end_date,
                "address": order_to_add.address,
                "price": order_to_add.price,
                "customer_id": order_to_add.customer_id,
                "executor_id": order_to_add.executor_id
            }
        )
    return jsonify(result)


@app.route("/orders", methods=["POST"])
def add_order():
    order_data = request.json
    with db.session.begin():
        new_order = Order(
            name=order_data.get('name'),
            description=order_data.get('description'),
            start_date=order_data.get('start_date'),
            end_date=order_data.get('end_date'),
            address=order_data.get('address'),
            price=order_data.get('price'),
            customer_id=order_data.get('customer_id')
        )
        db.session.add(new_order)


@app.route("/orders/<int:oid>", methods=["GET"])
def get_order_by_id(oid):
    order_by_id = Order.query.get(oid)
    result = [
        {
            "id": order_by_id.id,
            "name": order_by_id.name,
            "description": order_by_id.description,
            "star_date": order_by_id.start_date,
            "end_date": order_by_id.end_date,
            "address": order_by_id.address,
            "price": order_by_id.price,
            "customer_id": order_by_id.customer_id,
            "executor_id": order_by_id.executor_id
        }
    ]
    return jsonify(result)


@app.route("/orders/<int:oid>", methods=["PUT"])
def update_order(oid):
    order_by_id = Order.query.get(oid)
    order_by_id.name = request.form['name']
    order_by_id.description = request.form['description']
    order_by_id.start_date = request.form['start_date']
    order_by_id.end_date = request.form['end_date']
    order_by_id.address = request.form['address']
    order_by_id.price = request.form['price']
    order_by_id.customer_id = request.form['customer_id']
    order_by_id.executor_id = request.form['executor_id']
    db.session.commit()


@app.route("/orders/<int:oid>", methods=["DELETE"])
def delete_order(oid):
    order_by_id = Order.query.get(oid)
    db.session.delete(order_by_id)
    db.session.commit()


@app.route("/offers", methods=["GET"])
def get_all_offers():
    result = []
    for offer_to_add in OFFERS:
        result.append(
            {
                "id": offer_to_add.id,
                "order_id": offer_to_add.order_id,
                "executor_id": offer_to_add.executor_id
            }
        )
    return result


@app.route("/offers", methods=["POST"])
def add_new_offer():
    offer_data = request.json
    new_offer = Offer(
        order_id=offer_data.get("order_id"),
        executor_id=offer_data.get("executor_id")
    )
    db.session.add(new_offer)
    db.session.commit()


@app.route("/offers/<int:of_id>", methods=["GET"])
def get_offer_by_id(of_id):
    offer_by_id = Offer.query.get(of_id)
    result = [
        {
            "id": offer_by_id.id,
            "order_id": offer_by_id.order_id,
            "executor_id": offer_by_id.executor_id
        }
    ]
    return jsonify(result)


@app.route("/offers/<int:of_id>", methods=["PUT"])
def update_offer(of_id):
    offer_by_id = Offer.query.get(of_id)
    offer_by_id.order_id = request.form['order_id']
    offer_by_id.executor_id = request.form['executor_id']
    db.session.commit()


@app.route("/offers/<int:of_id>", methods=["DELETE"])
def delete_offer(of_id):
    offer_by_id = Offer.query.get(of_id)
    db.session.delete(offer_by_id)
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
