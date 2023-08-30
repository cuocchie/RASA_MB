from flask import Flask

app = Flask(__name__)

@app.route("/get-content", methods=['GET'])
def hello_world():
    return "ABC"
