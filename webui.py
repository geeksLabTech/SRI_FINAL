from flask import Flask, request, render_template, redirect
from boolean_model import BooleanModel
from tools import get_size

# Flask app boilerplate
app = Flask(__name__)
boolean_model = BooleanModel('./static/corpus/*', 'english')

@app.route("/", methods = ["GET"])
def home():
    return redirect("/search")
@app.route('/search', methods = ["GET", "POST"])
def search():
    res = []
    methods = ["boolean"]
    if request.method == "POST":
        query = request.form['search']
        query_method = request.form['method']
        
        if query_method == "boolean":
            res = boolean_model.query(query)
        res = [(i,get_size(i)) for i in res]
        return render_template('search.html', results=res, methods=methods, query=query)
    return render_template('search.html', results=None, methods=methods, query=None)
     
if __name__ == "__main__":
    app.run(debug=True)
