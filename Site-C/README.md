# Site C / Site 3

Documentation du réseau, des services et de l'audit de Site C.

La nouvelle consigne professeur attribue à notre site le bloc global `172.16.128.0/18` (`255.255.192.0`). Pour conserver les VLAN, les passerelles et les ACL déjà préparés, les fichiers utilisent un découpage de travail en `/24` par VLAN. Ce découpage doit être validé avant mise en production.

## Documents

| Document | Contenu |
| --- | --- |
| [Plan d'adressage](Infrastructure/Plan_adressage_Site_C.md) | Bloc `/18`, VLAN, passerelles et sous-réseaux de travail |
| [Audit Site C](Infrastructure/docs/Audit_Site_C.md) | Écarts connus, preuves disponibles et plan de contrôle |
| [Planning Sprint 3](Infrastructure/Planning_Site_A_sprint3_routeur2.pdf) | Services, Routeur 2, Proxmox 2 et reverse proxy |
| [Dossier réseau](Infrastructure/docs/Dossier_reseau.md) | Architecture, services, routage et filtrage |
| [Guide de configuration](Infrastructure/docs/Configuration_Reseau_Commandes.md) | Commandes de vérification et de mise en service |
| [Inventaire des configurations](Infrastructure/configuration/README.md) | Fichiers à préparer, appliquer et sauvegarder |
| [Configuration Switch L3](Infrastructure/Switch%20L3.txt) | VLAN, noms, ports, SVI, ACL, relais DHCP et SSH |
| [Configuration Routeur 2](Infrastructure/Routeur%202.txt) | Interfaces, routes, ACL d'isolation et SSH |

## Découpage de travail

```text
Site 3 : 172.16.128.0/18
  VLAN 10 : 172.16.128.0/24  GW .1
  VLAN 20 : 172.16.129.0/24  GW .1
  VLAN 30 : 172.16.130.0/24  GW .1
  VLAN 40 : 172.16.131.0/24  GW .1
  VLAN 50 : 172.16.132.0/24  GW .1
  VLAN 60 : 172.16.133.0/24  GW .1
  VLAN 70 : 172.16.134.0/24  GW .1
  VLAN 80 : 172.16.135.0/24  GW .1
  VLAN 99 : 172.16.136.0/24  GW .1
  Transit R1 : 172.16.137.0/30
  DMZ/Proxmox 2 : 172.16.138.0/24
```

Les adresses et le masque `/18` de la photo sont la référence. Le détail `/24` ci-dessus est une proposition de travail, pas une validation du professeur. L'ancien `nouveau adressage.pdf` est conservé comme historique et ne doit plus être appliqué.
