from flask import render_template
import dao
from app import app


@app.route("/")
def index():
    cates = dao.load_categories()
    prods = dao.load_products()
    return render_template("index.html", categories=cates, products=prods)


if __name__ == '__main__':
    app.run(debug=True)
