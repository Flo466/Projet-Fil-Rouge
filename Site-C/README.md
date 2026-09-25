# Site C

Ce dossier regroupe la configuration réseau et l'application Web du Site C. Le plan demandé est maintenant appliqué dans tous les documents : LAN privé `172.16.2.0/24` découpé en huit `/27`, et DMZ `172.16.3.128/26` découpée en deux `/27`.

Le serveur Proxmox 2 et les deux serveurs Web restent dans le VLAN 30. Les caméras sont dans le VLAN 70 et le reverse proxy dans le VLAN 71 de la DMZ. Les VLAN 30, 70 et 71 passent sur les trunks vers Routeur 2 et Proxmox 2. Le lien existant entre le switch L3 et Routeur 1 est conservé sans modification.

## Plan d'adressage

| VLAN | Usage | Sous-réseau | Passerelle |
| ---: | --- | --- | --- |
| 10 | Service 1 | `172.16.2.0/27` | `172.16.2.1` |
| 20 | Service 2 | `172.16.2.32/27` | `172.16.2.33` |
| 30 | Serveurs / Proxmox 2 / Web | `172.16.2.64/27` | `172.16.2.65` |
| 40 | Wi-Fi employés | `172.16.2.96/27` | `172.16.2.97` |
| 50 | VoIP | `172.16.2.128/27` | `172.16.2.129` |
| 60 | Wi-Fi invités | `172.16.2.160/27` | `172.16.2.161` |
| 80 | Réserve | `172.16.2.192/27` | `172.16.2.193` |
| 99 | Management | `172.16.2.224/27` | `172.16.2.225` |
| 70 | Caméras DMZ | `172.16.3.128/27` | `172.16.3.129` |
| 71 | DMZ reverse proxy | `172.16.3.160/27` | `172.16.3.161` |

## Documents à expliquer

| Document | Rôle |
| --- | --- |
| [Infrastructure/README.md](Infrastructure/README.md) | Plan d'adressage, rôles et liens |
| [Switch-L3.txt](Infrastructure/configuration/Switch-L3.txt) | VLAN, ports, passerelles LAN, ACL, SSH et routes DMZ |
| [Routeur-2.txt](Infrastructure/configuration/Routeur-2.txt) | Trunk, passerelles DMZ, routage, ACL et SSH |
| [Dossier réseau](Infrastructure/docs/Dossier_reseau.md) | Architecture et procédure de recette |
| [Audit Site C](Infrastructure/docs/Audit_Site_C.md) | Contrôles et preuves à recueillir |
| [Application-Web/README.md](Application-Web/README.md) | Adresses du reverse proxy et des serveurs Web |

Les fichiers sont des configurations de préparation : il faut vérifier les numéros de ports, le modèle IOS et les adresses réellement utilisées avant collage sur le matériel.
