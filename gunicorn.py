import multiprocessing
import os

# Configuration Gunicorn pour la production

# Serveur socket
bind = "0.0.0.0:8000"

backlog = 2048

# Workers
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 120
keepalive = 5

# Process naming
proc_name = 'wariblo'

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process management
daemon = False
pidfile = '/tmp/gunicorn.pid'
user = None
group = None
tmp_upload_dir = None

# Server mechanics
reload = False
reload_engine = 'auto'
reload_extra_files = []

# SSL (si nécessaire)
# keyfile = '/path/to/keyfile'
# certfile = '/path/to/certfile'

# Server hooks
def on_starting(server):
    """Appelé juste avant le démarrage des workers"""
    print("Démarrage de Gunicorn pour Wariblo...")

def on_reload(server):
    """Appelé lors du rechargement"""
    print("Rechargement de Gunicorn...")

def when_ready(server):
    """Appelé quand le serveur est prêt"""
    print("Serveur Wariblo prêt sur", server.address)

def pre_fork(server, worker):
    """Appelé juste avant le fork d'un worker"""
    pass

def post_fork(server, worker):
    """Appelé juste après le fork d'un worker"""
    print(f"Worker {worker.pid} démarré")

def pre_exec(server):
    """Appelé juste avant l'exécution d'un nouveau master"""
    print("Exécution d'un nouveau master...")

def worker_int(worker):
    """Appelé quand un worker reçoit SIGINT"""
    print(f"Worker {worker.pid} reçu SIGINT")

def worker_abort(worker):
    """Appelé quand un worker reçoit SIGABRT"""
    print(f"Worker {worker.pid} reçu SIGABRT")

def nworkers_changed(server, new_value, old_value):
    """Appelé quand le nombre de workers change"""
    print(f"Nombre de workers changé de {old_value} à {new_value}")

def on_exit(server):
    """Appelé quand le serveur s'arrête"""
    print("Arrêt de Gunicorn...")
