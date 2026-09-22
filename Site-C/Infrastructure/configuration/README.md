# Inventaire des configurations de Site C

Site C est le Site 3 de la consigne professeur. Le bloc global validé est `172.16.128.0/18` avec le masque `255.255.192.0`. Le dépôt utilise un découpage de travail en `/24` par VLAN, à valider avant application.

| Fichier | Cible | Contenu | État |
| --- | --- | --- | --- |
| [Switch L3.txt](../Switch%20L3.txt) | Switch L3 | VLAN, noms, ports, SVI, relais DHCP, ACL et SSH | Configuration de travail à valider |
| [Routeur 2.txt](../Routeur%202.txt) | Routeur 2 | Interfaces, routes, ACL d'isolation et SSH | Configuration de travail à valider |
| [Routeur2_Proxmox2.md](Routeur2_Proxmox2.md) | Routeur 2 / Proxmox 2 | Plan d'adressage et règles de flux | Proposition à valider |

## VLAN et passerelles de travail

| VLAN | Réseau | Passerelle |
| ---: | --- | --- |
| 10 | `172.16.128.0/24` | `172.16.128.1` |
| 20 | `172.16.129.0/24` | `172.16.129.1` |
| 30 | `172.16.130.0/24` | `172.16.130.1` |
| 40 | `172.16.131.0/24` | `172.16.131.1` |
| 50 | `172.16.132.0/24` | `172.16.132.1` |
| 60 | `172.16.133.0/24` | `172.16.133.1` |
| 70 | `172.16.134.0/24` | `172.16.134.1` |
| 80 | `172.16.135.0/24` | `172.16.135.1` |
| 99 | `172.16.136.0/24` | `172.16.136.1` |

## Services de travail

| Rôle | Adresse | Passerelle |
| --- | --- | --- |
| Windows AD/DNS/DHCP | `172.16.130.10/24` | `172.16.130.1` |
| Zabbix | `172.16.130.11/24` | `172.16.130.1` |
| IPBX | `172.16.130.12/24` | `172.16.130.1` |
| Routeur 2 côté VLAN 30 | `172.16.130.254/24` | `172.16.130.1` |
| Proxmox 2 | `172.16.138.2/24` | `172.16.138.1` |
| Reverse proxy | `172.16.138.10/24` | `172.16.138.1` |
| Web 1 / Web 2 | `172.16.138.11` / `.12` | `172.16.138.1` |

Transit proposé vers Routeur 1 : `172.16.137.0/30`, SW-L3 `172.16.137.2`, routeur `172.16.137.1`.

Avant application, relever le modèle IOS, les ports, le WAN, le NAT, le domaine AD, les ports Web et le découpage validé par le professeur. Tester les ACL et sauvegarder les configurations seulement après recette.
