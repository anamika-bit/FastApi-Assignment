from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict,Optional

app = FastAPI()

#Database to store items
db = {}

class Item(BaseModel):
    name: str
    price: float
    quantity: int


#Routes
@app.get("/items/{item_id}")
def get_item_by_id(item_id: int):
    item = db.get(item_id)
    if not item:
        raise HTTPException(status_code=404,detail="Item not found")
    return item


@app.get("/items")
def get_items():
    return db


@app.post("/items")
def create_item(item: Item):
    item_id = len(db) + 1
    db[item_id] = item.dict()
    return {"item": db[item_id]}



@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    db[item_id] = item.dict()
    return { "item" : db[item_id] }


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    del db[item_id]
    return {"message" : "Item deleted"}


@app.post("/inventory")
def manage_inventory(inventory: Dict[int,int]):
    for item_id,quantity in inventory.items():
        if item_id not in db:
            raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
        if quantity < 0:
            raise HTTPException(status_code=400, detail="Invalid quantity")
        db[item_id]['quantity'] = quantity
    return {"message" : "Inventory updated"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app,host="0.0.0.0",port=8000)

