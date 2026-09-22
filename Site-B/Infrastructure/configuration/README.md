# Inventaire des configurations

Cette liste est alignée sur `docs/schéma réseau.pdf`. Elle distingue la configuration disponible des configurations qui restent à produire ou à exporter depuis les équipements.

## Fichiers disponibles

| Fichier | Cible | Contenu | État |
| --- | --- | --- | --- |
| [SW1.conf](SW1.conf) | SW1 Cisco | VLAN 10 à 50, ports d’accès, SVI, relais DHCP vers `192.168.50.11`, port 24 routé, route par défaut et ACL entrante du VLAN 30 | Configuration unique à adapter au modèle et aux interfaces |

## Configurations à préparer

| Cible | Paramètres principaux à configurer | Vérifications et sauvegarde attendues |
| --- | --- | --- |
| R1 TP-Link | Port 1 sur le réseau amont `172.16.50.0/24` ; port 4 `10.0.0.254/29` ; port 5 `192.168.0.1/24` ; routes vers les VLAN et la DMZ via `10.0.0.253` ; NAT Internet sur le port 1 | Relever l’IP et la passerelle du port 1 ; confirmer le NAT des réseaux routés ; désactiver UPnP et l’administration WAN ; exporter la configuration |
| FW1 Hillstone | e0/0 `192.168.1.1/24` gestion ; e0/1 `10.0.0.253/29` AMONT ; e0/2 `10.0.10.254/29` LAN ; e0/3 `10.0.20.254/24` proposée DMZ ; routes LAN via `10.0.10.253` ; défaut via `10.0.0.254` | Créer les objets `.11` à `.14` et `.2` à `.6` ; appliquer la matrice de règles ; conserver le suivi de session et les journaux ; exporter la configuration |
| SW1 Cisco | Configuration fournie dans `SW1.conf` ; ACL complémentaires éventuelles pour les VLAN 10, 20, 40 et 50 ; éventuel accès d’administration | Vérifier le support L3, les noms d’interfaces, les compteurs ACL, le relais DHCP et la route par défaut ; sauvegarder la running-config validée |
| PC04 Proxmox | vmbr0 non étiqueté sur VLAN 50 ; gestion `192.168.50.10/24`, passerelle `192.168.50.254` ; VM `.11` à `.14` | Pare-feu local pour les flux intra-VLAN ; sauvegarde de la configuration réseau et des VM ; test de restauration |
| SRV1 Proxmox | vmbr0 non étiqueté sur la DMZ ; gestion `10.0.20.1/24`, passerelle `10.0.20.254` ; VM `.2` à `.6` | Pare-feu local pour DNS, reverse proxy et backends Web ; sauvegarde de la configuration réseau et des VM ; test de restauration |
| Windows interne | `192.168.50.11/24` ; AD DS, DNS, DHCP et GLPI ; DNS externe redirigé vers `10.0.20.2` | Définir domaine, nom d’hôte, certificats et sauvegarde système ; autoriser le DHCP dans AD ; limiter GLPI et l’accès base |
| Base Debian | `192.168.50.12/24` | Choisir moteur et port ; n’autoriser que le serveur Windows `.11` et l’administration depuis PC03 ; sauvegarder et tester la restauration |
| Zabbix | `192.168.50.13/24` | Définir agents, groupes, identifiants et ports 10050/10051 selon le mode ; limiter les sources et sauvegarder la base Zabbix |
| Squid | `192.168.50.14/24` | Choisir mode explicite ou transparent et port d’écoute ; définir ACL Web, journalisation et politique de contournement |
| DNS de DMZ | `10.0.20.2/24` | Autoriser la récursion uniquement depuis `192.168.50.11` et les hôtes DMZ retenus ; définir les redirecteurs externes ; ne pas publier le résolveur récursif |
| Reverse proxy | `10.0.20.3/24` | Définir les virtual hosts, certificats et backends Web1 `.4`, Web2 `.5`, Web3 `.6` ; seule cible possible d’un futur DNAT Web |
| Web1, Web2, Web3 | `10.0.20.4/24`, `.5/24`, `.6/24` | N’accepter HTTP/HTTPS applicatif que depuis le reverse proxy `.3` et l’administration depuis PC03 ; synchroniser contenu et journaux |
| AP1 Netis | `192.168.30.2/24`, passerelle `192.168.30.254`, DHCP désactivé, mode pont | Définir sécurité Wi-Fi et isolation des clients ; sauvegarder la configuration |
| Postes clients | PC01 `192.168.10.10`, PC02 `192.168.20.10`, PC03 `192.168.40.10` ; DNS `192.168.50.11` | Vérifier domaine, DNS, proxy éventuel, pare-feu local et accès autorisés/refusés |

## Dépendances de filtrage à ne pas oublier

- Le relais DHCP de SW1 et toutes les règles DNS/DHCP qui visaient `192.168.50.20` doivent viser `192.168.50.11`.
- Les accès Web LAN vers DMZ doivent viser le reverse proxy `10.0.20.3`, pas les serveurs Web `.4` à `.6`.
- Le flux DNS externe du serveur Windows doit viser `10.0.20.2`, pas l’ancienne adresse `.53`.
- Les flux `.11` vers `.12`, `.13` vers ses agents et les clients vers `.14` sont intra-VLAN 50 : ils ne passent pas par les ACL inter-VLAN de SW1.
- Les flux `.3` vers `.4` à `.6` sont intra-DMZ : ils ne passent pas par FW1. Les pare-feu Proxmox ou des VM doivent les limiter.
- Une future publication Internet doit chaîner le DNAT R1 vers `10.0.0.253`, puis FW1 vers `10.0.20.3`. Aucune publication n’est activée dans la cible actuelle.

## Paramètres encore à relever

- Modèles, versions et noms réels des interfaces de R1, FW1 et SW1.
- Adresse, mode d’attribution et passerelle de R1 port 1 dans `172.16.50.0/24`.
- Domaine AD, noms d’hôtes, noms DNS, certificats, résolveurs et serveurs NTP.
- Moteur et port de la base Debian ; mode et port de Squid ; périmètre Zabbix.
- Adresse proposée `10.0.20.254/24` de FW1 e0/3, à valider avant application.

La configuration de ce dossier ne doit être sauvegardée sur l’équipement qu’après inventaire du matériel, adaptation, accès console disponible et recette positive et négative.
