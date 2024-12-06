from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db_config import get_connection
from Crypto.Cipher import AES
import base64
import os

app = Flask(__name__)

# AES Encryption Key and IV (used to encrypt card data)
key = os.urandom(16)  # Save this securely; regenerate for production
iv = os.urandom(16)

# Encryption Functions
def encrypt_data(data):
    """Encrypt data using AES (Advanced Encryption Standard)"""
    cipher = AES.new(key, AES.MODE_CFB, iv)
    encrypted = base64.b64encode(cipher.encrypt(data.encode()))
    return encrypted.decode()

def decrypt_data(encrypted_data):
    """Decrypt data using AES"""
    cipher = AES.new(key, AES.MODE_CFB, iv)
    decrypted = cipher.decrypt(base64.b64decode(encrypted_data.encode()))
    return decrypted.decode()

# Root Route for Base URL
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the E-Commerce API! Use /register, /login, /process_payment, or /search_product"}), 200

# User Registration (POST /register)
@app.route('/register', methods=['POST'])
def register():
    try:
        # Parse user input
        data = request.json
        username = data['username']
        password = generate_password_hash(data['password'])
        email = data['email']
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        address = data.get('address', '')
        phone_number = data.get('phone_number', '')

        conn = get_connection()
        cursor = conn.cursor()

        # Insert user into database, handle duplicate email
        try:
            cursor.execute(
                """
                INSERT INTO users (username, password_hash, email, first_name, last_name, address, phone_number)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (username, password, email, first_name, last_name, address, phone_number)
            )
            conn.commit()
            return jsonify({"message": "User registered successfully!"}), 201

        except Exception as e:
            if "Duplicate entry" in str(e) and "email" in str(e):
                return jsonify({"error": "Email already exists. Please use a different email."}), 400
            return jsonify({"error": str(e)}), 500

        finally:
            conn.close()

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# User Login (POST /login)
@app.route('/login', methods=['POST'])
def login():
    try:
        # Parse user input
        data = request.json
        email = data['email']
        password = data['password']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[0], password):
            return jsonify({"message": "Login successful!"}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Process Payment (POST /process_payment)
@app.route('/process_payment', methods=['POST'])
def process_payment():
    try:
        # Parse payment details
        data = request.json
        user_id = data['user_id']
        product_id = data['product_id']
        quantity = data['quantity']
        total_price = data['total_price']
        shipping_address = data['shipping_address']
        card_data = data['card_data']

        # Encrypt the card data
        encrypted_card = encrypt_data(card_data)

        # Insert order into database
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO orders (user_id, product_id, quantity, total_price, shipping_address, encrypted_card_data)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (user_id, product_id, quantity, total_price, shipping_address, encrypted_card)
        )
        conn.commit()
        conn.close()

        return jsonify({"message": "Payment processed securely!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Secure Query Example (GET /search_product)
@app.route('/search_product', methods=['GET'])
def search_product():
    try:
        # Get product name from query parameter
        product_name = request.args.get('product_name')

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE name = %s", (product_name,))
        products = cursor.fetchall()
        conn.close()

        if products:
            return jsonify(products), 200
        else:
            return jsonify({"message": "No products found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
