from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Card, card_schema, cards_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return ['is', 'this', 'working', '?']

@api.route('/cards', methods = ['POST'])
@token_required
def create_card(current_user_token):
    card_number = request.json['card_number']
    expiration_date = request.json['expiration_date']
    cvv = request.json['cvv']
    name = request.json['name']
    zip_code = request.json['zip_code']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token}')

    card = Card(card_number, expiration_date, cvv, name, zip_code, user_token= user_token)

    db.session.add(card)
    db.session.commit()

    response = card_schema.dump(card)
    return jsonify(response)

@api.route('/cards', methods = ['GET'])
@token_required
def get_cards(current_user_token):
    a_user = current_user_token.token
    cards = Card.query.filter_by(user_token = a_user).all()
    response = cards_schema.dump(cards)
    return jsonify(response)

@api.route('/cards/<id>', methods = ['GET'])
@token_required
def get_single_card(current_user_token, id):
    card = Card.query.get(id)
    response = card_schema.dump(card)
    return jsonify(response)

@api.route('/cards/<id>', methods = ['POST','PUT'])
@token_required
def update_card(current_user_token,id):
    card = Card.query.get(id)
    card.card_number = request.json['card_number']
    card.expiration_date = request.json['expiration_date']
    card.cvv = request.json['cvv']
    card.name = request.json['name']
    card.zip_code = request.json['zip_code']
    card.user_token = current_user_token.token

    db.session.commit()
    response = card_schema.dump(card)
    return jsonify(response)

@api.route('/cards/<id>', methods = ['DELETE'])
@token_required
def delete_card(current_user_token,id):
    card = Card.query.get(id)
    db.session.delete(card)
    db.session.commit()
    response = card_schema.dump(card)
    return jsonify(response)