import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('price',
        type=float,
        required=True,
        help="This field cannot left black!"
    )

    @jwt_required()
    def get(self, name):
       item = self.find_by_name(name)

       if item:
           return item
       return {'Message': {'Item not found'}}, 404


    @classmethod
    def find_by_name(cls, name):
       conn = sqlite3.connect('data.db')
       cursor = conn.cursor()

       query = "SELECT * FROM items WHERE name=?"
       result = cursor.execute(query, (name,))
       row = result.fetchone()
       conn.close()
       
       if row:
           return {'Item': {'name': row[0], 'price': row[1]}}
       

    def post(self, name):        
        if self.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parse.parse_args()
    
        item = {'name': name, 'price': data['price']}

        try:
            self.insert(item)
        except:
            return {'Message': 'An error occured inserting the item'}, 500
        
        return item, 201


    @classmethod
    def insert(cls, item):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        conn.commit()
        conn.close()
    

    @classmethod
    def update(cls, item):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        query = "UPDATE INTO SET price=? WHERE name=?"
        cursor.execute(query, (item['price'], item['name']))

        conn.commit()
        conn.close()


    def delete(self, name):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        conn.commit()
        conn.close()
        
        return {'message' : 'Item deleted'}


    def put(self, name):
        data = Item.parse.parse_args()

        item = self.find_by_name(name)
        update_item = {'name': name, 'price': data['price']}

        if item is None:
            try:
                self.insert(update_item)
            except:
                return {'Message': 'An error occured inserting the item'}, 500
        else:
            try:
                self.update(update_item)
            except:
                return {'Message': 'An error occured updating the item'}, 500
        return update_item        


class ItemList(Resource):
    def get(self):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append(row)

        conn.close()
        return {'Items': items}