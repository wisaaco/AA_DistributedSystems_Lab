from flask import Flask, request, jsonify
import random
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)
things = {}
things[1] = {"id": 1, "name": "Thing Value %f"%random.random()}
things[2] = {"id": 2, "name": "Thing Value %f"%random.random()}
things[3] = {"id": 3, "name": "Thing Value %f"%random.random()}

@app.route("/api/v1/random", methods=["GET"])
def get_random_number():
    """
    Obtener un número aleatorio
    ---
    tags:
      - Random
    responses:
      200:
        description: Número aleatorio
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/Random'
    """
    return jsonify({"random":random.random()}), 200

@app.route("/api/v1/things/<int:thing_id>", methods=["GET"])
def get_things(thing_id):
    """
    Obtener un thing por ID
    ---
    tags:
      - Things
    responses:
      200:
        description: Thing encontrado
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Thing'
      404:
        description: Thing no encontrado
    """
    if thing_id in things:
        return jsonify(things[thing_id]), 200
    else:
        return jsonify({"error": "Thing not found"}), 404

@app.route("/api/v1/things", methods=["POST"])
def add_thing():
    """
    Crear un nuevo thing
    ---
    tags:
      - Things
    responses:
      201:
        description: Thing creado
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Thing'
      415:
        description: Request must be JSON
    """
    if request.is_json:
        data = request.get_json()
        things[int(data["id"])] = data
        return jsonify(data), 201
    return {"error": "Request must be JSON"}, 415


app.config["SWAGGER"] = {
    "components": {
        "schemas": {
            "Random": {
                "type": "object",
                "properties": {
                    "random": {"type": "number"},
                }
            },
            "Thing": {
                "type": "object",
                "required": ["id", "name"],
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"}
                }
            }
        }
    }
}


if __name__ == "__main__":
    app.run(debug=True)


# Run: python3 app.py (me: /Users/isaac/.pyenv/versions/3.11.0rc2/envs/my3110/bin/python3 app.py)
# With curl or browser: http://127.0.0.1:5000/api/v1/random    
# curl -i http://127.0.0.1:5000/api/v1/things -X POST -H 'Content-Type: application/json' -d '{"id":4, "name":"Thing Value 4.3"}'
# openapi.yaml in https://editor.swagger.io/