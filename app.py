from src.logger import logging 
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

@app.get('/')
def home():
    return {"Data": "Testing"}

@app.get('/about')
def about():
    return {"Data": "About"}

class Item(BaseModel):
    name: str
    price: float

inventory = {
        1: {
                "name": "Milk",
                "price": 19.5
        }
}

@app.get('/get-item/{item_id}')
def get_item(item_id: int):
    logging.info("Logging get_item")
    return inventory[item_id]

@app.get('/get-by-name')
def get_item(name: str = None):
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
    return {"Data": "Not found"}

@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    logging.info("Logging create_item")
    if item_id in inventory:
        return {"Error": "Item ID already exists"}
    inventory[item_id] = {"name": item.name, "price": item.price}
    return inventory[item_id]

if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)
