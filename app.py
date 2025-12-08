# app.py
from flask import Flask, request, jsonify
from shortest_path import shortest_path_weighted

app = Flask(__name__)

@app.route("/shortest_path", methods=["GET"])
def get_shortest_path():
    start = request.args.get("start")
    end = request.args.get("end")
    if not start or not end:
        return jsonify({"error": "Il faut préciser start et end"}), 400
    
    path, distance = shortest_path_weighted(start, end)
    if path:
        return jsonify({"path": path, "distance": distance})
    else:
        return jsonify({"error": "Aucun chemin trouvé"}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)
