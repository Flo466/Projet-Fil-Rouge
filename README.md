# Projet Fil Rouge

Projet de préparation au titre professionnel Administrateur d’infrastructures sécurisées.

La documentation décrit le réseau, son câblage, son adressage, ses services, son routage et sa politique de filtrage. Elle est alignée sur le schéma `docs/schéma réseau.pdf` de la branche `yanis`, au commit `2276171` du 18 septembre 2026.

## Documents

| Document | Contenu |
| --- | --- |
| [Schéma réseau de référence](docs/sch%C3%A9ma%20r%C3%A9seau.pdf) | Topologie et adressage de référence |
| [Dossier technique](docs/Dossier_reseau.md) | Inventaire, réseaux, hôtes, VM, câblage, routage, filtrage, mise en service et recette |
| [Guide de configuration](docs/Configuration_Reseau_Commandes.md) | Paramètres par équipement, exemples IOS et PowerShell, procédures de vérification et retour arrière |
| [Inventaire des configurations](configuration/README.md) | Liste des configurations à préparer, appliquer, vérifier et sauvegarder |
| [Exemple de base SW1](configuration/SW1_base_IOS_exemple.txt) | VLAN, ports, SVI, relais DHCP et routage IOS ; ACL à compléter avant mise en service |
| [Exemple ACL Wi-Fi](configuration/SW1_WIFI_IN_exemple.txt) | Filtre IPv4 entrant du VLAN 30 ; dépend aussi des autorisations de retour sur le VLAN 50 |

## Architecture actualisée

```text
Internet / réseau NAT 172.16.50.0/24
  |
R1 port 1 (adresse et passerelle amont à relever)
  |
R1 port 4 (10.0.0.254/29)
  |
FW1 e0/1 (10.0.0.253/29) - zone AMONT
  |
  +-- e0/3 (10.0.20.254/24 proposée) - zone DMZ
  |      +-- SRV1 Proxmox (10.0.20.1/24)
  |             +-- DNS Windows       10.0.20.2/24
  |             +-- Reverse proxy     10.0.20.3/24
  |             +-- Web1              10.0.20.4/24
  |             +-- Web2              10.0.20.5/24
  |             +-- Web3              10.0.20.6/24
  |
  +-- e0/2 (10.0.10.254/29) - zone LAN
         |
       SW1 port 24 (10.0.10.253/29)
         +-- VLAN 10 Direction       192.168.10.0/24
         +-- VLAN 20 Comptabilité    192.168.20.0/24
         +-- VLAN 30 Wi-Fi           192.168.30.0/24
         +-- VLAN 40 Administration  192.168.40.0/24
         +-- VLAN 50 Serveurs        192.168.50.0/24
                +-- PC04 Proxmox     192.168.50.10/24
                       +-- Windows AD/DNS/DHCP/GLPI  192.168.50.11/24
                       +-- Base Debian              192.168.50.12/24
                       +-- Zabbix                    192.168.50.13/24
                       +-- Squid                     192.168.50.14/24
```

Les passerelles des VLAN 10 à 50 sont les adresses `.254` de SW1. SW1 route les échanges inter-VLAN et les filtre par ACL. FW1 contrôle les communications entre LAN, DMZ et amont. Les échanges entre VM d’un même pont Proxmox ne traversent ni SW1 ni FW1 et doivent donc être filtrés sur les hôtes ou dans Proxmox.

Le schéma fixe aussi les interfaces de gestion R1 port 5 `192.168.0.1/24`, FW1 e0/0 `192.168.1.1/24` et l’adresse de gestion SW1 `192.168.99.10/24`. Aucun raccordement permanent n’est représenté pour ces réseaux. Le VLAN 99 reste réservé et les accès R1/FW1 s’effectuent localement, de façon temporaire, tant qu’un réseau de gestion dédié n’est pas conçu.

## Changements issus du nouveau schéma

- Le transit R1-FW1 utilise désormais le **port 4** de R1, et non le port 3.
- Le **port 1 de R1** porte la sortie NAT vers le réseau amont `172.16.50.0/24`. L’adresse de R1, la passerelle et le mode d’attribution restent à relever.
- Les VM internes sont fixées à `192.168.50.11` à `.14`. Le serveur Windows regroupe AD, DNS, DHCP et GLPI ; la base Debian, Zabbix et Squid deviennent des machines distinctes.
- Les VM de DMZ sont fixées à `10.0.20.2` à `.6`. Le reverse proxy est séparé des trois serveurs Web.
- Le relais DHCP, le DNS des clients, les ACL et les tests qui visaient `192.168.50.20` visent désormais `192.168.50.11`.
- Une éventuelle publication Web doit cibler le reverse proxy `10.0.20.3`, jamais directement les serveurs Web `.4` à `.6`.
- Le neuvième câble, auparavant en réserve, est affecté au WAN de R1. Les neuf câbles sont donc utilisés dans la topologie représentée.

## Paramètres à confirmer

Le schéma ne précise pas l’adresse de FW1 e0/3 ; `10.0.20.254/24` reste la passerelle proposée pour la DMZ. Il ne donne pas non plus l’adresse exacte de R1 port 1, la passerelle amont, le domaine AD, les noms DNS, les certificats, les résolveurs et serveurs NTP externes, le port d’écoute de Squid ni le moteur et le port de la base Debian. Ces valeurs doivent être validées avant déploiement.

Les exemples Cisco supposent une syntaxe IOS compatible. Les réglages TP-Link et Hillstone sont documentés sous forme de paramètres, sans inventer de commandes pour un modèle qui n’a pas encore été relevé. Les règles couvrent IPv4 ; IPv6 doit faire l’objet d’un plan d’adressage et de filtrage séparé s’il est activé.

## Ordre de mise en service

1. Relever les modèles, versions, interfaces, paramètres WAN et capacités, puis sauvegarder les équipements.
2. Recâbler le WAN, R1, FW1 et les deux hyperviseurs ; vérifier les deux transits et la DMZ.
3. Configurer les VLAN, le routage, les ponts Proxmox et les adresses fixes des VM.
4. Déployer AD, DNS, DHCP, GLPI, la base, Zabbix, Squid, le DNS de DMZ, le reverse proxy et les trois serveurs Web.
5. Configurer le relais DHCP, les routes, le NAT et les matrices de filtrage.
6. Exécuter les tests autorisés et interdits, conserver les preuves, puis sauvegarder les configurations validées.

## État de validation

Les documents et exemples décrivent une configuration cible. Ils n’attestent pas que les commandes ont été appliquées ni que les tests de recette ont réussi sur le matériel. Toute prochaine modification du schéma doit être répercutée dans les deux documents Markdown, l’inventaire des configurations et les exemples du dossier `configuration`.
