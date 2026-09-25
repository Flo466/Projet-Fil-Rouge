# Infrastructure - Site C

Ce dossier contient le plan d'adressage retenu et les deux configurations à expliquer à l'oral : le switch L3 et Routeur 2. Le lien existant entre le switch L3 et Routeur 1 est conservé tel quel.

## Réseaux

### LAN privé : `172.16.2.0/24`

Le LAN est découpé en huit sous-réseaux `/27` (`255.255.255.224`). La passerelle est la première adresse utilisable de chaque bloc.

| VLAN | Usage | Réseau | Passerelle | Hôtes |
| ---: | --- | --- | --- | --- |
| 10 | Service 1 | `172.16.2.0/27` | `172.16.2.1` | `.2` à `.30` |
| 20 | Service 2 | `172.16.2.32/27` | `172.16.2.33` | `.34` à `.62` |
| 30 | Serveurs / Proxmox 2 / Web | `172.16.2.64/27` | `172.16.2.65` | `.66` à `.94` |
| 40 | Wi-Fi employés | `172.16.2.96/27` | `172.16.2.97` | `.98` à `.126` |
| 50 | VoIP | `172.16.2.128/27` | `172.16.2.129` | `.130` à `.158` |
| 60 | Wi-Fi invités | `172.16.2.160/27` | `172.16.2.161` | `.162` à `.190` |
| 80 | Réserve / extension | `172.16.2.192/27` | `172.16.2.193` | `.194` à `.222` |
| 99 | Management | `172.16.2.224/27` | `172.16.2.225` | `.226` à `.254` |

Adresses de travail du VLAN 30 : AD/DNS/DHCP `172.16.2.66`, Zabbix `172.16.2.67`, Proxmox 2 `172.16.2.68`, Web 1 `172.16.2.69`, Routeur 2 côté LAN `172.16.2.70`, Web 2 `172.16.2.71`.

### DMZ : `172.16.3.128/26`

La DMZ est découpée en deux sous-réseaux `/27` (`255.255.255.224`) :

| VLAN | Rôle | Réseau | Passerelle | Hôtes proposés |
| ---: | --- | --- | --- | --- |
| 70 | Caméras DMZ | `172.16.3.128/27` | `172.16.3.129` | Caméras `.130` à `.158` |
| 71 | DMZ reverse proxy | `172.16.3.160/27` | `172.16.3.161` | Reverse proxy `.162` |

## Liens

- SW-L3 ↔ Routeur 1 : lien existant conservé tel quel, aucune adresse ni route modifiée.
- SW-L3 ↔ Routeur 2 `Gi0/0` : trunk 802.1Q, port du switch **à confirmer**, VLAN autorisés 30, 70 et 71.
- SW-L3 ↔ Proxmox 2 : trunk 802.1Q, port du switch **à confirmer**, VLAN autorisés 30, 70 et 71 ; VLAN 30 natif pour la gestion de Proxmox.
- Les ports connus `Gi1/0/22` (Wi-Fi invités) et `Gi1/0/23` (caméras) restent en accès comme dans l'extrait fourni.
- Le VLAN 70 contient les caméras de la DMZ ; le VLAN 71 contient le reverse proxy.
- Les deux serveurs Web applicatifs restent dans le VLAN 30.

## Fichiers

- [Switch-L3.txt](configuration/Switch-L3.txt) : VLAN, ports, SVI, ACL, relais DHCP et SSH.
- [Routeur-2.txt](configuration/Routeur-2.txt) : sous-interfaces trunk, routes, ACL DMZ et SSH.
- [Dossier réseau](docs/Dossier_reseau.md) : explication de l'architecture et de la recette.
- [Audit Site C](docs/Audit_Site_C.md) : contrôle documentaire et preuves à recueillir.

Le découpage est construit à partir des réseaux fournis par l'équipe. Les noms des interfaces et les ports doivent être vérifiés sur le matériel avant collage de configuration.
