from flask import Flask,render_template,request,redirect,flash
import sqlite3

app = Flask(__name__)
app.secret_key = "3535abc123"
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/add_product", methods=["GET","POST"])
def addproduct():
    if request.method=="POST":
        name = request.form["name"]
        price = request.form["price"]
        quantity = request.form["quantity"]

        conn = sqlite3.connect("database.db")
        cursor=conn.cursor()

        cursor.execute(
        "insert into product(name,price,quantity)values(?,?,?)",(name,price,quantity)
        )
        conn.commit()
        conn.close()

        flash("Product Added Successfully!")
        return  redirect("/products")
    return render_template("add_product.html")

def init_db():
    conn = sqlite3.connect("database.db")
    cursor=conn.cursor()
    cursor.execute("""
    create table if not exists product(
    id integer primary key autoincrement,
    name text,
    price integer,
    quantity integer)
    """)
    conn.commit()
    conn.close()
@app.route("/products")
def displayproducts():
    conn = sqlite3.connect("database.db")
    cursor=conn.cursor()
    cursor.execute("select * from product")
    data = cursor.fetchall()
    conn.close()
    return render_template("products.html",product=data)#the product is a list ,data is come from products.html
@app.route("/delete/<int:id>")
def deleteitems(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("delete from product where id= ?",(id,))
    conn.commit()
    conn.close()
    flash("Product Deleted Succesfully")
    return redirect("/products")

@app.route("/update/<int:id>/",methods=["GET","POST"])
def update(id):
    if request.method == "POST":
        price = request.form["price"]
        quantity = request.form["quantity"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("update product set price = ?,quantity = ? where id =?",(price,quantity,id))
        conn.commit()
        conn.close()
        flash("Product Update Succesfully")
        return redirect("/products")
    return render_template("update.html")
@app.route("/billing")
def billit():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("select * from product")
    data=cursor.fetchall()
    conn.commit()
    conn.close()
    return render_template("billing.html",product=data)#product is database table name

init_db()
if __name__ == "__main__" :
    app.run(debug=True)



