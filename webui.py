from flask import Flask, request, render_template, redirect
from boolean_model import BooleanModel
from tools import get_size
import ir_datasets
from system import InformationRetrievalSystem
from tokenizer import NltkTokenizer, Tokenizer

# Flask app boilerplate
app = Flask(__name__)

tokenizer = NltkTokenizer('english')
cranfield = ir_datasets.load('cranfield')
queries = cranfield.queries_iter()
sri = InformationRetrievalSystem(tokenizer=tokenizer)
sri.load_and_process_corpus_from_ir_datasets('cranfield')

# boolean_model = BooleanModel('./static/corpus/*', 'english')

@app.route("/", methods = ["GET"])
def home():
    return redirect("/search")
@app.route('/search', methods = ["GET", "POST"])
def search():
    res = []
    methods = ["boolean", "vectorial", "fuzzy"]
    if request.method == "POST":
        query = request.form['search']
        if query == '':
            return render_template('search.html', results=None, methods=methods, query=None)

        query_method = request.form['method']
 
        if query_method == "boolean":
            res = sri.process_query_with_boolean_model(query)
            res = [(i,get_size(i)) for i in res]
        return render_template('search.html', results=res, methods=methods, query=query)
    return render_template('search.html', results=None, methods=methods, query=None)
     
if __name__ == "__main__":
    app.run(debug=True)
