#!/usr/bin/env python3

# from pypsrp.client import Client
from flask import Flask, render_template, request, session, make_response, jsonify
from flask_bootstrap import Bootstrap
from os import environ
from gittool import make_pr
import config
import json

app = Flask(__name__)
app.config.from_object("config.Config")

Bootstrap(app)

@app.route("/", methods=["GET", "POST"])
def main():
    devices = ["R1", "R2"]
    return render_template("main.html", devices=devices)


@app.route("/newvlan", methods=["POST"])
def newvlan():
    vlan_name = request.form.get("vlan_name")
    vlan_id = request.form.get("vlan_id")
    device = request.form.get("device_choice")
    yaml_data = {
        "vrfs" : {
           "name": vlan_name,
           "vlan_id": vlan_id,
           "linknett": f"192.168.{vlan_id}.0",
           "loopback": f"192.168.{vlan_id}.100"
        }
    }
    new_data = make_pr(yaml_data)
    response = make_response(
        jsonify(
            new_data
        ),
        401,
    )
    response.headers["Content-Type"] = "application/json"
    return response

if __name__ == "__main__":
    app.run()