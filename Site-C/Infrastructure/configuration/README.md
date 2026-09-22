# Inventaire des configurations de Site C

Les fichiers de ce dossier sont alignés sur `../nouveau adressage.pdf`. Les réseaux du plan sont des `/28` ; une adresse historique en `/24` ne doit pas être appliquée sur Site C.

| Fichier | Cible | Contenu | État |
| --- | --- | --- | --- |
| [Switch L3.txt](../Switch%20L3.txt) | Switch L3 | VLAN 10, 20, 30, 40, 50, 60, 70, 80 et 99, SVI `/28`, ports d'accès, ACL et SSH | Exemple à adapter au modèle |
| [Routeur2_Proxmox2.md](Routeur2_Proxmox2.md) | Routeur 2 et Proxmox 2 | Liaison au VLAN 30, réseau isolé des Web et reverse proxy | Adresses de transit proposées |

## Adresses du plan

| VLAN | Réseau | Passerelle | Hôtes utilisables |
| ---: | --- | --- | --- |
| 10 | `192.168.0.0/28` | `192.168.0.1` | `.2` à `.14` |
| 20 | `192.168.0.16/28` | `192.168.0.17` | `.18` à `.30` |
| 30 | `192.168.0.32/28` | `192.168.0.33` | `.34` à `.46` |
| 40 | `192.168.0.48/28` | `192.168.0.49` | `.50` à `.62` |
| 50 | `192.168.0.64/28` | `192.168.0.65` | `.66` à `.78` |
| 60 | `192.168.0.80/28` | `192.168.0.81` | `.82` à `.94` |
| 70 | `192.168.0.96/28` | `192.168.0.97` | `.98` à `.110` |
| 80 | `192.168.0.112/28` | `192.168.0.113` | `.114` à `.126` |
| 99 | `192.168.0.128/28` | `192.168.0.129` | `.130` à `.142` |

## Répartition proposée des serveurs

Les rôles ci-dessous utilisent des hôtes libres du VLAN 30 et doivent être confirmés avant installation :

| Rôle | Adresse | Passerelle |
| --- | --- | --- |
| Windows Server AD/DNS/DHCP | `192.168.0.34/28` | `192.168.0.33` |
| Zabbix | `192.168.0.35/28` | `192.168.0.33` |
| Routeur 2 côté VLAN 30 | `192.168.0.46/28` | `192.168.0.33` |
| Proxmox 2 côté réseau isolé | `192.168.200.2/24` | `192.168.200.1` |
| Reverse proxy | `192.168.200.10/24` | `192.168.200.1` |
| Web 1 | `192.168.200.11/24` | `192.168.200.1` |
| Web 2 | `192.168.200.12/24` | `192.168.200.1` |

Le transit proposé entre le switch et Routeur 1 est `192.168.254.0/30` : switch `.2`, routeur `.1`. Ces deux propositions évitent le conflit avec les sous-réseaux du nouveau plan.

## Avant application

Relever le modèle et la version IOS, les noms d'interfaces, les ports réellement raccordés, l'adresse WAN de Routeur 1, les paramètres NAT, le domaine AD, les ports Web et la méthode de sauvegarde. Tester chaque ACL par un flux autorisé et un flux refusé avant `write memory`.
