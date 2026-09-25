# Dossier réseau - Site C

## 1. Plan d'adressage

Le LAN privé fourni est `172.16.2.0/24` (`255.255.255.0`). Il est découpé en huit sous-réseaux `/27` (`255.255.255.224`) :

| VLAN | Usage | Réseau / plage complète | Passerelle |
| ---: | --- | --- | --- |
| 10 | Service 1 | `172.16.2.0/27` (`.0` à `.31`) | `172.16.2.1` |
| 20 | Service 2 | `172.16.2.32/27` (`.32` à `.63`) | `172.16.2.33` |
| 30 | Serveurs / Proxmox 2 / Web | `172.16.2.64/27` (`.64` à `.95`) | `172.16.2.65` |
| 40 | Wi-Fi employés | `172.16.2.96/27` (`.96` à `.127`) | `172.16.2.97` |
| 50 | VoIP | `172.16.2.128/27` (`.128` à `.159`) | `172.16.2.129` |
| 60 | Wi-Fi invités | `172.16.2.160/27` (`.160` à `.191`) | `172.16.2.161` |
| 80 | Réserve | `172.16.2.192/27` (`.192` à `.223`) | `172.16.2.193` |
| 99 | Management | `172.16.2.224/27` (`.224` à `.255`) | `172.16.2.225` |

La DMZ fournie est `172.16.3.128/26` (`255.255.255.192`, de `.128` à `.191`). Elle est divisée en deux `/27` :

| VLAN | Usage | Réseau / plage complète | Passerelle |
| ---: | --- | --- | --- |
| 70 | Caméras DMZ | `172.16.3.128/27` (`.128` à `.159`) | `172.16.3.129` |
| 71 | DMZ reverse proxy | `172.16.3.160/27` (`.160` à `.191`) | `172.16.3.161` |

Adresses prévues : AD/DNS/DHCP `172.16.2.66`, Zabbix `172.16.2.67`, Proxmox 2 `172.16.2.68`, Web 1 `172.16.2.69`, Routeur 2 sur le VLAN 30 `172.16.2.70`, Web 2 `172.16.2.71`, reverse proxy `172.16.3.162`. Les caméras utilisent les adresses disponibles du VLAN 70.

## 2. Liens et ports

| Lien | Mode | VLAN autorisés | Rôle |
| --- | --- | --- | --- |
| SW-L3 Gi1/0/22 ↔ R2 Gi0/0 | trunk 802.1Q | 30, 70, 71 | Routeur 2 porte les passerelles DMZ |
| SW-L3 Gi1/0/23 ↔ Proxmox 2 | trunk 802.1Q | 30, 70, 71 | Gestion Proxmox en VLAN 30, VM dans les DMZ |
| SW-L3 Gi1/0/24 ↔ Routeur 1 | routé L3 | inchangé | Lien existant à ne pas modifier |

Les ports Gi1/0/1-4, 5-8, 9-12, 13-16 et 17-20 sont respectivement en accès dans les VLAN 10, 20, 30, 40 et 50. Gi1/0/21 est le poste d'administration du VLAN 99.

## 3. Routage et filtrage

Le switch L3 est la passerelle des huit VLAN LAN. Routeur 2 est la passerelle des VLAN DMZ et utilise `172.16.2.65` comme sortie vers le LAN. Le switch route `172.16.3.128/27` et `172.16.3.160/27` vers `172.16.2.70`. Le lien vers Routeur 1 et sa route par défaut restent tels qu'ils étaient.

Les ACL du switch autorisent DNS, DHCP et les services nécessaires, puis bloquent les accès inter-réseaux non prévus. Les ACL de Routeur 2 autorisent HTTP/HTTPS vers le reverse proxy `172.16.3.162`, puis du reverse proxy vers Web 1 `172.16.2.69` et Web 2 `172.16.2.71`. Les caméras sont limitées à leur supervision et les nouvelles connexions de la DMZ vers le LAN sont refusées par défaut.

## 4. Recette

1. Vérifier `show vlan brief`, `show interfaces trunk` et `show ip interface brief`.
2. Vérifier les routes et le ping entre `172.16.2.65`, `172.16.2.70`, `172.16.3.129` et `172.16.3.161`.
3. Tester DHCP/DNS depuis les VLAN 10, 20 et 40.
4. Tester HTTP/HTTPS via `172.16.3.162`, puis vérifier que le proxy atteint `172.16.2.69` et `172.16.2.71`.
5. Tester SSH depuis le VLAN 99 et le refus depuis un autre VLAN.
6. Contrôler les compteurs avec `show access-lists` et sauvegarder après validation.
