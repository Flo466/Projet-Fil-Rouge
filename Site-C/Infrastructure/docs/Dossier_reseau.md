# Dossier réseau - Site C / Site 3

## 1. Référence d'adressage

La consigne professeur attribue à notre site le bloc `172.16.128.0/18` avec le masque `255.255.192.0`. La plage globale va de `172.16.128.0` à `172.16.191.255`.

La consigne ne fournit pas le découpage interne. Pour garder les VLAN et les ACL exploitables, ce dépôt utilise un découpage de travail en `/24`, documenté dans [Plan_adressage_Site_C.md](../Plan_adressage_Site_C.md). Ce choix doit être validé avant tout déploiement réel.

## 2. VLAN, passerelles et rôles

| VLAN | Usage | Réseau de travail | Passerelle |
| ---: | --- | --- | --- |
| 10 | Service 1 | `172.16.128.0/24` | `172.16.128.1` |
| 20 | Service 2 | `172.16.129.0/24` | `172.16.129.1` |
| 30 | Serveurs | `172.16.130.0/24` | `172.16.130.1` |
| 40 | Wi-Fi employés | `172.16.131.0/24` | `172.16.131.1` |
| 50 | VoIP | `172.16.132.0/24` | `172.16.132.1` |
| 60 | Wi-Fi invités | `172.16.133.0/24` | `172.16.133.1` |
| 70 | Caméras IP | `172.16.134.0/24` | `172.16.134.1` |
| 80 | Réserve | `172.16.135.0/24` | `172.16.135.1` |
| 99 | Management | `172.16.136.0/24` | `172.16.136.1` |

| Rôle | Adresse de travail | Passerelle |
| --- | --- | --- |
| Windows AD/DNS/DHCP | `172.16.130.10/24` | `172.16.130.1` |
| Zabbix | `172.16.130.11/24` | `172.16.130.1` |
| IPBX | `172.16.130.12/24` | `172.16.130.1` |
| Routeur 2 vers VLAN 30 | `172.16.130.254/24` | `172.16.130.1` |
| Proxmox 2 | `172.16.138.2/24` | `172.16.138.1` |
| Reverse proxy | `172.16.138.10/24` | `172.16.138.1` |
| Web 1 / Web 2 | `172.16.138.11` / `.12` | `172.16.138.1` |

Le transit vers Routeur 1 est proposé en `172.16.137.0/30` : SW-L3 `.2`, routeur `.1`. Le réseau applicatif de Routeur 2 est `172.16.138.0/24` dans le découpage de travail.

## 3. Ports et VLAN

| Ports SW-L3 | Mode | VLAN | Usage |
| --- | --- | ---: | --- |
| Gi1/0/1 à 4 | Access | 10 | Service 1 |
| Gi1/0/5 à 8 | Access | 20 | Service 2 |
| Gi1/0/9 à 12 | Access | 30 | Serveurs / Routeur 2 selon raccordement |
| Gi1/0/13 à 16 | Access | 40 | Wi-Fi employés |
| Gi1/0/17 à 20 | Access | 50 | VoIP |
| Gi1/0/21 | Access | 99 | Administration |
| Gi1/0/22 | Access | 60 | Wi-Fi invités |
| Gi1/0/23 | Access | 70 | Caméra IP |
| Gi1/0/24 | Routé L3 | Transit | Routeur 1 |

Le VLAN 80 est créé mais aucun port ne lui est attribué tant que son usage n'est pas confirmé. Un point d'accès multi-SSID devra utiliser un trunk avec une liste de VLAN limitée.

## 4. Routage et services

Le SW-L3 route les VLAN et utilise `172.16.137.1` comme route par défaut. Routeur 2 utilise `172.16.130.1` comme route par défaut et dessert `172.16.138.0/24`. Windows Server fournit AD, DNS et DHCP sur `172.16.130.10`; les SVI clientes relaient DHCP vers cette adresse. Zabbix est proposé en `172.16.130.11`.

Le reverse proxy `172.16.138.10` est la seule cible Web autorisée. Web 1 et Web 2 restent derrière Routeur 2. Les interfaces d'administration ne sont accessibles que depuis le VLAN 99.

## 5. Politique ACL

- VLAN 10 et 20 : DNS, DHCP, AD et HTTPS vers `172.16.130.10`, puis Internet ; autres réseaux internes refusés.
- VLAN 40 : mêmes services d'entreprise, accès aux VLAN 10/20 selon besoin ; autres réseaux privés refusés.
- VLAN 50 : DHCP/DNS et IPBX `172.16.130.12` ; autres réseaux internes refusés.
- VLAN 60 : DHCP, DNS et Internet uniquement ; aucun accès privé.
- VLAN 70 : supervision Zabbix `172.16.130.11:10051` uniquement ; autres flux refusés.
- VLAN 80 : bloqué en attente d'un usage.
- VLAN 99 : administration SSH/HTTPS/8006 et diagnostic vers les équipements et serveurs autorisés.
- Zone `172.16.138.0/24` : reverse proxy vers Web 1/Web 2 ; pas de nouvelles connexions vers les VLAN internes.

Les ACL sont dans `Infrastructure/Switch L3.txt` et `Infrastructure/Routeur 2.txt`. Les règles sont des modèles ; vérifier les retours TCP/UDP/ICMP et les compteurs avant sauvegarde.

## 6. Mise en service

1. Faire valider le découpage `/24` dans le bloc `/18`.
2. Relever les modèles, ports, versions IOS et câbles ; exporter les configurations initiales.
3. Configurer les VLAN, SVI, relais DHCP, ports et SSH du SW-L3.
4. Configurer Routeur 2, Proxmox 2, le reverse proxy et les Web.
5. Tester les flux autorisés et interdits, puis vérifier les routes retour.
6. Sauvegarder uniquement après validation positive et négative.
