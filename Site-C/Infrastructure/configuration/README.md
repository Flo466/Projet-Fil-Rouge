# Inventaire des configurations de Site C

Site C est le Site 2 de la consigne professeur. Le bloc global validé est `172.16.64.0/18` avec le masque `255.255.192.0`. Le dépôt utilise un découpage de travail en `/24` par VLAN, à valider avant application.

| Fichier | Cible | Contenu | État |
| --- | --- | --- | --- |
| [Switch L3.txt](../Switch%20L3.txt) | Switch L3 | VLAN, noms, ports, SVI, relais DHCP, ACL et SSH | Configuration de travail à valider |
| [Routeur 2.txt](../Routeur%202.txt) | Routeur 2 | Interfaces, routes, ACL d'isolation et SSH | Configuration de travail à valider |
| [Routeur2_Proxmox2.md](Routeur2_Proxmox2.md) | Routeur 2 / Proxmox 2 | Plan d'adressage et règles de flux | Proposition à valider |

## VLAN et passerelles de travail

| VLAN | Réseau | Passerelle |
| ---: | --- | --- |
| 10 | `172.16.64.0/24` | `172.16.64.1` |
| 20 | `172.16.65.0/24` | `172.16.65.1` |
| 30 | `172.16.66.0/24` | `172.16.66.1` |
| 40 | `172.16.67.0/24` | `172.16.67.1` |
| 50 | `172.16.68.0/24` | `172.16.68.1` |
| 60 | `172.16.69.0/24` | `172.16.69.1` |
| 70 | `172.16.70.0/24` | `172.16.70.1` |
| 80 | `172.16.71.0/24` | `172.16.71.1` |
| 99 | `172.16.72.0/24` | `172.16.72.1` |

## Services de travail

| Rôle | Adresse | Passerelle |
| --- | --- | --- |
| Windows AD/DNS/DHCP | `172.16.66.10/24` | `172.16.66.1` |
| Zabbix | `172.16.66.11/24` | `172.16.66.1` |
| IPBX | `172.16.66.12/24` | `172.16.66.1` |
| Routeur 2 côté VLAN 30 | `172.16.66.254/24` | `172.16.66.1` |
| Proxmox 2 | `172.16.74.2/24` | `172.16.74.1` |
| Reverse proxy | `172.16.74.10/24` | `172.16.74.1` |
| Web 1 / Web 2 | `172.16.74.11` / `.12` | `172.16.74.1` |

Transit proposé vers Routeur 1 : `172.16.73.0/30`, SW-L3 `172.16.73.2`, routeur `172.16.73.1`.

Avant application, relever le modèle IOS, les ports, le WAN, le NAT, le domaine AD, les ports Web et le découpage validé par le professeur. Tester les ACL et sauvegarder les configurations seulement après recette.
