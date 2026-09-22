# Routeur 2 et Proxmox 2

Le planning demande d'isoler le second serveur Proxmox derrière Routeur 2. Le bloc du professeur pour Site C est `172.16.64.0/18`. Le découpage ci-dessous est celui utilisé dans les configurations du dépôt et reste à valider.

## Adressage de travail

| Équipement | Interface | Adresse | Passerelle | Rôle |
| --- | --- | --- | --- | --- |
| SW-L3 | SVI VLAN 30 | `172.16.66.1/24` | - | Passerelle des serveurs |
| Routeur 2 | Interface vers VLAN 30 | `172.16.66.254/24` | `172.16.66.1` | Liaison vers le réseau principal |
| Routeur 2 | Interface vers Proxmox 2 | `172.16.74.1/24` | - | Passerelle applicative |
| Proxmox 2 | Carte de gestion | `172.16.74.2/24` | `172.16.74.1` | Hôte de virtualisation |
| Reverse proxy | VM | `172.16.74.10/24` | `172.16.74.1` | Seule cible Web publiée |
| Web 1 | VM | `172.16.74.11/24` | `172.16.74.1` | Serveur Web |
| Web 2 | VM | `172.16.74.12/24` | `172.16.74.1` | Serveur Web de secours |

## Routage

Routeur 2 possède une route par défaut vers le SW-L3 :

```text
ip route 0.0.0.0 0.0.0.0 172.16.66.1
```

Le SW-L3 doit connaître le réseau applicatif :

```text
ip route 172.16.74.0 255.255.255.0 172.16.66.254
```

Routeur 1 doit avoir une route vers `172.16.74.0/24` via le transit du SW-L3, si ce réseau doit sortir vers Internet. Les routes et le NAT ne doivent être appliqués qu'après validation du découpage.

## Filtrage

- VLAN 10, 20 et 40 : HTTP/HTTPS vers le reverse proxy uniquement.
- VLAN 99 : SSH/HTTPS/8006 et ICMP d'administration vers Routeur 2, Proxmox et les VM autorisées.
- Reverse proxy : HTTP/HTTPS vers Web 1 et Web 2.
- Réseau `172.16.74.0/24` : aucune nouvelle connexion vers les VLAN internes ; seuls les retours établis sont autorisés.
- Aucun accès Internet direct à Routeur 2, Proxmox ou aux interfaces d'administration.

La configuration complète est dans `Infrastructure/Routeur 2.txt`. Tester chaque règle par un flux autorisé et un flux refusé avant `write memory`.
