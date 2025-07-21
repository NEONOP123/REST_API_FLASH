from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# In-memory data
stores = [
    {
        "name": "My Python Project",
        "items": [
            {
                "name": "My Efforts",
                "price": 9.69
            }
        ]
    }
]

# Home page (renders HTML)
@app.route("/")
def home():
    return render_template("index.html")  # Make sure index.html exists in a /templates folder

# POST /store → create a new store
@app.route("/store", methods=["POST"])
def create_store():
    request_data = request.get_json()
    if not request_data or "name" not in request_data:
        return jsonify({"error": "Invalid store data"}), 400

    new_store = {
        "name": request_data["name"],
        "items": []
    }
    stores.append(new_store)
    return jsonify(new_store), 201

# GET /store/<string:name> → get a specific store
@app.route("/store/<string:name>", methods=["GET"])
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return jsonify(store)
    return jsonify({"message": "Store not found"}), 404

# GET /store → get all stores
@app.route("/store", methods=["GET"])
def get_stores():
    return jsonify({"stores": stores})

# POST /store/<string:name>/item → add item to a store
@app.route("/store/<string:name>/item", methods=["POST"])
def create_item_in_store(name):
    request_data = request.get_json()
    if not request_data or "name" not in request_data or "price" not in request_data:
        return jsonify({"error": "Invalid item data"}), 400

    for store in stores:
        if store["name"] == name:
            new_item = {
                "name": request_data["name"],
                "price": request_data["price"]
            }
            store["items"].append(new_item)
            return jsonify(new_item), 201
    return jsonify({"message": "Store not found"}), 404

# GET /store/<string:name>/item → get items from a store
@app.route("/store/<string:name>/item", methods=["GET"])
def get_items_in_store(name):
    for store in stores:
        if store["name"] == name:
            return jsonify({"items": store["items"]})
    return jsonify({"message": "Store not found"}), 404

# Run the app
if __name__ == "__main__":
    app.run(port=5000, debug=True)
