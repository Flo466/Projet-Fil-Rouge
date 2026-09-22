# Dossier réseau - Site C

## 1. Périmètre

Ce dossier adapte la méthode documentaire du site B au plan d'adressage fourni pour Site C. Il reprend le travail du planning de sprint 3 : switch L3, VLAN supplémentaires, relais DHCP, supervision, Routeur 2, second Proxmox, DMZ logique et reverse proxy.

Le PDF `nouveau adressage.pdf` fixe les neuf réseaux `/28`. Le planning fournit les rôles et les ports du switch, mais ses exemples en `/24` et son transit `192.168.0.0/30` chevauchent le nouveau VLAN 10. Le transit de production doit donc être séparé ; ce dossier propose `192.168.254.0/30`.

## 2. Plan d'adressage

| VLAN | Usage | Réseau | Passerelle | Hôtes utilisables | Diffusion |
| ---: | --- | --- | --- | --- | --- |
| 10 | Service 1 | `192.168.0.0/28` | `192.168.0.1` | `.2` à `.14` | `.15` |
| 20 | Service 2 | `192.168.0.16/28` | `192.168.0.17` | `.18` à `.30` | `.31` |
| 30 | Serveurs | `192.168.0.32/28` | `192.168.0.33` | `.34` à `.46` | `.47` |
| 40 | Wi-Fi employés | `192.168.0.48/28` | `192.168.0.49` | `.50` à `.62` | `.63` |
| 50 | VoIP | `192.168.0.64/28` | `192.168.0.65` | `.66` à `.78` | `.79` |
| 60 | Wi-Fi invités | `192.168.0.80/28` | `192.168.0.81` | `.82` à `.94` | `.95` |
| 70 | Caméras | `192.168.0.96/28` | `192.168.0.97` | `.98` à `.110` | `.111` |
| 80 | Réserve | `192.168.0.112/28` | `192.168.0.113` | `.114` à `.126` | `.127` |
| 99 | Management | `192.168.0.128/28` | `192.168.0.129` | `.130` à `.142` | `.143` |

Masque de tous les VLAN : `255.255.255.240`.

### Adresses de services proposées

Ces affectations utilisent des hôtes disponibles du VLAN 30 et doivent être confirmées avant déploiement :

| Rôle | Adresse | Passerelle |
| --- | --- | --- |
| Windows Server AD/DNS/DHCP | `192.168.0.34/28` | `192.168.0.33` |
| Zabbix | `192.168.0.35/28` | `192.168.0.33` |
| Routeur 2 côté VLAN 30 | `192.168.0.46/28` | `192.168.0.33` |
| Proxmox 2 | `192.168.200.2/24` | `192.168.200.1` |
| Reverse proxy | `192.168.200.10/24` | `192.168.200.1` |
| Web 1 | `192.168.200.11/24` | `192.168.200.1` |
| Web 2 | `192.168.200.12/24` | `192.168.200.1` |

Le réseau `192.168.200.0/24` est proposé pour la liaison Routeur 2-Proxmox 2. Le transit vers Routeur 1 est proposé en `192.168.254.0/30` : switch L3 `192.168.254.2`, Routeur 1 `192.168.254.1`.

## 3. Affectation des ports

| Ports du SW-L3 | Mode | VLAN | Usage |
| --- | --- | ---: | --- |
| Gi1/0/1 à 4 | Access | 10 | Service 1 |
| Gi1/0/5 à 8 | Access | 20 | Service 2 |
| Gi1/0/9 à 12 | Access | 30 | Serveurs et Routeur 2 selon raccordement |
| Gi1/0/13 à 16 | Access | 40 | Wi-Fi employés |
| Gi1/0/17 à 20 | Access | 50 | Téléphonie IP |
| Gi1/0/21 | Access | 99 | Poste d'administration |
| Gi1/0/22 | Access | 60 | Wi-Fi invités |
| Gi1/0/23 | Access | 70 | Caméra IP |
| Gi1/0/24 | Routé L3 | Transit proposé | Routeur 1 |

