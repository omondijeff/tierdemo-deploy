"""Minimal 3-tier dummy: HTTP + Redis PING + Postgres SELECT 1."""
import os
import time

import flask
import psycopg2
import redis

app = flask.Flask(__name__)


def _redis_ok():
    host = os.environ.get("REDIS_HOST", "redis.redis.svc.cluster.local")
    password = os.environ.get("REDIS_PASSWORD", "")
    r = redis.Redis(host=host, port=6379, password=password or None, socket_timeout=3)
    return r.ping() is True


def _postgres_ok():
    conn = psycopg2.connect(
        host=os.environ.get("POSTGRES_HOST", "postgres.database.svc.cluster.local"),
        port=int(os.environ.get("POSTGRES_PORT", "5432")),
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        dbname=os.environ["POSTGRES_DB"],
        connect_timeout=3,
    )
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1")
        row = cur.fetchone()
        return row is not None and row[0] == 1
    finally:
        conn.close()


@app.route("/ready")
def ready():
    try:
        ok_r = _redis_ok()
        ok_p = _postgres_ok()
    except Exception:
        return ("not ready", 503)
    if ok_r and ok_p:
        return ("ok", 200)
    return ("not ready", 503)


@app.route("/")
def index():
    redis_status = "unknown"
    pg_status = "unknown"
    try:
        redis_status = "OK" if _redis_ok() else "FAIL"
    except Exception as e:
        redis_status = f"ERROR: {e}"
    try:
        pg_status = "OK" if _postgres_ok() else "FAIL"
    except Exception as e:
        pg_status = f"ERROR: {e}"

    return flask.Response(
        f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>3-tier demo</title>
<style>
body {{ font-family: system-ui, sans-serif; margin: 2rem; max-width: 48rem; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #ccc; padding: 0.5rem 0.75rem; text-align: left; }}
.ok {{ color: #0a0; }} .bad {{ color: #a00; }}
footer {{ margin-top: 2rem; font-size: 0.9rem; color: #444; }}
</style></head><body>
<h1>Three-tier dummy application</h1>
<p>Presentation: this pod &middot; Cache: Redis &middot; Data: PostgreSQL (PVC)</p>
<table>
<tr><th>Tier</th><th>Check</th><th>Result</th></tr>
<tr><td>Cache (Redis)</td><td><code>PING</code></td><td class="{'ok' if redis_status == 'OK' else 'bad'}">{redis_status}</td></tr>
<tr><td>Data (Postgres)</td><td><code>SELECT 1</code></td><td class="{'ok' if pg_status == 'OK' else 'bad'}">{pg_status}</td></tr>
</table>
<footer>
PostgreSQL uses PVC <code>postgres-pvc</code> with StorageClass <code>local-path</code>
(state survives pod restarts; delete the pod to verify the same data directory is reattached).
</footer>
</body></html>""",
        mimetype="text/html",
    )


if __name__ == "__main__":
    # Wait for optional dependency install wrapper (see Deployment command).
    time.sleep(0.1)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
