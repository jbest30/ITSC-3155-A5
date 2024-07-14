class OrderDetail(BaseModel):
    order_id: int
    sandwich_id: int
    quantity: int
    price: float

@app.post("/order_details/", response_model=OrderDetail)
def create_order_detail(order_detail: OrderDetail):
    conn = sqlite3.connect('pythonsqlite.db')
    sql = ''' INSERT INTO order_details(order_id, sandwich_id, quantity, price)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (order_detail.order_id, order_detail.sandwich_id, order_detail.quantity, order_detail.price))
    conn.commit()
    return order_detail

@app.put("/order_details/{order_detail_id}", response_model=OrderDetail)
def update_order_detail(order_detail_id: int, order_detail: OrderDetail):
    conn = sqlite3.connect('pythonsqlite.db')
    sql = ''' UPDATE order_details
              SET order_id = ? ,
                  sandwich_id = ? ,
                  quantity = ? ,
                  price = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (order_detail.order_id, order_detail.sandwich_id, order_detail.quantity, order_detail.price, order_detail_id))
    conn.commit()
    return order_detail

@app.delete("/order_details/{order_detail_id}")
def delete_order_detail(order_detail_id: int):
    conn = sqlite3.connect('pythonsqlite.db')
    sql = 'DELETE FROM order_details WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (order_detail_id,))
    conn.commit()
    return {"message": "Order detail deleted"}

@app.get("/order_details/", response_model=list[OrderDetail])
def read_all_order_details():
    conn = sqlite3.connect('pythonsqlite.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM order_details")
    rows = cur.fetchall()
    return [{"order_id": row[1], "sandwich_id": row[2], "quantity": row[3], "price": row[4]} for row in rows]

@app.get("/order_details/{order_detail_id}", response_model=OrderDetail)
def read_one_order_detail(order_detail_id: int):
    conn = sqlite3.connect('pythonsqlite.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM order_details WHERE id=?", (order_detail_id,))
    row = cur.fetchone()
    if row:
        return {"order_id": row[1], "sandwich_id": row[2], "quantity": row[3], "price": row[4]}
    raise HTTPException(status_code=404, detail="Order detail not found")
