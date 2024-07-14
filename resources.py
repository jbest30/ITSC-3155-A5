class Resource(BaseModel):
    name: str
    quantity: int
    unit: str

@app.post("/resources/", response_model=Resource)
def create_resource(resource: Resource):
    conn = sqlite3.connect('pythonsqlite.db')
    sql = ''' INSERT INTO resources(name, quantity, unit)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (resource.name, resource.quantity, resource.unit))
    conn.commit()
    return resource

@app.put("/resources/{resource_id}", response_model=Resource)
def update_resource(resource_id: int, resource: Resource):
    conn = sqlite3.connect('pythonsqlite.db')
    sql = ''' UPDATE resources
              SET name = ? ,
                  quantity = ? ,
                  unit = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (resource.name, resource.quantity, resource.unit, resource_id))
    conn.commit()
    return resource

@app.delete("/resources/{resource_id}")
def delete_resource(resource_id: int):
    conn = sqlite3.connect('pythonsqlite.db')
    sql = 'DELETE FROM resources WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (resource_id,))
    conn.commit()
    return {"message": "Resource deleted"}

@app.get("/resources/", response_model=list[Resource])
def read_all_resources():
    conn = sqlite3.connect('pythonsqlite.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM resources")
    rows = cur.fetchall()
    return [{"name": row[1], "quantity": row[2], "unit": row[3]} for row in rows]

@app.get("/resources/{resource_id}", response_model=Resource)
def read_one_resource(resource_id: int):
    conn = sqlite3.connect('pythonsqlite.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM resources WHERE id=?", (resource_id,))
    row = cur.fetchone()
    if row:
        return {"name": row[1], "quantity": row[2], "unit": row[3]}
    raise HTTPException(status_code=404, detail="Resource not found")
