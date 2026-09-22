# Routeur 2 et Proxmox 2

Le planning demande d'isoler le second serveur Proxmox derrière un deuxième routeur. Le planning historique indique `192.168.30.253/24` côté switch, mais cette adresse chevauche désormais le plan de Site C. La valeur adaptée proposée ici est `192.168.0.46/28`, dernière adresse utilisable du VLAN 30.

## Adressage proposé

| Équipement | Interface | Adresse | Réseau | Rôle |
| --- | --- | --- | --- | --- |
| SW-L3 | SVI VLAN 30 | `192.168.0.33/28` | VLAN 30 | Passerelle des serveurs |
| Routeur 2 | Interface 1 vers VLAN 30 | `192.168.0.46/28` | VLAN 30 | Liaison vers le réseau principal |
| Routeur 2 | Interface 2 vers Proxmox 2 | `192.168.200.1/24` | Réseau isolé | Passerelle du second hyperviseur |
| Proxmox 2 | Carte de gestion | `192.168.200.2/24` | Réseau isolé | Hôte de virtualisation |
| Reverse proxy | VM | `192.168.200.10/24` | Réseau isolé | Seule cible d'une future publication Web |
| Web 1 | VM | `192.168.200.11/24` | Réseau isolé | Serveur Web |
| Web 2 | VM | `192.168.200.12/24` | Réseau isolé | Serveur Web de secours ou second site |

Les adresses `192.168.0.46/28` et `192.168.200.0/24` sont des propositions à valider avec l'équipe. Le masque et l'adresse de Proxmox 2 n'étaient pas fixés dans le planning.

## Règles de routage

Routeur 2 doit avoir une route par défaut vers `192.168.0.33` côté VLAN 30. Le switch L3 doit avoir une route vers `192.168.200.0/24` via `192.168.0.46` :

```text
ip route 192.168.200.0 255.255.255.0 192.168.0.46
```

Si le switch ne doit pas exposer le réseau applicatif aux autres VLAN, cette route doit être filtrée par l'ACL de chaque SVI. Les retours de Routeur 1 vers `192.168.200.0/24` doivent passer par le switch puis Routeur 2, ou être masqués par Routeur 2 selon le choix NAT documenté.

## Filtrage minimal

- Autoriser depuis le VLAN 99 d'administration les seuls ports SSH/HTTPS nécessaires à Routeur 2, Proxmox 2 et au reverse proxy.
- Autoriser depuis le VLAN 30 l'administration et les mises à jour nécessaires ; ne pas autoriser l'accès direct aux serveurs Web depuis les VLAN utilisateurs.
- Autoriser vers le reverse proxy uniquement TCP 80/443 depuis les réseaux explicitement retenus.
- Autoriser le reverse proxy vers Web 1 et Web 2 sur le port applicatif retenu.
- Refuser toute nouvelle connexion du réseau `192.168.200.0/24` vers les VLAN utilisateurs et le VLAN 99 ; autoriser seulement les réponses aux sessions suivies.
- Ne publier ni Proxmox 2, ni Routeur 2, ni les interfaces d'administration.

## Mise en service

1. Sauvegarder les configurations et relever les interfaces réelles.
2. Raccorder Routeur 2 au port access ou au trunk du VLAN 30 selon le modèle du switch.
3. Configurer les deux interfaces, puis vérifier `192.168.0.33` et `192.168.200.1` depuis des postes autorisés.
4. Configurer le pont Proxmox 2 et ses VM sans activer de publication WAN.
5. Tester les routes, les règles positives et les refus, puis sauvegarder.