Le VLAN 80 est créé mais aucun port ne lui est attribué avant définition de son usage. Un point d'accès qui transporte plusieurs VLAN doit être configuré en trunk après vérification de sa compatibilité ; un port access ne transporte qu'un VLAN non marqué.

## 4. Services

Windows Server sur `192.168.0.34` héberge AD, DNS et DHCP. Les relais DHCP sont configurés sur les SVI des VLAN clients. Zabbix sur `192.168.0.35` surveille le switch, Routeur 1, Routeur 2, Proxmox et les services autorisés. Le domaine, les noms DNS, les plages DHCP et les ports de supervision restent à confirmer.

Routeur 2 isole Proxmox 2 sur `192.168.200.0/24`. Le reverse proxy est la seule cible d'une future publication Web ; les serveurs Web ne sont jamais publiés directement. Le DNS, l'AD, la base, la supervision et les interfaces de gestion restent sur des réseaux privés.

## 5. Routage

| Équipement | Destination | Prochain saut |
| --- | --- | --- |
| SW-L3 | `0.0.0.0/0` | `192.168.254.1` |
| SW-L3 | `192.168.200.0/24` | `192.168.0.46` |
| Routeur 1 | `192.168.0.0/24` | `192.168.254.2` |
| Routeur 1 | `192.168.200.0/24` | `192.168.254.2` |
| Routeur 2 | `0.0.0.0/0` | `192.168.0.33` |
| Proxmox 2 et VM | `0.0.0.0/0` | `192.168.200.1` |

La route vers `192.168.200.0/24` doit être filtrée sur le switch si les VLAN utilisateurs ne doivent pas atteindre la DMZ logique. Les règles de retour doivent être présentes sur Routeur 1 et Routeur 2 avant tout test applicatif.

## 6. Politique de filtrage

- VLAN 10 et 20 : autoriser DNS, DHCP et les services AD vers `192.168.0.34`, puis l'accès Internet ; refuser les autres VLAN privés.
- VLAN 40 : mêmes services d'entreprise ; aucun accès direct à la VoIP, aux caméras, aux invités ou au management.
- VLAN 50 : autoriser uniquement l'IPBX et les services VoIP identifiés ; refuser les autres réseaux internes.
- VLAN 60 : DHCP, DNS et Internet uniquement ; aucune nouvelle connexion vers les réseaux privés.
- VLAN 70 : caméras isolées ; autoriser seulement la supervision Zabbix et les flux explicitement validés.
- VLAN 80 : réseau réservé, bloqué tant que son usage n'est pas défini.
- VLAN 99 : administration depuis les postes habilités ; SSH/HTTPS vers les équipements et hyperviseurs uniquement.
- Réseau Proxmox 2 : reverse proxy vers Web 1 et Web 2 ; aucune nouvelle connexion vers les postes, serveurs ou management.

Les ACL IOS ne suivent pas automatiquement les sessions. Les retours DNS, DHCP, TCP et ICMP doivent être autorisés selon le matériel ou contrôlés par le pare-feu. La configuration fournie est un exemple à vérifier, pas une preuve de recette.

## 7. Mise en service et recette

1. Relever modèles, versions IOS, interfaces et câbles ; sauvegarder les configurations.
2. Créer les VLAN et SVI `/28`, vérifier chaque passerelle et le routage L3.
3. Installer Windows Server et Zabbix dans le VLAN 30 ; configurer les relais DHCP.
4. Déployer Routeur 2 et Proxmox 2 sur les réseaux proposés après validation des adresses.
5. Déployer reverse proxy et Web 1/Web 2 ; n'activer aucune publication WAN pendant les tests.
6. Vérifier les flux autorisés et refusés depuis chaque VLAN, les journaux ACL et les routes retour.
7. Sauvegarder les configurations uniquement après validation positive et négative.

Tests minimum : ping des passerelles, renouvellement DHCP, résolution DNS interne et externe, jonction au domaine depuis VLAN 10/20, accès Web via le reverse proxy, supervision Zabbix, refus du VLAN invités vers les réseaux privés, refus des caméras vers les postes et accès SSH depuis VLAN 99.
