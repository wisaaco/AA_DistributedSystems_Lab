
from flask import Flask, request, jsonify
import random
#Based on: https://realpython.com/api-integration-in-python/

app = Flask(__name__)

things = [ ]

@app.get("/random")
def get_random_number():
    return jsonify({"random":random.random()})

@app.get("/things")
def get_things():
    return jsonify(things)

@app.post("/addThing")
def add_thing():
    if request.is_json:
        thing = request.get_json()
        things.append(thing)
        return thing, 201
    return {"error": "Request must be JSON"}, 415

# Save the file as: app.py  #or: export FLASK_APP=app.py
# Run: python -m flask run
# With curl or browser: http://127.0.0.1:5000/random    
# curl -i http://127.0.0.1:5000/addThing -X POST -H 'Content-Type: application/json' -d '{"seed":2022}'