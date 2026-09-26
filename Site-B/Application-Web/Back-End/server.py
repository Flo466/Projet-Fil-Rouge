#!/usr/bin/env python3
"""
Back-End HTTP & API REST - Site B (Projet Fil Rouge - TP-AIS)
Fichier : server.py
Rôle : Serveur HTTP et API REST autonome développé exclusivement en Python standard.
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import logging
import mimetypes
import os
import platform
import sys
import time
from typing import Dict, Any, Tuple
from urllib.parse import urlparse

# Configuration de base
HOST = os.environ.get("SERVER_HOST", "0.0.0.0")
PORT = int(os.environ.get("SERVER_PORT", "8000"))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "Front-End"))
DATA_FILE = os.path.join(BASE_DIR, "fake_data.json")

# Heure de démarrage pour le calcul de l'uptime
START_TIME = time.time()

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("SiteB-Backend")


def load_fake_data() -> Dict[str, Any]:
    """Charge les données simulées (fake data) depuis le fichier JSON externe."""
    if not os.path.exists(DATA_FILE):
        logger.warning("Fichier de données introuvable : %s", DATA_FILE)
        return {"services": [], "site": {}}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError) as err:
        logger.error("Erreur lors du chargement de %s : %s", DATA_FILE, err)
        return {"services": [], "site": {}}


class BackendRequestHandler(SimpleHTTPRequestHandler):
    """
    Gestionnaire de requêtes HTTP assurant :
    1. La fourniture des points d'accès REST (/api/*)
    2. La gestion des en-têtes CORS pour les requêtes cross-origin
    3. La distribution des fichiers statiques du dossier Front-End
    """

    def end_headers(self) -> None:
        """Ajoute les en-têtes CORS standard à toutes les réponses."""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        super().end_headers()

    def do_OPTIONS(self) -> None:
        """Gère les requêtes préliminaires CORS (preflight)."""
        self.send_response(204)
        self.end_headers()

    def do_GET(self) -> None:
        """Routeur des requêtes GET."""
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        if path.startswith("/api/"):
            self._handle_api_get(path)
        else:
            self._handle_static_file(path)

    def do_POST(self) -> None:
        """Routeur des requêtes POST."""
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        if path == "/api/echo":
            self._handle_api_echo()
        else:
            self._send_json({"error": "Endpoint non trouvé", "path": path}, status=404)

    # --------------------------------------------------------------------------
    # GESTION DES POINTS DE TERMINAISON API (REST)
    # --------------------------------------------------------------------------

    def _handle_api_get(self, path: str) -> None:
        """Dispatche les routes d'API en lecture."""
        if path == "/api/status":
            self._send_status()
        elif path == "/api/services":
            self._send_services()
        else:
            self._send_json({"error": "Route API inconnue", "path": path}, status=404)

    def _send_status(self) -> None:
        """Renvoie l'état du serveur, télémétrie système et informations d'exécution."""
        uptime_seconds = int(time.time() - START_TIME)
        uptime_str = self._format_uptime(uptime_seconds)
        data = load_fake_data()
        site_info = data.get("site", {})

        payload = {
            "status": "Opérationnel",
            "server": "Python Standard HTTP Server",
            "python_version": platform.python_version(),
            "system": platform.system(),
            "release": platform.release(),
            "uptime": uptime_str,
            "uptime_seconds": uptime_seconds,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
            "site": site_info.get("name", "Site-B"),
            "environment": site_info.get("environment", "DMZ / Application-Web")
        }
        self._send_json(payload)

    def _send_services(self) -> None:
        """Renvoie l'inventaire des services du Site B depuis le fichier fake_data.json."""
        data = load_fake_data()
        services = data.get("services", [])
        self._send_json({"services": services, "count": len(services)})

    def _handle_api_echo(self) -> None:
        """Traite une charge utile POST et la renvoie formatée."""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length == 0:
                self._send_json({"error": "Corps de requête vide"}, status=400)
                return

            body = self.rfile.read(content_length).decode("utf-8")
            data = json.loads(body)
            self._send_json({"received": data, "status": "Succès"})
        except json.JSONDecodeError:
            self._send_json({"error": "Format JSON invalide"}, status=400)
        except Exception as err:
            logger.error("Erreur de traitement POST: %s", err)
            self._send_json({"error": "Erreur interne du serveur"}, status=500)

    # --------------------------------------------------------------------------
    # DISTRIBUTION DES FICHIERS STATIQUES (FRONT-END)
    # --------------------------------------------------------------------------

    def _handle_static_file(self, path: str) -> None:
        """Distribue les fichiers statiques du dossier Front-End."""
        # Redirection de la racine vers index.html
        if path in ("/", ""):
            path = "/index.html"

        # Nettoyage du chemin relatif pour éviter la traversée de répertoires
        normalized_path = os.path.normpath(path.lstrip("/"))
        file_path = os.path.join(FRONTEND_DIR, normalized_path)

        # Vérification de sécurité (ne pas sortir de FRONTEND_DIR)
        if not os.path.abspath(file_path).startswith(FRONTEND_DIR):
            self._send_json({"error": "Accès refusé"}, status=403)
            return

        if not os.path.isfile(file_path):
            self._send_json({"error": "Fichier introuvable", "file": normalized_path}, status=404)
            return

        mime_type, _ = mimetypes.guess_type(file_path)
        mime_type = mime_type or "application/octet-stream"

        try:
            with open(file_path, "rb") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-Type", mime_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except OSError as err:
            logger.error("Erreur de lecture du fichier %s : %s", file_path, err)
            self._send_json({"error": "Erreur lors de la lecture du fichier"}, status=500)

    # --------------------------------------------------------------------------
    # UTILITAIRES DE RÉPONSE
    # --------------------------------------------------------------------------

    def _send_json(self, data: Dict[str, Any], status: int = 200) -> None:
        """Sérialise et envoie une réponse JSON avec code HTTP."""
        response_bytes = json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response_bytes)))
        self.end_headers()
        self.wfile.write(response_bytes)

    @staticmethod
    def _format_uptime(seconds: int) -> str:
        """Formate le temps d'exécution en chaîne lisible."""
        days, rem = divmod(seconds, 86400)
        hours, rem = divmod(rem, 3600)
        minutes, secs = divmod(rem, 60)
        parts = []
        if days > 0:
            parts.append(f"{days}j")
        if hours > 0 or days > 0:
            parts.append(f"{hours}h")
        if minutes > 0 or hours > 0 or days > 0:
            parts.append(f"{minutes}m")
        parts.append(f"{secs}s")
        return " ".join(parts)


def run_server(host: str = HOST, port: int = PORT) -> None:
    """Démarre le serveur HTTP."""
    server_address = (host, port)
    httpd = HTTPServer(server_address, BackendRequestHandler)
    logger.info("==================================================")
    logger.info("  Serveur Back-End Python démarré avec succès")
    logger.info("  Écoute sur http://%s:%d", host, port)
    logger.info("  Dossier Front-End servi : %s", FRONTEND_DIR)
    logger.info("  Point d'accès API : http://%s:%d/api/status", host, port)
    logger.info("==================================================")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("\nArrêt demandé par l'utilisateur (SIGINT)...")
    finally:
        httpd.server_close()
        logger.info("Serveur arrêté proprement.")


if __name__ == "__main__":
    # Support d'un argument optionnel pour changer le port : python3 server.py 8080
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        PORT = int(sys.argv[1])
    run_server(HOST, PORT)

