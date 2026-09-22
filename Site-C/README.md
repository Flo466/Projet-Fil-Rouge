# Site C

Documentation du réseau, des services et de la mise en service du site C.

Le plan d'adressage de Site C utilise des sous-réseaux `/28` dans `192.168.0.0/24`. Les anciennes adresses `/24` du planning générique ne sont donc pas reprises lorsqu'elles chevauchent ces réseaux.

## Documents

| Document | Contenu |
| --- | --- |
| [Plan d'adressage](Infrastructure/nouveau%20adressage.pdf) | Réseaux, passerelles, hôtes et masques de Site C |
| [Planning Sprint 3](Infrastructure/Planning_Site_A_sprint3_routeur2.pdf) | Services, supervision, Routeur 2, Proxmox 2 et reverse proxy |
| [Dossier réseau](Infrastructure/docs/Dossier_reseau.md) | Architecture, services, routage et filtrage |
| [Guide de configuration](Infrastructure/docs/Configuration_Reseau_Commandes.md) | Commandes IOS et paramètres de mise en service |
| [Inventaire des configurations](Infrastructure/configuration/README.md) | Fichiers à préparer et vérifier |
| [Configuration Switch L3](Infrastructure/Switch%20L3.txt) | Exemple IOS adapté au plan `/28` |
| [Routeur 2 et Proxmox 2](Infrastructure/configuration/Routeur2_Proxmox2.md) | Isolation du second hyperviseur et réseau applicatif |

## Architecture

```text
Internet -- Routeur 1 / pare-feu -- transit proposé -- SW-L3
                                      192.168.254.0/30
                                             |
             +-------------------------------+------------------+
             |                                                  |
      VLAN 10, 20, 40, 50, 60, 70, 80                    VLAN 30
      postes, Wi-Fi, VoIP, caméras                       serveurs
                                                        192.168.0.32/28
                                                               |
                                                   AD/DNS/DHCP, Zabbix
                                                               |
                                                   Routeur 2 .46 proposé
                                                               |
                                                   192.168.200.0/24 proposé
                                                               |
                                                   Proxmox 2, proxy, Web
```

Les passerelles du plan fourni sont `.1`, `.17`, `.33`, `.49`, `.65`, `.81`, `.97`, `.113` et `.129` pour les VLAN 10, 20, 30, 40, 50, 60, 70, 80 et 99. Le transit vers Routeur 1 et le réseau de Proxmox 2 sont proposés séparément, car le planning historique `192.168.0.0/30` entrerait en conflit avec le VLAN 10.

Les fichiers décrivent une cible de configuration. Les modèles, ports physiques, adresse WAN, domaine, NAT et ports applicatifs doivent être relevés avant application. Les commandes IOS sont des exemples à adapter au switch réel.
