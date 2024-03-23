from flask import Flask, jsonify, request
import re

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

@app.route("/step/add", methods=["POST"])
def open_step_editor(action_code):
    return