from flask import Flask, request, render_template, redirect
from boolean_model import BooleanModel
from tools import get_size
import ir_datasets
from system import InformationRetrievalSystem
from tokenizer import NltkTokenizer, Tokenizer

# Flask app boilerplate
app = Flask(__name__)

tokenizer = NltkTokenizer('english')

print("loading Corpus")
sri = InformationRetrievalSystem(tokenizer=tokenizer)
sri.load_and_process_corpus_from_path('./static/corpus/*')

@app.route("/", methods = ["GET"])
def home():
    return redirect("/search")
@app.route('/search', methods = ["GET", "POST"])
def search():
    res = []
    rel = None
    methods = ["boolean", "vectorial", "fuzzy"]
    try:
        query_method = request.form['method']
    except:
        query_method = 'boolean' 
    
    if request.method == "POST":
        query = request.form['search']
        if query == '':
            return render_template('search.html', results=None, methods=methods, query=None)

        models = {
            "boolean": sri.process_query_with_boolean_model, 
            "vectorial": sri.process_query_with_vectorial_model,
            "fuzzy": sri.process_query_with_fuzzy_model
            }
        res = models[query_method](query)
        # print(type(res[0]))
        if len(res) > 0 and type(res[0]) is tuple:
            rel = {sri.documents[r[0]].title:r[1] for r in res}
            res = [r[0] for r in res]
            
        res = [(sri.documents[i].title,get_size(i)) for i in res]
        return render_template('search.html', results=res, methods=methods, sel_method=(query_method if query_method else 'boolean'), query=query, relevance=rel)
    return render_template('search.html', results=None, methods=methods,sel_method=(query_method if query_method else 'boolean') ,query=None, relevance=rel)
    
if __name__ == "__main__":
    app.run(debug=True)
