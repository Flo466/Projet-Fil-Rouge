# Audit et recette — Site C

**Audit documentaire uniquement : aucun équipement n'a été configuré ni testé à distance.**

Le plan cible respecte LAN 172.16.2.0/24 (7 /27 attribués et 1 /27 libre) et DMZ 172.16.3.128/26 (2 /27). Les passerelles LAN et caméras sont sur le switch ; la passerelle proxy .161 est uniquement sur R2. Trois nœuds Proxmox sont prévus en VLAN 30.

| Contrôle sur la maquette | Résultat attendu |
|---|---|
| show vlan brief / show ip interface brief sur SW | VLAN LAN + caméra ; aucune passerelle SVI 71 |
| show ip route sur SW | 172.16.3.160/27 via 172.16.2.70 |
| show ip interface brief / show ip route sur R2 | Gi0/0/1 .70, Gi0/0/0 .161 ; défaut via .65 |
| Accès proxy depuis VLAN 10/20/40 | HTTP/HTTPS fonctionnels, réponses reçues |
| Proxy vers Web 1 .69 et Web 2 .71 | HTTP/HTTPS autorisés |
| Proxy vers autres services LAN / caméras | Nouvelles connexions refusées |
| VLAN 99 vers SSH R2 et gestion Proxmox | Aller et retour fonctionnels |
| VLAN 50 / DHCP des VLAN clients | VoIP conservée ; bail et DNS fonctionnels |
| Caméras | Supervision selon protocole réel à confirmer ; refus des autres flux |
| Serveur VLAN 30 vers client/admin/caméra : nouvelle connexion non prévue | Refusée ; retours DNS/DHCP/admin et Zabbix prévus à tester séparément |
| Serveur VLAN 30 vers Internet | HTTP/HTTPS et NTP autorisés ; autres ports refusés ; DNS externe réservé à .66 |
| Deux hôtes du VLAN 30 | Échanges locaux non filtrés par ACL_VLAN30 |
| Proxmox 2 | Deux bridges distincts, aucune IP hôte sur la DMZ |
| Cluster 3 nœuds | Quorum, stockage, watchdog et bascule à tester |

Avant déploiement : confirmer les ports 9–12, les noms des cartes Proxmox et les IP libres. Le transit R1 reprend ton extrait (192.168.0.2/30 vers .1). Le DNS de la VM proxy et ses mises à jour ne sont pas ouverts par les ACL actuelles : ajouter des exceptions précises lorsque leurs destinations seront connues. La publication Internet/NAT reste hors de cette modification.

Conserver les sorties show access-lists et les résultats positifs/négatifs, puis sauvegarder. Aucun résultat de HA ou de déploiement n'est présumé acquis.
