class Recipe(BaseModel):
    name: str
    ingredients: str
    instructions: str

@app.post("/recipes/", response_model=Recipe)
def create_recipe(recipe: Recipe):
    conn = sqlite3.connect('pythonsqlite.db')
    sql = ''' INSERT INTO recipes(name, ingredients, instructions)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (recipe.name, recipe.ingredients, recipe.instructions))
    conn.commit()
    return recipe

@app.put("/recipes/{recipe_id}", response_model=Recipe)
def update_recipe(recipe_id: int, recipe: Recipe):
    conn = sqlite3.connect('pythonsqlite.db')
    sql = ''' UPDATE recipes
              SET name = ? ,
                  ingredients = ? ,
                  instructions = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (recipe.name, recipe.ingredients, recipe.instructions, recipe_id))
    conn.commit()
    return recipe

@app.delete("/recipes/{recipe_id}")
def delete_recipe(recipe_id: int):
    conn = sqlite3.connect('pythonsqlite.db')
    sql = 'DELETE FROM recipes WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (recipe_id,))
    conn.commit()
    return {"message": "Recipe deleted"}

@app.get("/recipes/", response_model=list[Recipe])
def read_all_recipes():
    conn = sqlite3.connect('pythonsqlite.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM recipes")
    rows = cur.fetchall()
    return [{"name": row[1], "ingredients": row[2], "instructions": row[3]} for row in rows]

@app.get("/recipes/{recipe_id}", response_model=Recipe)
def read_one_recipe(recipe_id: int):
    conn = sqlite3.connect('pythonsqlite.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM recipes WHERE id=?", (recipe_id,))
    row = cur.fetchone()
    if row:
        return {"name": row[1], "ingredients": row[2], "instructions": row[3]}
    raise HTTPException(status_code=404, detail="Recipe not found")
