# Trino Bouncer

An example webserver to redirect Trino requests.
You may not want to use Python for this on large production workloads.

### Notes
* Use `http://127.0.0.1` for the host, at least on macOS. Flask/Werkzug doesn't like IPv6 with default configs.

## Running the Example

1. Stand up the Trino "clusters" using the provided `docker-compose.yaml`
2. Start the Flask app with `poetry run flask run --debug` from the `trino_bouncer` folder.
3. Run the example test with `poetry run python scripts/integration_test.py`