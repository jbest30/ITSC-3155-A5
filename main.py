from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

# Importing functions from the other files
from sandwiches import create_sandwich as create_sandwich_func, update_sandwich as update_sandwich_func, delete_sandwich as delete_sandwich_func, read_all_sandwiches as read_all_sandwiches_func, read_one_sandwich as read_one_sandwich_func
from resources import create_resource as create_resource_func, update_resource as update_resource_func, delete_resource as delete_resource_func, read_all_resources as read_all_resources_func, read_one_resource as read_one_resource_func
from recipes import create_recipe as create_recipe_func, update_recipe as update_recipe_func, delete_recipe as delete_recipe_func, read_all_recipes as read_all_recipes_func, read_one_recipe as read_one_recipe_func
from order_details import create_order_detail as create_order_detail_func, update_order_detail as update_order_detail_func, delete_order_detail as delete_order_detail_func, read_all_order_details as read_all_order_details_func, read_one_order_detail as read_one_order_detail_func

app = FastAPI()

# Orders

class Order(BaseModel):
    customer_name: str
    order_date: str

@app.post("/orders/", response_model=Order)
def create_order(order: Order):
    conn = sqlite3.connect('pythonsqlite.db')
    sql = ''' INSERT INTO orders(customer_name, order_date)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (order.customer_name, order.order_date))
    conn.commit()
    return order

@app.put("/orders/{order_id}", response_model=Order)
def update_order(order_id: int, order: Order):
    conn = sqlite3.connect('pythonsqlite.db')
    sql = ''' UPDATE orders
              SET customer_name = ? ,
                  order_date = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (order.customer_name, order.order_date, order_id))
    conn.commit()
    return order

@app.delete("/orders/{order_id}")
def delete_order(order_id: int):
    conn = sqlite3.connect('pythonsqlite.db')
    sql = 'DELETE FROM orders WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (order_id,))
    conn.commit()
    return {"message": "Order deleted"}

@app.get("/orders/", response_model=list[Order])
def read_all_orders():
    conn = sqlite3.connect('pythonsqlite.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders")
    rows = cur.fetchall()
    return [{"customer_name": row[1], "order_date": row[2]} for row in rows]

@app.get("/orders/{order_id}", response_model=Order)
def read_one_order(order_id: int):
    conn = sqlite3.connect('pythonsqlite.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders WHERE id=?", (order_id,))
    row = cur.fetchone()
    if row:
        return {"customer_name": row[1], "order_date": row[2]}
    raise HTTPException(status_code=404, detail="Order not found")

# Sandwihes

class Sandwich(BaseModel):
    name: str
    ingredients: str
    price: float

@app.post("/sandwiches/", response_model=Sandwich)
def create_sandwich(sandwich: Sandwich):
    return create_sandwich_func(sandwich)

@app.put("/sandwiches/{sandwich_id}", response_model=Sandwich)
def update_sandwich(sandwich_id: int, sandwich: Sandwich):
    return update_sandwich_func(sandwich_id, sandwich)

@app.delete("/sandwiches/{sandwich_id}")
def delete_sandwich(sandwich_id: int):
    return delete_sandwich_func(sandwich_id)

@app.get("/sandwiches/", response_model=list[Sandwich])
def read_all_sandwiches():
    return read_all_sandwiches_func()

@app.get("/sandwiches/{sandwich_id}", response_model=Sandwich)
def read_one_sandwich(sandwich_id: int):
    return read_one_sandwich_func(sandwich_id)

# Resources

class Resource(BaseModel):
    name: str
    quantity: int
    unit: str

@app.post("/resources/", response_model=Resource)
def create_resource(resource: Resource):
    return create_resource_func(resource)

@app.put("/resources/{resource_id}", response_model=Resource)
def update_resource(resource_id: int, resource: Resource):
    return update_resource_func(resource_id, resource)

@app.delete("/resources/{resource_id}")
def delete_resource(resource_id: int):
    return delete_resource_func(resource_id)

@app.get("/resources/", response_model=list[Resource])
def read_all_resources():
    return read_all_resources_func()

@app.get("/resources/{resource_id}", response_model=Resource)
def read_one_resource(resource_id: int):
    return read_one_resource_func(resource_id)

# Recipes

class Recipe(BaseModel):
    name: str
    ingredients: str
    instructions: str

@app.post("/recipes/", response_model=Recipe)
def create_recipe(recipe: Recipe):
    return create_recipe_func(recipe)

@app.put("/recipes/{recipe_id}", response_model=Recipe)
def update_recipe(recipe_id: int, recipe: Recipe):
    return update_recipe_func(recipe_id, recipe)

@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int):
    return delete_recipe_func(recipe_id)

@app.get("/recipes/", response_model=list[Recipe])
def read_all_recipes():
    return read_all_recipes_func()

@app.get("/recipes/{recipe_id}", response_model=Recipe)
def read_one_recipe(recipe_id: int):
    return read_one_recipe_func(recipe_id)

# Order Details

class OrderDetail(BaseModel):
    order_id: int
    sandwich_id: int
    quantity: int
    price: float

@app.post("/order_details/", response_model=OrderDetail)
def create_order_detail(order_detail: OrderDetail):
    return create_order_detail_func(order_detail)

@app.put("/order_details/{order_detail_id}", response_model=OrderDetail)
def update_order_detail(order_detail_id: int, order_detail: OrderDetail):
    return update_order_detail_func(order_detail_id, order_detail)

@app.delete("/order_details/{order_detail_id}")
def delete_order_detail(order_detail_id: int):
    return delete_order_detail_func(order_detail_id)

@app.get("/order_details/", response_model=list[OrderDetail])
def read_all_order_details():
    return read_all_order_details_func()

@app.get("/order_details/{order_detail_id}", response_model=OrderDetail)
def read_one_order_detail(order_detail_id: int):
    return read_one_order_detail_func(order_detail_id)
