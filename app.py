from flask import Flask

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

@app.get("/stores")
def get_stores():
    return {"stores":stores}