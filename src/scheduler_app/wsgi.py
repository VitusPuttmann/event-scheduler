"""
WSGI entrypoint used by Gunicorn in Docker.
"""


def app(environ, start_response):
    body = (
        b"event-scheduler container is running. "
        b"Main workflow is executed via scheduler_app.cli."
    )
    headers = [
        ("Content-Type", "text/plain; charset=utf-8"),
        ("Content-Length", str(len(body))),
    ]
    start_response("200 OK", headers)
    return [body]
