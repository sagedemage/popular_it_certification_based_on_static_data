# HTTP Server serving HTML and JSON files
import json
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/serve-html-file", methods=["GET"])
def serve_html_file():
    # http://127.0.0.1:5000/serve-html-file?index=0
    if request.method == "GET":
        if request.args.get('index') != None:
            index = request.args.get('index')
            if index.isdigit():
                with open(f"html_content/output{index}.html", "r", encoding="utf-8") as f:
                    data = f.read()
                return data
            else:
                return "Index is not a number"
        else:
            return "Please supply the query, ?index=num like this /serve-html-file?index=0"
    else:
        return "Method Not Allowed"

@app.route("/serve-json-file", methods=["GET"])
def serve_json_file():
    # http://127.0.0.1:5000/serve-json-file?index=0
    if request.method == "GET":
        if request.args.get('index') != None:
            index = request.args.get('index')
            if index.isdigit():
                with open(f"website_info/output{index}.json", "r") as f:
                    data = json.load(f)
                return data
            else:
                return "Index is not a number"
        else:
            return "Please supply the query, ?index=num like this /serve-json-file?index=0"
    else:
        return "Method Not Allowed"
