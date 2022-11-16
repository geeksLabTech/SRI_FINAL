from flask import Flask
from boolean_model import BooleanModel

# Flask app boilerplate
app = Flask(__name__)
model = BooleanModel('./corpus/soccer/*', 'english')

@app.route("/", methods = ["GET"])
def home():
    return 