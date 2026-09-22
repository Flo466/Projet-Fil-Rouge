# Ordre de déploiement Site C

| Étape | Action | Dépendance |
| ---: | --- | --- |
| 1 | Valider Routeur 2, Proxmox 2 et `192.168.200.0/24` | Routage et filtrage |
| 2 | Installer Web 1 `192.168.200.11` et Web 2 `192.168.200.12` | Proxmox 2 |
| 3 | Tester Nginx et `/healthz` avec `fronts.yml` | SSH et Python 3 |
| 4 | Installer le reverse proxy `192.168.200.10` | Web 1 et Web 2 |
| 5 | Appliquer les règles Routeur 2 et SW-L3 | Services testés |
| 6 | Effectuer la recette positive et négative | Tout le reste |

Ne pas publier le reverse proxy avant d'avoir validé les routes retour, les journaux de filtrage et les certificats.
