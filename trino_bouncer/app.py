from trino_bouncer.bouncer import Bouncer

from flask import Flask, redirect, request

from werkzeug.serving import WSGIRequestHandler
WSGIRequestHandler.protocol_version = "HTTP/1.1"

app = Flask(__name__)
bouncer = Bouncer()
bouncer.add_targets({
    # Should match the docker-compose.yaml file
    "green": "http://localhost:8081",
    "blue": "http://localhost:8082",
})


@app.route("/v1/<path:path>", methods=["GET", "POST"])
def trino(path):
    target = bouncer.active
    app.logger.debug(f"Redirecting to: {target[1] + '/v1/' + path}")
    return redirect(target[1] + '/v1/' + path, code=307)


@app.route("/status")
def status():
    active = bouncer.active
    return {"name": active[0], "url": active[1]}


@app.route("/switch", methods=["POST"])
def switch():
    cluster = request.args.get("cluster", None)
    if cluster is None:
        return "Missing 'cluster' parameter", 400

    try:
        bouncer.active = cluster
    except KeyError:
        return f"Unknown cluster '{cluster}'", 404

    return f"Now active: {bouncer.active}", 200
