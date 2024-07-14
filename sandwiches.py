from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Sandwiches

class Sandwich(BaseModel):
    name: str
    ingredients: str
    price: float

@app.post("/sandwiches/", response_model=Sandwich)
def create_sandwich(sandwich: Sandwich):
    conn = sqlite3.connect('pythonsqlite.db')
    sql = ''' INSERT INTO sandwiches(name, ingredients, price)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (sandwich.name, sandwich.ingredients, sandwich.price))
    conn.commit()
    return sandwich

@app.put("/sandwiches/{sandwich_id}", response_model=Sandwich)
def update_sandwich(sandwich_id: int, sandwich: Sandwich):
    conn = sqlite3.connect('pythonsqlite.db')
    sql = ''' UPDATE sandwiches
              SET name = ? ,
                  ingredients = ? ,
                  price = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (sandwich.name, sandwich.ingredients, sandwich.price, sandwich_id))
    conn.commit()
    return sandwich

@app.delete("/sandwiches/{sandwich_id}")
def delete_sandwich(sandwich_id: int):
    conn = sqlite3.connect('pythonsqlite.db')
    sql = 'DELETE FROM sandwiches WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (sandwich_id,))
    conn.commit()
    return {"message": "Sandwich deleted"}

@app.get("/sandwiches/", response_model=list[Sandwich])
def read_all_sandwiches():
    conn = sqlite3.connect('pythonsqlite.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM sandwiches")
    rows = cur.fetchall()
    return [{"name": row[1], "ingredients": row[2], "price": row[3]} for row in rows]

@app.get("/sandwiches/{sandwich_id}", response_model=Sandwich)
def read_one_sandwich(sandwich_id: int):
    conn = sqlite3.connect('pythonsqlite.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM sandwiches WHERE id=?", (sandwich_id,))
    row = cur.fetchone()
    if row:
        return {"name": row[1], "ingredients": row[2], "price": row[3]}
    raise HTTPException(status_code=404, detail="Sandwich not found")
