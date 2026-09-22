# Ordre de déploiement Web - Site C

| Étape | Action | Dépendance |
| ---: | --- | --- |
| 1 | Valider le découpage du bloc `172.16.128.0/18` et le réseau applicatif `172.16.138.0/24` | Validation du plan |
| 2 | Configurer Routeur 2 et Proxmox 2 | Routage et filtrage |
| 3 | Installer Web 1 `172.16.138.11` et Web 2 `172.16.138.12` | Proxmox 2 |
| 4 | Tester Nginx et `/healthz` avec `fronts.yml` | SSH et Python 3 |
| 5 | Installer le reverse proxy `172.16.138.10` | Web 1 et Web 2 |
| 6 | Appliquer les règles ACL et effectuer la recette | Services testés |

Ne pas publier le reverse proxy avant d'avoir validé les routes retour, les journaux de filtrage et les certificats.
