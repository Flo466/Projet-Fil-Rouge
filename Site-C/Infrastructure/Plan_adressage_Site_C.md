# Plan d'adressage Site C - bloc du professeur et découpage de travail

## Bloc attribué

Site C correspond au **Site 2** dans la consigne. Le bloc fourni est `172.16.64.0/18`, soit le masque `255.255.192.0` et la plage `172.16.64.0` à `172.16.127.255`.

La photo ne fixe pas le découpage interne. Le tableau ci-dessous est donc le découpage de travail utilisé pour garder les VLAN, les passerelles et les ACL cohérents dans le dépôt. Il doit être validé par le professeur avant application sur les équipements.

## VLAN et passerelles proposées

| VLAN | Usage | Réseau de travail | Passerelle | Plage d'hôtes |
| ---: | --- | --- | --- | --- |
| 10 | Service 1 | `172.16.64.0/24` | `172.16.64.1` | `.2` à `.254` |
| 20 | Service 2 | `172.16.65.0/24` | `172.16.65.1` | `.2` à `.254` |
| 30 | Serveurs | `172.16.66.0/24` | `172.16.66.1` | `.2` à `.254` |
| 40 | Wi-Fi employés | `172.16.67.0/24` | `172.16.67.1` | `.2` à `.254` |
| 50 | VoIP | `172.16.68.0/24` | `172.16.68.1` | `.2` à `.254` |
| 60 | Wi-Fi invités | `172.16.69.0/24` | `172.16.69.1` | `.2` à `.254` |
| 70 | Caméras IP | `172.16.70.0/24` | `172.16.70.1` | `.2` à `.254` |
| 80 | Réserve / extension | `172.16.71.0/24` | `172.16.71.1` | `.2` à `.254` |
| 99 | Management | `172.16.72.0/24` | `172.16.72.1` | `.2` à `.254` |

## Réseaux d'infrastructure proposés

| Usage | Réseau | Équipement / adresse |
| --- | --- | --- |
| Transit SW-L3 vers Routeur 1 | `172.16.73.0/30` | SW-L3 `.2`, Routeur 1 `.1` |
| Réseau Routeur 2 / Proxmox 2 / DMZ | `172.16.74.0/24` | Routeur 2 `.1`, Proxmox 2 `.2` |
| Reverse proxy | `172.16.74.10/24` | Passerelle `172.16.74.1` |
| Web 1 | `172.16.74.11/24` | Passerelle `172.16.74.1` |
| Web 2 | `172.16.74.12/24` | Passerelle `172.16.74.1` |
| Routeur 2 côté VLAN 30 | `172.16.66.254/24` | Passerelle `172.16.66.1` |

Le bloc `/18` conserve de la place pour les extensions jusqu'à `172.16.127.255`. Les adresses exactes des services, du WAN et du pare-feu restent à confirmer avec l'équipe.

## Statut

Les adresses ci-dessus permettent de conserver les VLAN, les SVI, les ACL et les exemples de services dans un plan cohérent. Elles sont une proposition de découpage interne ; seules les valeurs `172.16.64.0/18` et `255.255.192.0` sont directement confirmées par la consigne photographiée.

L'ancien fichier `nouveau adressage.pdf` est conservé comme historique, mais ses réseaux `192.168.0.0/28` ne doivent plus être appliqués.
