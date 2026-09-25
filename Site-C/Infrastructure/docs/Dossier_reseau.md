# Câblage et fonctionnement

## Ports du switch

| Ports | Affectation |
|---|---|
| Gi1/0/1–4 | Access VLAN 10 |
| Gi1/0/5–8 | Access VLAN 20 |
| Gi1/0/9–12 | Access VLAN 30 : Proxmox 1, 2, 3 et Routeur 2, ordre **à confirmer** |
| Gi1/0/13–16 | Access VLAN 40 |
| Gi1/0/17–20 | Access VLAN 50 VoIP |
| Gi1/0/21 | Access VLAN 99 |
| Gi1/0/22 | Access VLAN 60 |
| Gi1/0/23 | Access VLAN 70 caméras |
| Gi1/0/24 | Lien Routeur 1 conservé |

Routeur 2 **Gi0/0/1** rejoint un port VLAN 30 du switch. **Gi0/0/0** rejoint directement la deuxième carte de Proxmox 2. Tous ces câbles sont non tagués, sans trunk.

## Proxmox et haute disponibilité

Trois nœuds sont prévus sur le VLAN 30 : Proxmox 1 (.72), Proxmox 2 (.68) et Proxmox 3 (.73). Proxmox 1 héberge initialement Web 1 (.69) et Web 2 (.71).

Sur Proxmox 2 :
- Carte 1 → bridge LAN (ex. vmbr0), gestion 172.16.2.68/27 et unique passerelle hôte 172.16.2.65.
- Carte 2 → bridge DMZ (ex. vmbr1), **sans IP ni passerelle sur l'hôte**.
- VM reverse proxy → bridge DMZ uniquement, sans tag VLAN, 172.16.3.162/27 et passerelle 172.16.3.161.
- Ne pas réunir les deux cartes dans le même bridge et ne pas activer de routage LAN/DMZ sur l'hôte.

Trois nœuds permettent de prévoir le quorum du cluster ; la HA demande aussi stockage partagé ou réplication adaptée, watchdog et tests de bascule. Le reverse proxy reste dépendant du câble DMZ de Proxmox 2 : **pas de HA automatique du proxy** tant que les autres nœuds n'ont pas accès au même réseau DMZ isolé. Un cluster à trois nœuds n'apporte pas cette connectivité à lui seul.

## Routes et filtrage

- Switch : route 172.16.3.160/27 via 172.16.2.70 ; caméras directement sur SVI 70.
- R2 : route par défaut vers 172.16.2.65 ; DMZ directement connectée sur Gi0/0/0.
- Utilisateurs → proxy → Web 1/Web 2 : HTTP/HTTPS.
- Caméras : DNS et supervision prévue vers Zabbix ; administration depuis VLAN 99.
- Les retours du proxy traversant le SVI 30 sont autorisés explicitement. Aucun NAT entre LAN et DMZ.
- Les échanges entre hôtes du VLAN 30 restent en niveau 2 : ils ne passent pas par les ACL des SVI. Filtrer sur les hôtes si nécessaire.
- Les ACL TCP « established » vérifient les bits ACK/RST ; elles ne remplacent pas un pare-feu avec suivi de connexions.

## Filtrage du VLAN 30

Le VLAN serveurs ne dispose plus d'une autorisation générale vers toutes les destinations. Son ACL en entrée autorise les réponses DNS/DHCP de .66, les retours TCP et ping vers les administrateurs, les réponses Zabbix aux caméras et les retours du proxy via R2. Les autres flux vers les réseaux privés sont bloqués. Vers les destinations externes, seuls HTTP/HTTPS et NTP sont ouverts aux serveurs ; seul .66 peut effectuer des requêtes DNS externes. Tout le reste est refusé.

Ces sorties sont limitées par port, pas par serveur externe : fixer les résolveurs, dépôts et serveurs NTP permettra de restreindre aussi les destinations. Les autorisations de retour UDP reposent sur les IP/ports, et `established` sur ACK/RST : aucun suivi de session. L'ACL ne filtre ni les communications internes au VLAN 30, ni les réponses Internet entrant par R1. AD au-delà de DNS/DHCP, supervision par interrogation et nouveaux services nécessiteront leurs propres flux validés ; ils ne sont pas ouverts implicitement.

## Application

Les fichiers décrivent l'état cible. Avant application, sauvegarder les configurations et remplacer A_REMPLACER. Remplacer entièrement ACL_VLAN30 (notamment son ancien `permit ip 172.16.2.64 0.0.0.31 any`) lors d’une fenêtre de maintenance ; ajouter les nouvelles lignes après cette permission ne suffit pas. Retirer les anciennes ACL ou sous-interfaces incompatibles ; ne pas cumuler les versions. Si une ancienne SVI 71 existe sur le switch, la supprimer pour que seule R2 porte 172.16.3.161. Vérifier le lien R1 avec l'équipe.

[Plan complet](../README.md) · [Tests](Audit_Site_C.md)
