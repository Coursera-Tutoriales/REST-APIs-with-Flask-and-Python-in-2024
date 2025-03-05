from flask import Flask, request

# se crea una instancia de Flask en app
app = Flask(__name__)

stores = [
    {
        "name":"Tienda1",
        "items":[
            {
                "name":"Chair",
                "price":1500
            }
        ]
    }
]

@app.get("/store")
def get_stores():
    return {"stores":stores}

@app.get("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return store, 201
    return {"message" : "Store not found"}, 404

@app.post("/store")
def create_store():
    # se almacena el json en un diccionario
    request_data = request.get_json()
    new_store = {"name" : request_data["name"], "items" : []}
    stores.append(new_store)
    return new_store, 201

@app.post("/store/<string:name>/item")
def create_item_in_store(name):
    # se almacena el json en un diccionario
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201
    return {"message" : "Store not found"}, 404

@app.get("/store/<string:name>/item")
def get_items_in_store(name):
    for store in stores:
        if store["name"] == name:            
            return {"items":store["items"]}, 201
    return {"message" : "Store not found"}, 404