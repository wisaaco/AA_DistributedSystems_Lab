#Based on: https://realpython.com/api-integration-in-python/

from flask import Flask, request, jsonify
import random
app = Flask(__name__)

things = {}
things[1] = {"id": 1, "name": "Thing Value %f"%random.random()}
things[2] = {"id": 2, "name": "Thing Value %f"%random.random()}
things[3] = {"id": 3, "name": "Thing Value %f"%random.random()}

@app.route("/api/v1/random", methods=["GET"])
def get_random_number():
    return jsonify({"random":random.random()}), 200

@app.route("/api/v1/things/<int:thing_id>", methods=["GET"])
def get_things(thing_id):
    if thing_id in things:
        return jsonify(things[thing_id]), 200
    else:
        return jsonify({"error": "Thing not found"}), 404

@app.route("/api/v1/things", methods=["POST"])
def add_thing():
    if request.is_json:
        data = request.get_json()
        things[int(data["id"])] = data
        return jsonify(data), 201
    return {"error": "Request must be JSON"}, 415


if __name__ == "__main__":
    app.run(debug=True)


# Run: python3 app.py (me: /Users/isaac/.pyenv/versions/3.11.0rc2/envs/my3110/bin/python3 app.py)
# With curl or browser: http://127.0.0.1:5000/api/v1/random    
# curl -i http://127.0.0.1:5000/api/v1/things -X POST -H 'Content-Type: application/json' -d '{"id":4, "name":"Thing Value 4.3"}'
# openapi.yaml in https://editor.swagger.io/

# Guidelines:
# https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design
#https://swagger.io/specification/