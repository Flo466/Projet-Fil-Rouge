# Application Web - Site C

Le service Web reprend l'organisation du site B sur le réseau applicatif de travail `172.16.138.0/24`, inclus dans le bloc Site 3 `172.16.128.0/18`.

| Rôle | Adresse | Passerelle |
| --- | --- | --- |
| Reverse proxy | `172.16.138.10/24` | `172.16.138.1` |
| Web 1 | `172.16.138.11/24` | `172.16.138.1` |
| Web 2 | `172.16.138.12/24` | `172.16.138.1` |

Le reverse proxy est la seule cible autorisée pour les accès HTTP/HTTPS. Web 1 et Web 2 ne sont pas publiés directement. Ansible installe Nginx et fournit `/healthz` sur les fronts ; les certificats, noms DNS et ports doivent être confirmés avant déploiement.

Les fichiers Ansible sont dans `../Infrastructure/configuration/DMZ/Config_Ansible`.
