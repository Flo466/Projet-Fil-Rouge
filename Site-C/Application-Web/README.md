# Application Web - Site C

Le reverse proxy est placé dans le VLAN 71 de la DMZ fournie `172.16.3.128/26`. Le VLAN 70 est réservé aux caméras. Les deux serveurs Web applicatifs restent dans le VLAN 30 du LAN.

| VLAN | Rôle | Adresse | Passerelle |
| ---: | --- | --- | --- |
| 30 | Web 1 | `172.16.2.69/27` | `172.16.2.65` |
| 30 | Web 2 | `172.16.2.71/27` | `172.16.2.65` |
| 70 | Caméras DMZ | `172.16.3.130` à `172.16.3.158` (`/27`) | `172.16.3.129` |
| 71 | Reverse proxy | `172.16.3.162/27` | `172.16.3.161` |

Le reverse proxy `172.16.3.162` est la seule cible publiée en HTTP/HTTPS. Il relaie vers `172.16.2.69` et `172.16.2.71` dans le VLAN 30. Les caméras du VLAN 70 sont isolées et peuvent envoyer leur supervision vers Zabbix selon les ACL. Les VLAN 30, 70 et 71 sont transportés sur les trunks SW-L3 ↔ Routeur 2 et SW-L3 ↔ Proxmox 2.

Les règles ACL autorisent les utilisateurs à joindre le reverse proxy, puis le reverse proxy à joindre les deux serveurs Web du VLAN 30. Les accès d'administration passent par le VLAN 99.
