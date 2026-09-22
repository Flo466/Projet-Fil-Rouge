# Application Web - Site C

Le site C reprend l'organisation du site B avec un reverse proxy et deux serveurs Web sur le réseau isolé de Proxmox 2. Les adresses proposées sont `192.168.200.10` pour le reverse proxy, `192.168.200.11` pour Web 1 et `192.168.200.12` pour Web 2. Elles doivent être validées avant déploiement.

## Déploiement

- Les serveurs Web écoutent uniquement sur le réseau applicatif et ne sont pas publiés directement.
- Le reverse proxy distribue les requêtes HTTP/HTTPS vers Web 1 et Web 2.
- Ansible installe Nginx et fournit une page de santé `/healthz` sur les fronts.
- Aucun secret, certificat ou mot de passe ne doit être placé dans le dépôt.

Les fichiers Ansible sont dans `../Infrastructure/configuration/DMZ/Config_Ansible`. Le port SSH, l'utilisateur de déploiement et les certificats restent à renseigner selon l'environnement réel.
