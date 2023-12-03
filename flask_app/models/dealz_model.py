from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import users_model


db = 'cardealz'

class Dealz:
    def __init__(self, data):
        self.id = data['id']
        self.price = data['price']
        self.model = data['model']
        self.make = data['make']
        self.year = data['year']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['user_id']
        self.seller = []

    @staticmethod
    def validate_dealz(dealz):
        is_valid = True
        if dealz['price'] == 0:
            flash("Price can not be 0!")
            is_valid = False
        if dealz['model'] == "":
            flash("Please indicate a model!")
            is_valid = False
        if dealz['make'] == "":
            flash("Please indicate a manufacturer!")
            is_valid = False
        if dealz['year'] == 0:
            flash("Please indicate the year!")
            is_valid = False
        if len(dealz['description']) < 5:
            flash("Please write a more detailed description")
            is_valid = False
        return is_valid


    @classmethod
    def get_dealz(cls):
        query = "SELECT * FROM dealz;"
        result = connectToMySQL(db).query_db(query)
        dealz = []
        for deal in result:
            dealz.appent(cls(deal))
        return dealz
    
    @classmethod
    def get_dealz_from_user(cls):
        query = "SELECT * FROM dealz LEFT JOIN users ON dealz.user_id = users.id;"
        result = connectToMySQL(db).query_db(query)
        dealz_from_user = []
        for deal in result:
            dealz = cls(deal)
            dealz_info = {
                'id': deal['users.id'],
                'first_name': deal['first_name'],
                'last_name': deal['last_name'],
                'email': deal['email'],
                'password': deal['password'],
                'created_at': deal['users.created_at'],
                'updated_at': deal['users.updated_at'],
            }
            dealz.seller.append(users_model.User(deal))
            dealz_from_user.append(dealz)
        return dealz_from_user

    @classmethod
    def save_dealz(cls, data):
        query = "INSERT INTO dealz (price, model, make, year, description, user_id) VALUES (%(price)s, %(model)s, %(make)s, %(year)s, %(description)s, %(id)s);"
        result = connectToMySQL(db).query_db(query, data)
        return result
    
    @classmethod
    def get_dealz_by_user_id(cls, data):
        query = "SELECT * FROM dealz LEFT JOIN users ON dealz.user_id = users.id WHERE dealz.id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        dealz_from_user = []
        for deal in result:
            dealz = cls(deal)
            dealz_info = {
                'id': deal['users.id'],
                'first_name': deal['first_name'],
                'last_name': deal['last_name'],
                'email': deal['email'],
                'password': deal['password'],
                'created_at': deal['users.created_at'],
                'updated_at': deal['users.updated_at']
            }
            dealz.seller.append(users_model.User(deal))
            dealz_from_user.append(dealz)
        return dealz_from_user

    @classmethod
    def update_dealz(cls, data):
        query = "UPDATE dealz SET price = %(price)s, model = %(model)s, make = %(make)s, year = %(year)s, description = %(description)s WHERE id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        return result
    
    @classmethod
    def delete_dealz(cls, data):
        query = "DELETE FROM dealz WHERE dealz.id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        return result