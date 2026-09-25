# Back-End Python - Site B

Serveur applicatif et API REST développé exclusivement en Python standard (sans dépendance externe requise).

## Fichiers

- [`server.py`](./server.py) : Serveur HTTP gérant les routes REST (`/api/*`), les en-têtes CORS et la distribution des fichiers statiques du dossier `Front-End`.
- [`fake_data.json`](./fake_data.json) : Jeu de données simulées (services, environnement, métadonnées) découplé du code source.

## Démarrage rapide

Exécuter la commande suivante depuis ce dossier :

```bash
python3 server.py
```

Pour spécifier un port différent (par exemple `8080`) :

```bash
python3 server.py 8080
```

## Points de terminaison (Endpoints API)

| Méthode | Route | Description | Exemple de réponse |
|---|---|---|---|
| `GET` | `/api/status` | Télémétrie et état de santé du serveur | JSON (`status`, `uptime`, `python_version`, etc.) |
| `GET` | `/api/services` | Liste des services réseau / DMZ du Site B | JSON (`services`, `count`) |
| `POST` | `/api/echo` | Test de transmission de charge utile JSON | JSON écho |

## Architecture & Sécurité

- **Zéro dépendance pip** : Utilise uniquement la bibliothèque standard Python (`http.server`, `json`, `platform`, `time`, `logging`).
- **Support CORS** : En-têtes `Access-Control-Allow-Origin: *` pour faciliter les tests inter-domaines.
- **Protection contre la traversée de répertoires** : Validation canonique des chemins de fichiers servis.

