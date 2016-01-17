from flask import Flask
from flask import jsonify, abort
from flask import request
from haproxy_rest import HaProxy


app = Flask(__name__)
hap = HaProxy('/var/run/haproxysock')


@app.route('/haproxy/api/v1.0/disable_server', methods=['PUT'])
def disable_server():
    in_dict = {'backend': request.json['backend'], 'server': request.json['server']}
    try:
        hap.disable_server(in_dict)
        return jsonify({"Disabled": True}), 200
    except LookupError:
        return jsonify({"Disabled", False}), 504


@app.route('/haproxy/api/v1.0/enable_server', methods=['PUT'])
def enable_server():
    in_dict = {'backend': request.json['backend'], 'server': request.json['server']}
    try:
        hap.enable_server(in_dict)
        return jsonify({"Enabled": True}), 200
    except LookupError:
        return jsonify({"Enabled", False}), 504


@app.route('/haproxy/api/v1.0/info', methods=['GET'])
def get_info():
    hap._get_info()
    return jsonify(hap.info), 200


@app.route('/haproxy/api/v1.0/backend/<resource>', methods=['GET'])
def get_backend(resource):
        stats = list(hap.get_stats('backend', resource))
        if not stats:
            return jsonify({"Response:": "Resource not found"}), 404
        else:
            return jsonify({"backends": stats})


@app.route('/haproxy/api/v1.0/backend', methods=['GET'])
def get_backends():
        return jsonify({"backends": list(hap.get_stats('backend'))})


@app.route('/haproxy/api/v1.0/frontend/<resource>', methods=['GET'])
def get_frontend(resource):
        stats = list(hap.get_stats('frontend', resource))
        if not stats:
            return jsonify({"Response:": "Resource not found"}), 404
        else:
            return jsonify({"frontend": stats})


@app.route('/haproxy/api/v1.0/frontend', methods=['GET'])
def get_frontends():
    return jsonify({"frontends": list(hap.get_stats('frontend'))})


@app.route('/haproxy/api/v1.0/stats', methods=['GET'])
def get_stats():
    return jsonify({"stats": list(hap.get_stats('stats'))})


if __name__ == "__main__":
    app.run(debug=True)
