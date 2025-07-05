from flask import render_template, request
# from app import app
import dao
from app import app


@app.route("/")
def index():
    cates = dao.load_categories()
    cate_id = request.args.get("cate_id")
    kw = request.args.get("kw")
    product = dao.load_product(cate_id=cate_id, kw=kw)
    return render_template("index.html", category=cates, product=product)

if __name__ == '__main__':
    app.run(debug=True)