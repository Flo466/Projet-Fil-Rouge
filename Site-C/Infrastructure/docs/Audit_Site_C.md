# Audit documentaire et de préparation - Site C

## Périmètre

Cet audit compare les fichiers du dépôt avec la nouvelle consigne d'adressage photographiée et avec la procédure `audit_infrastructure_reellement_deployee.html`. Il s'agit d'un audit documentaire : aucune connexion au switch, au routeur, au pare-feu ou aux VM n'a été possible depuis VS Code. Les constats « déployé » devront donc être prouvés par des exports et des tests sur la maquette autorisée.

## Référence d'adressage

| Élément | Valeur retenue |
| --- | --- |
| Site | Site 3 - notre site |
| Bloc | `172.16.128.0/18` |
| Masque | `255.255.192.0` |
| Plage | `172.16.128.0` à `172.16.191.255` |
| Découpage interne | Proposition `/24` par VLAN, à valider |

## Constats

| ID | Niveau | Constat | Action |
| --- | --- | --- | --- |
| A-01 | Élevé | Les anciens fichiers utilisaient `192.168.0.0/28`, hors du bloc Site 3. | Remplacés dans les documents et les configurations de travail par `172.16.128.0/18`. |
| A-02 | Élevé | La photo ne fournit pas le découpage interne du `/18`. | Les `/24` utilisés ici sont marqués « à valider » partout. |
| A-03 | Élevé | Une configuration ne peut pas être déclarée conforme sans preuve de l'équipement réel. | Relever running-config, câblage, tables MAC/ARP et résultats de tests. |
| A-04 | Moyen | Les adresses WAN, le NAT, le domaine AD et les ports applicatifs ne sont pas fournis. | Compléter après inventaire et conserver les valeurs confirmées. |
| A-05 | Moyen | Les accès d'administration et les flux inter-VLAN doivent être testés en positif et en négatif. | Exécuter la recette depuis chaque VLAN et conserver les preuves. |

## Éléments préparés dans le dépôt

- `Infrastructure/Switch L3.txt` conserve les noms de VLAN, les ports, les SVI, le relais DHCP, les ACL et SSH.
- `Infrastructure/Routeur 2.txt` contient les interfaces, les routes, les ACL d'isolation de Proxmox 2 et SSH.
- `Infrastructure/Plan_adressage_Site_C.md` centralise le bloc `/18` et le découpage de travail.
- `Infrastructure/docs/Dossier_reseau.md` et `Configuration_Reseau_Commandes.md` utilisent les mêmes adresses.
- `Infrastructure/configuration/DMZ/Config_Ansible` utilise les adresses du réseau applicatif de travail `172.16.138.0/24`.

## Preuves à recueillir sur la maquette

```text
show version
show inventory
show interfaces status
show vlan brief
show interfaces trunk
show ip interface brief
show ip route
show access-lists
show mac address-table
show arp
```

Depuis des postes autorisés :

```text
ipconfig /all
ipconfig /renew
ping <passerelle-du-vlan>
tracert <destination>
nslookup <nom-interne> <serveur-dns>
```

Tester au minimum : DNS/DHCP/AD depuis les VLAN 10, 20 et 40 ; Internet depuis le VLAN 60 sans accès aux réseaux privés ; supervision des caméras depuis Zabbix ; Web via le reverse proxy ; administration SSH depuis le VLAN 99 ; refus du réseau Proxmox 2 vers les VLAN internes.

## Conclusion

La documentation et les configurations sont alignées sur le bloc `172.16.128.0/18` et conservent tous les VLAN et ACL demandés. Le site ne peut pas être déclaré conforme ou réellement déployé avant validation du découpage `/24` et collecte des preuves sur les équipements.
