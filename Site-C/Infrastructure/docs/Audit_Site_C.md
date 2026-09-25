# Audit documentaire et préparation - Site C

## Périmètre

Cet audit vérifie que les fichiers de Site C utilisent le plan fourni par l'équipe et que les rôles du switch L3, de Routeur 2, de Proxmox 2 et de la DMZ sont compréhensibles. C'est un audit de configuration préparée : aucune connexion directe aux équipements n'a été faite depuis VS Code.

## Plan contrôlé

| Zone | Réseau fourni | Découpage retenu |
| --- | --- | --- |
| LAN privé | `172.16.2.0/24` | 8 sous-réseaux `/27` pour les VLAN 10, 20, 30, 40, 50, 60, 80 et 99 |
| DMZ | `172.16.3.128/26` | VLAN 70 en `172.16.3.128/27`, VLAN 71 en `172.16.3.160/27` |

Le tableau complet avec les passerelles est dans [Dossier réseau](Dossier_reseau.md) et [Infrastructure/README.md](../README.md).

## Contrôles préparés

- Le VLAN 30 conserve la gestion de Proxmox 2, les serveurs internes et les deux serveurs Web `172.16.2.69` et `172.16.2.71`.
- Les trunks SW-L3 ↔ Routeur 2 et SW-L3 ↔ Proxmox 2 sont préparés pour les VLAN 30, 70 et 71 ; leurs ports physiques restent à confirmer.
- Routeur 2 porte `172.16.3.129` et `172.16.3.161`, les passerelles des deux sous-réseaux DMZ.
- Le VLAN 70 contient les caméras DMZ et le VLAN 71 contient le reverse proxy `172.16.3.162`, qui relaie vers les deux serveurs Web du VLAN 30.
- Le lien SW-L3 ↔ Routeur 1 (`Gi1/0/24`) est explicitement conservé sans changement.
- Les ACL gardent les services nécessaires et limitent l'administration au VLAN 99.

## Preuves à recueillir sur le matériel

```text
show version
show inventory
show interfaces status
show vlan brief
show interfaces trunk
show ip interface brief
show ip route
show access-lists
show mac address-table
show arp
```

Tests à faire : ping des passerelles LAN et DMZ, renouvellement DHCP, résolution DNS, supervision des caméras vers Zabbix, accès Web via `172.16.3.162`, accès du reverse proxy vers `172.16.2.69` et `172.16.2.71`, SSH depuis le VLAN 99 et refus d'un accès DMZ vers les VLAN internes.

## Résultat

La structure du dépôt contient une configuration lisible et un plan d'adressage cohérent avec les réseaux fournis. La conformité « réellement déployée » ne pourra être déclarée qu'après comparaison avec les sorties ci-dessus et validation du câblage réel.
