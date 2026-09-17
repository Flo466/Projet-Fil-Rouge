# Projet Fil Rouge

Projet de préparation au titre professionnel Administrateur d’infrastructures sécurisées.

La documentation décrit le réseau, son câblage, son adressage, les services, le routage et la politique de filtrage à mettre en place. Elle est alignée sur le dernier schéma du 17 septembre 2026, au commit `743c5c2`, intégré dans `main` par `8476785`.

## Documents

| Document | Contenu |
| --- | --- |
| [Schéma réseau de référence](TPAIS%20projet%20diagramme.pdf) | Topologie fournie, conservée dans sa version originale |
| [Dossier technique Word](Dossier_reseau.docx) | Inventaire, réseaux, hôtes, VM, câblage, routage, filtrage, mise en service et recette |
| [Dossier technique en Markdown](docs/Dossier_reseau.md) | Version textuelle du dossier pour la lecture et la revue des modifications dans Git |
| [Guide de configuration PDF](Configuration_Reseau_Commandes.pdf) | Paramètres par équipement, exemples IOS et PowerShell, procédures de vérification et retour arrière |
| [Guide de configuration en Markdown](docs/Configuration_Reseau_Commandes.md) | Version textuelle du guide avec les commandes copiables |
| [Exemple de base SW1](configuration/SW1_base_IOS_exemple.txt) | VLAN, ports, SVI, relais DHCP et routage IOS ; ACL à ajouter avant mise en service |
| [Exemple ACL Wi-Fi](configuration/SW1_WIFI_IN_exemple.txt) | Filtre IPv4 entrant du VLAN 30 ; dépend aussi des autorisations de retour sur VLAN 50 |

## Architecture actualisée

```text
R1 port 3 (10.0.0.254/29)
  |
  | Transit 10.0.0.248/29
  |
FW1 e0/1 (10.0.0.253/29) - zone AMONT
  |
  +-- e0/3 (10.0.20.254/24 proposée) - zone DMZ
  |      +-- SRV1 Proxmox (10.0.20.1/24)
  |             +-- WEB01 (10.0.20.10/24 proposée)
  |             +-- DNSDMZ01 (10.0.20.53/24 proposée)
  |
  +-- e0/2 (10.0.10.254/29) - zone LAN
         |
         | Transit 10.0.10.248/29
         |
       SW1 port 24 (10.0.10.253/29)
         +-- VLAN 10 Direction       192.168.10.0/24
         +-- VLAN 20 Comptabilité    192.168.20.0/24
         +-- VLAN 30 Wi-Fi           192.168.30.0/24
         +-- VLAN 40 Administration  192.168.40.0/24
         +-- VLAN 50 Serveurs        192.168.50.0/24
                +-- PC04 Proxmox     192.168.50.10/24
                       +-- DC01      192.168.50.20/24 proposée
                       +-- GLPI01    192.168.50.30/24 proposée
```

Les passerelles des VLAN 10 à 50 sont les adresses `.254` de SW1. SW2 est conservé en réserve et n’intervient plus dans les communications. Le câblage actif utilise huit des neuf câbles disponibles ; C02 reste libre. Le port 3 de R1 remplace l’ancien raccordement du port 4 vers SW2.

SW1 route les échanges entre VLAN et doit les filtrer par ACL. FW1 contrôle les communications entre LAN, DMZ et amont. Les échanges à l’intérieur d’un même VLAN nécessitent les pare-feu des hôtes, de Proxmox ou l’isolation Wi-Fi.

## Compléments proposés

Le schéma fixe les réseaux, les interfaces et les adresses des hyperviseurs. Les documents complètent les éléments suivants comme **propositions de mise en service**, sans les présenter comme une configuration déjà appliquée :

- `10.0.20.254/24` pour FW1 e0/3 et la passerelle de la DMZ ; `.253` reste libre.
- DC01 `192.168.50.20` pour AD, DNS et DHCP ; GLPI01 `192.168.50.30` pour GLPI.
- WEB01 `10.0.20.10` pour le Web et le reverse proxy ; DNSDMZ01 `10.0.20.53` pour la résolution externe à accès restreint.
- DHCP Wi-Fi de `192.168.30.100` à `.199`, passerelle `192.168.30.254`, DNS `192.168.50.20`, bail proposé de huit heures.
- Direction et Comptabilité autorisées vers AD, DNS, GLPI et le Web ; Wi-Fi isolé avec DNS, DHCP et Web vers Internet ; administration depuis PC03 `192.168.40.10`.
- NAT Internet sur R1 si le modèle prend en charge les réseaux routés. Le guide décrit un repli avec SNAT sur FW1. Aucune publication WAN n’est activée par défaut.

L’adresse de gestion SW1 `192.168.99.10/24` est celle du nouveau schéma. Son transport n’étant pas défini, le VLAN 99 reste réservé et aucune joignabilité de cette IP n’est annoncée. L’administration de SW1 se fait provisoirement depuis PC03 via `192.168.40.254`.

Le dernier schéma ajoute les interfaces de gestion **R1 port 5 `192.168.0.1/24`** et **FW1 e0/0 `192.168.1.1/24`**. Le guide décrit un accès local successif depuis PC03, temporairement configuré en `192.168.0.10/24` puis `192.168.1.10/24`, sans passerelle. Ces deux IP de poste sont des propositions à vérifier. Aucun raccordement permanent ni route vers ces réseaux n’est ajouté au plan. Après intervention, PC03 retrouve son câblage et sa configuration du VLAN 40.

## Ordre de mise en service

1. Relever les modèles, versions, interfaces et capacités, puis sauvegarder les équipements.
2. Recâbler R1, FW1 et SRV1 ; vérifier les deux transits et la DMZ.
3. Configurer les VLAN, le routage, les hyperviseurs et les VM.
4. Déployer DNS, AD, DHCP, GLPI et Web ; configurer le relais DHCP.
5. Appliquer les matrices de filtrage et le NAT adapté au matériel.
6. Effectuer les tests autorisés et interdits, conserver leurs preuves puis sauvegarder les configurations validées.

## État de validation

Les documents et les exemples décrivent une configuration cible. Les tests de recette restent à exécuter sur les équipements ; les résultats attendus ne sont pas des résultats observés.

Les modèles exacts, les paramètres WAN, le domaine AD, les certificats, les résolveurs et NTP externes, ainsi que les associations d’alimentation doivent être relevés avant déploiement. Les exemples Cisco supposent une syntaxe IOS compatible. Les réglages TP-Link et Hillstone sont décrits sous forme de paramètres à saisir, sans leur attribuer une CLI non vérifiée.

Les règles couvrent IPv4. Si IPv6 est utilisé, son adressage et son filtrage doivent être documentés séparément.

Lors d’une prochaine modification, mettre à jour les versions Word ou PDF **et** leurs versions Markdown afin de conserver la cohérence des informations.
