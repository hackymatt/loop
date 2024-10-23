import multiprocessing
import os
from dotenv import load_dotenv


load_dotenv()

LOCAL = os.getenv("LOCAL", "True") == "True"

# Django WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
wsgi_app = "core.wsgi"
# The number of worker processes for handling requests
workers = (multiprocessing.cpu_count() * 3) + 1
# Timeout
timeout = 30
# The socket to bind
bind = "0.0.0.0:8000"
# Daemonize the Gunicorn process (detach & enter background)
daemon = not LOCAL
# Access log configuration (optional)
accesslog = "-"  # Log to stdout, useful for Docker
errorlog = "-"  # Log errors to stdout
