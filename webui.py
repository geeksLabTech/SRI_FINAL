from flask import Flask, request, render_template, redirect
from boolean_model import BooleanModel

# Flask app boilerplate
app = Flask(__name__)
boolean_model = BooleanModel('./corpus/soccer/*', 'english')

@app.route("/", methods = ["GET"])
def home():
    return redirect("/search")
@app.route('/search', methods = ["GET", "POST"])
def search():
    res = []
    
    if request.method == "POST":
        query = request.form['search']
        # query_method = request.form['query_method']
        
        # if query_method == "boolean":
        res = boolean_model.query(query)
        print(res)
        return render_template('search.html', results=res)
    return render_template('search.html')
     
if __name__ == "__main__":
    app.run(debug=True)
