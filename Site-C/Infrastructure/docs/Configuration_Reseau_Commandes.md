# Guide de configuration - Site C

Ce guide accompagne `Dossier_reseau.md` et `Infrastructure/Switch L3.txt`. Il reprend le plan `/28` de Site C. Les exemples doivent être adaptés au matériel et testés en console.

## 1. Contrôles avant changement

```text
show version
show inventory
show interfaces status
show running-config
show startup-config
```

Sauvegarder la configuration avant la modification. Vérifier que le switch prend en charge le routage L3, les SVI, les ACL et le relais DHCP.

## 2. VLAN et passerelles

Le masque est `255.255.255.240` pour chaque VLAN. Les passerelles sont :

```text
VLAN 10  192.168.0.1
VLAN 20  192.168.0.17
VLAN 30  192.168.0.33
VLAN 40  192.168.0.49
VLAN 50  192.168.0.65
VLAN 60  192.168.0.81
VLAN 70  192.168.0.97
VLAN 80  192.168.0.113
VLAN 99  192.168.0.129
```

Le fichier `Switch L3.txt` contient les interfaces et les ACL complètes. Ne pas recopier une adresse `/24` du planning Site A.

## 3. Transit vers Routeur 1

Le transit historique `192.168.0.0/30` est incompatible avec le VLAN 10. La proposition utilisée dans les exemples est :

```text
interface GigabitEthernet1/0/24
 description TRANSIT_ROUTEUR1_PROPOSE
 no switchport
 ip address 192.168.254.2 255.255.255.252
 no shutdown
exit
ip route 0.0.0.0 0.0.0.0 192.168.254.1
```

Sur Routeur 1, ajouter les routes vers les blocs du plan via `192.168.254.2`, puis le NAT de sortie vers le WAN réel. L'adresse WAN et sa passerelle ne sont pas fournies dans les documents.

## 4. Routeur 2 et Proxmox 2

Le planning demande une liaison Routeur 2-SW-L3 et une seconde interface vers Proxmox 2. L'adaptation proposée est :

```text
Routeur 2, interface VLAN 30 : 192.168.0.46/28
Routeur 2, interface Proxmox 2 : 192.168.200.1/24
Proxmox 2 : 192.168.200.2/24, passerelle 192.168.200.1
```

Le switch doit utiliser la route suivante si le réseau applicatif doit être joignable depuis un réseau autorisé :

```text
ip route 192.168.200.0 255.255.255.0 192.168.0.46
```

Ne pas publier Routeur 2, Proxmox ou leur administration sur Internet. Les règles de filtrage doivent limiter la zone applicative au reverse proxy et aux flux d'administration autorisés.

## 5. Windows Server, DHCP et DNS

Proposition : Windows Server `192.168.0.34/28`, passerelle `192.168.0.33`. Créer une étendue par VLAN avec la passerelle de la ligne correspondante et le DNS `192.168.0.34`. Activer `ip helper-address 192.168.0.34` sur les SVI clientes.

Vérifications Windows :

```text
ipconfig /all
ipconfig /renew
nslookup domaine.local 192.168.0.34
```

Le domaine, les plages DHCP et les redirecteurs DNS doivent être confirmés avant déploiement.

## 6. Contrôles du switch

```text
show vlan brief
show interfaces status
show ip interface brief
show ip route
show ip interface Vlan30
show ip access-lists
ping 192.168.0.33
ping 192.168.254.1
copy running-config startup-config
```

Tester depuis un poste de chaque VLAN un flux autorisé et un flux interdit. Vérifier les compteurs ACL et les journaux de refus.

## 7. Retour arrière

Conserver la configuration précédente hors de l'équipement. En cas de perte d'accès après une ACL, utiliser la console, retirer l'ACL de l'interface concernée, rétablir les routes précédentes et refaire les tests avant toute nouvelle sauvegarde.
