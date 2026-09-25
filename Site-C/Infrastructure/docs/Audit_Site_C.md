# Vérifications de la maquette

Cette liste décrit les résultats attendus. Aucun équipement réel n'a été testé à distance.

| À vérifier | Résultat attendu |
|---|---|
| `show vlan brief` et `show ip interface brief` | VLAN, ports et passerelles conformes au plan ; pas de SVI 71 ni VLAN 80 |
| Routes | Switch : DMZ proxy via `.70` ; R2 : défaut via `.65` |
| PC VLAN 10 → proxy HTTP/HTTPS | Page reçue, avec Web 1 puis Web 2 comme cible |
| PC VLAN 10 → Web 1/2 directement | Refus |
| Proxy → Web 1/2 sur 80/443 | Connexion et réponses autorisées |
| Proxy → autre serveur LAN sur SSH | Refus par R2 |
| DHCP et DNS des clients | Bail, passerelle et résolution fonctionnels |
| VLAN 99 → SSH R2 et interface Proxmox | Connexion et réponses ; SSH R2 refusé depuis les autres VLAN |
| Serveur → nouvelle connexion vers client/caméra/admin | Refus hors exceptions documentées |
| Serveur → Internet | HTTP/HTTPS/NTP autorisés ; DNS externe réservé à `.66`, sous réserve de R1 |
| Caméras | DNS et flux Zabbix actif si matériel compatible ; autres flux refusés |
| Proxmox 2 | Deux bridges séparés ; VM proxy uniquement dans la DMZ |

Confirmer les ports 9–12, les cartes Proxmox et les IP libres. La HA, AD complet et le protocole réel de supervision restent à valider séparément. Conserver les compteurs `show access-lists` et les résultats obtenus, puis sauvegarder les équipements.
