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

@app.post("/store")
def create_store():
    # se almacena el json en un diccionario
    request_data = request.get_json()
    new_store = {"name" : request_data["name"], "items" : []}
    stores.append(new_store)
    return new_store, 201