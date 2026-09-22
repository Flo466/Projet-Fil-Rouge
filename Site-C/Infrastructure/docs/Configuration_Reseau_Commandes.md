# Guide de configuration - Site C / Site 2

Le bloc professeur est `172.16.64.0/18` (`255.255.192.0`). Les commandes utilisent le découpage de travail `/24` par VLAN décrit dans `Plan_adressage_Site_C.md`. Faire valider ce découpage avant application.

## 1. Sauvegarde et inventaire

```text
show version
show inventory
show interfaces status
show running-config
show startup-config
show vlan brief
```

Conserver les exports initiaux et vérifier les noms d'interfaces avant de coller la configuration.

## 2. Passerelles de travail

```text
VLAN 10  172.16.64.1/24
VLAN 20  172.16.65.1/24
VLAN 30  172.16.66.1/24
VLAN 40  172.16.67.1/24
VLAN 50  172.16.68.1/24
VLAN 60  172.16.69.1/24
VLAN 70  172.16.70.1/24
VLAN 80  172.16.71.1/24
VLAN 99  172.16.72.1/24
```

Le serveur AD/DNS/DHCP de travail est `172.16.66.10`. Les SVI clientes utilisent `ip helper-address 172.16.66.10`.

## 3. SW-L3 et transit

Le fichier `Infrastructure/Switch L3.txt` contient les noms de VLAN, les ports, les SVI, les ACL et le SSH. Le port 24 utilise le transit de travail suivant :

```text
interface GigabitEthernet1/0/24
 description TRANSIT_ROUTEUR1
 no switchport
 ip address 172.16.73.2 255.255.255.252
 no shutdown
exit
ip route 0.0.0.0 0.0.0.0 172.16.73.1
ip route 172.16.74.0 255.255.255.0 172.16.66.254
```

## 4. Routeur 2

Le fichier `Infrastructure/Routeur 2.txt` contient les interfaces, les routes, les ACL et le SSH :

```text
interface GigabitEthernet0/0
 description VERS_SW-L3_VLAN30
 ip address 172.16.66.254 255.255.255.0
 no shutdown
interface GigabitEthernet0/1
 description VERS_PROXMOX2_DMZ
 ip address 172.16.74.1 255.255.255.0
 no shutdown
ip route 0.0.0.0 0.0.0.0 172.16.66.1
```

Les flux Web passent par `172.16.74.10`. Proxmox 2 est `172.16.74.2`, Web 1 `.11` et Web 2 `.12` dans le plan de travail.

## 5. Contrôles et recette

```text
show ip interface brief
show ip route
show access-lists
show ip interface Vlan30
ping 172.16.66.1
ping 172.16.73.1
ping 172.16.74.2
copy running-config startup-config
```

Depuis un poste de chaque VLAN, tester un flux autorisé et un flux interdit. Vérifier les compteurs ACL, les journaux, les routes aller et retour, le DHCP, le DNS et le reverse proxy.

## 6. Retour arrière

En cas de perte d'accès après une ACL, utiliser la console, retirer l'ACL de l'interface concernée, restaurer la configuration sauvegardée et refaire la recette. Ne pas remplacer un refus par une autorisation globale permanente.
