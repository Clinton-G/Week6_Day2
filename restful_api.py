from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
import mysql.connector

app = Flask(__name__)
marsh = Marshmallow(app)

db_connection = mysql.connector.connect(
    host="localhost",
    user="clintongoin",
    password="password123",
    database="database"
)

class BookSchema(marsh.Schema):
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    genre = fields.Str(required=True)
    year = fields.Int(required=True)

book_schema = BookSchema()

@app.route('/books', methods=['POST'])
def add_book():
    book_data = request.json

    try:
        validated_data = book_schema.load(book_data)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    cursor = db_connection.cursor()
    insert_query = "INSERT INTO books (title, author, genre, year) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (
        validated_data['title'],
        validated_data['author'],
        validated_data['genre'],
        validated_data['year']
    ))
    db_connection.commit()
    cursor.close()

    return jsonify({'added successfully'}), 201

@app.route('/books', methods=['Post'])
def add_book():
    return "Welcome to the Books API"

if __name__ == '__main__':
    app.run(debug=True)