from flask import Flask, request, jsonify
from flask_cors import CORS
import redis

app = Flask(__name__)
CORS(app)
r = redis.StrictRedis(host = "redis", port = 6379, db = 0)

@app.route("/api/trips")
def get_trips():
    try:
        hour = request.args.get("hour")
        key = f"trips:total:{hour}"
        try:
            val = r.get(key)
            return jsonify({"Hour": hour, "Trip_Count": int(val) if val else 0})
        except redis.RedisError as e:
            return jsonify({"Error": f"Redis error occured {str(e)}"}), 500
    except Exception as e:
        return jsonify({"Error": str(e)}), 500

@app.route("/api/revenue")
def get_revenue():
    try:
        hour = request.args.get("hour")
        key = f"revenue:total:{hour}"
        try:
            val = r.get(key)
            return jsonify ({"Hour" : hour, "Revenue": float(val) if val else 0.0})
        except redis.RedisError as e:
            return jsonify({"Error": f"Redis error occured {str(e)}"}), 500
    except Exception as e:
        return jsonify({"Error": str(e)}), 500

@app.route("/api/distance")
def get_distance():
    try:
        hour = request.args.get("hour")
        key = f"distance:avg:{hour}"
        try:
            val = r.get(key)
            return jsonify({"Hour": hour, "Distance": float(val) if val else 0})
        except redis.RedisError as e:
            return jsonify({"Error": f"Redis error occured {str(e)}"}), 500
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


if __name__ == "__main__":
    app.run(host = "0.0.0.0", port= 5000, debug=True)