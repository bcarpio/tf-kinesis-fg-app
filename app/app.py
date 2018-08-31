from flask import Flask, render_template, redirect, make_response, Response, jsonify, url_for
from dump import *
import os

app = Flask(__name__)

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

@app.route("/")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return jsonify(links)

@app.route("/all")
def get_all_records():
    dict = dump_stream()
    return jsonify(dict)

@app.route("/instance")
def list_instance_records():
    dict = get_instance_data()
    return jsonify(dict)

@app.route("/rds")
def list_rds_records():
    dict = get_rds_data()
    return jsonify(dict)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
