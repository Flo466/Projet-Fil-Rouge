# Configuration réseau et vérifications

Projet Fil Rouge - mise à jour du 18 septembre 2026

Ce guide accompagne `Dossier_reseau.md` et le schéma `schéma réseau.pdf` de la branche `yanis`, commit `2276171`. Il décrit la configuration cible, les exemples de commandes et la recette de la nouvelle architecture. Les paramètres proposés complètent le schéma ; aucune commande n’a été exécutée sur les équipements pour cette mise à jour documentaire.

## 1 Préparer la mise en service

Sauvegarder R1, FW1, SW1 et les hyperviseurs. Garder un accès console pendant les changements. Relever les modèles et versions, le nom réel des interfaces, les paramètres WAN, le domaine AD, les certificats, les résolveurs et les sources NTP autorisés. Vérifier la disponibilité du routage L3, des SVI, du port routé, du relais DHCP et des ACL sur le Cisco.

Les commandes SW1 sont des exemples IOS avec GigabitEthernet1/0/1 à 24. Adapter les noms après inventaire ; elles ne constituent pas une configuration constructeur validée pour un modèle inconnu. Pour le TP-Link et le Hillstone, les tableaux donnent les paramètres exacts à saisir dans leur interface d’administration. Une syntaxe IOS ne doit pas être utilisée comme syntaxe TP-Link.

Convention proposée : FW1 e0/3 = `10.0.20.254/24`, car le schéma ne donne pas l’adresse de cette interface. Les adresses des VM sont en revanche fixées par le schéma : serveurs internes `192.168.50.11` à `.14` et serveurs DMZ `10.0.20.2` à `.6`. Le Wi-Fi utilise uniquement DNS, DHCP et l’accès Internet prévu. Le VLAN 99 est réservé avec SW1 `192.168.99.10` ; aucune interface opérationnelle ni route vers ce VLAN n’est créée.

## 2 Réseaux et raccordements

| Zone | Réseau et préfixe | Passerelle ou extrémités | Ports SW1 |
| --- | --- | --- | --- |
| VLAN 10 Direction | 192.168.10.0/24 | 192.168.10.254 | 1 à 4 |
| VLAN 20 Comptabilité | 192.168.20.0/24 | 192.168.20.254 | 5 à 9 |
| VLAN 30 Wi-Fi | 192.168.30.0/24 | 192.168.30.254 | 10 à 14 |
| VLAN 40 Administration | 192.168.40.0/24 | 192.168.40.254 | 15 à 18 |
| VLAN 50 Serveurs | 192.168.50.0/24 | 192.168.50.254 | 19 à 23 |
| Réseau amont / NAT Internet | 172.16.50.0/24 | R1 port 1 ; IP et passerelle à relever | Sans objet |
| Transit R1 vers FW1 | 10.0.0.248/29 | R1 .254 ; FW1 .253 | Sans objet |
| Transit SW1 vers FW1 | 10.0.10.248/29 | SW1 .253 ; FW1 .254 | 24 routé |
| DMZ | 10.0.20.0/24 | FW1 10.0.20.254 proposée | Sans objet |
| VLAN 99 Gestion réservé | 192.168.99.0/24 | SW1 .10 sur le schéma ; transport absent | Aucun |
| Gestion locale R1 | 192.168.0.0/24 | R1 port 5 : 192.168.0.1 | Aucun |
| Gestion locale FW1 | 192.168.1.0/24 | FW1 e0/0 : 192.168.1.1 | Aucun |

| Câble | Extrémité A | Extrémité B | Usage |
| --- | --- | --- | --- |
| C01 | R1 TP-Link<br>Port 4 | FW1 Hillstone<br>e0/1 | Transit 10.0.0.248/29 |
| C02 | Réseau amont / accès Internet | R1 TP-Link<br>Port 1 | WAN/NAT 172.16.50.0/24 |
| C03 | FW1 Hillstone<br>e0/2 | SW1 Cisco<br>Port 24 | Transit 10.0.10.248/29 |
| C04 | FW1 Hillstone<br>e0/3 | SRV1 ProLiant<br>Carte Ethernet reliée | DMZ 10.0.20.0/24 |
| C05 | SW1 Cisco<br>Port 1 | PC01 Dell<br>Interface Ethernet | Accès VLAN 10 |
| C06 | SW1 Cisco<br>Port 5 | PC02 Dell<br>Interface Ethernet | Accès VLAN 20 |
| C07 | SW1 Cisco<br>Port 15 | PC03 Dell<br>Interface Ethernet | Accès VLAN 40 |
| C08 | SW1 Cisco<br>Port 10 | AP1 Netis<br>Port LAN | Accès VLAN 30 |
| C09 | SW1 Cisco<br>Port 23 | PC04 Dell Proxmox<br>Carte Ethernet reliée | Accès VLAN 50 |

Les neuf câbles sont utilisés ; C02 est affecté au WAN de R1. SW2 demeure dans l’inventaire mais sort de la topologie active. Les deux transits /29 ont pour masque 255.255.255.248 : réseau .248, hôtes .249 à .254, diffusion .255. La DMZ et le réseau amont utilisent 255.255.255.0.

## 3 Configurer SW1

### Contrôler le matériel et sauvegarder

```text
show version
show inventory
show interfaces status
show running-config
show startup-config
```

Exporter les configurations avant toute modification. L’exemple suivant configure les VLAN 10 à 50 et désactive les ports actuellement libres. Il fournit le routage de base ; les ACL doivent être ajoutées ensuite selon la matrice de la section 7. Les ports 1, 5, 10, 15, 23 et 24 restent actifs.

### Créer les VLAN et le routage

```text
enable
configure terminal
hostname SW1
no ip domain-lookup
ip routing

vlan 10
 name DIRECTION
exit
interface range GigabitEthernet1/0/1 - 4
 description ACCES-DIRECTION
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 no shutdown
exit
interface Vlan10
 ip address 192.168.10.254 255.255.255.0
 no shutdown
exit

vlan 20
 name COMPTABILITE
exit
interface range GigabitEthernet1/0/5 - 9
 description ACCES-COMPTABILITE
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast
 no shutdown
exit
interface Vlan20
 ip address 192.168.20.254 255.255.255.0
 no shutdown
exit

vlan 30
 name WIFI
exit
interface range GigabitEthernet1/0/10 - 14
 description ACCES-WIFI
 switchport mode access
 switchport access vlan 30
 spanning-tree portfast
 no shutdown
exit
interface Vlan30
 ip address 192.168.30.254 255.255.255.0
 ip helper-address 192.168.50.11
 no shutdown
exit

vlan 40
 name ADMINISTRATION
exit
interface range GigabitEthernet1/0/15 - 18
 description ACCES-ADMINISTRATION
 switchport mode access
 switchport access vlan 40
 spanning-tree portfast
 no shutdown
exit
interface Vlan40
 ip address 192.168.40.254 255.255.255.0
 no shutdown
exit

vlan 50
 name SERVEURS
exit
interface range GigabitEthernet1/0/19 - 23
 description ACCES-SERVEURS
 switchport mode access
 switchport access vlan 50
 spanning-tree portfast
 no shutdown
exit
interface Vlan50
 ip address 192.168.50.254 255.255.255.0
 no shutdown
exit

interface GigabitEthernet1/0/24
 description TRANSIT-FW1-E0-2
 no switchport
 ip address 10.0.10.253 255.255.255.248
 no shutdown
exit

ip route 0.0.0.0 0.0.0.0 10.0.10.254

interface range GigabitEthernet1/0/2 - 4
 description RESERVE-NON-RACCORDEE
 shutdown
exit

interface range GigabitEthernet1/0/6 - 9
 description RESERVE-NON-RACCORDEE
 shutdown
exit

interface range GigabitEthernet1/0/11 - 14
 description RESERVE-NON-RACCORDEE
 shutdown
exit

interface range GigabitEthernet1/0/16 - 18
 description RESERVE-NON-RACCORDEE
 shutdown
exit

interface range GigabitEthernet1/0/19 - 22
 description RESERVE-NON-RACCORDEE
 shutdown
exit
end
```

Ne pas activer de SVI VLAN 99 sans raccordement défini. Le port 24 est routé et les ports 10 et 23 sont en accès : aucun de ces liens ne transporte de trunk 802.1Q. Les VM de PC04 utilisent le VLAN 50 non étiqueté.

### Vérifier puis sauvegarder après la recette

```text
show vlan brief
show ip interface brief
show ip route
show interfaces GigabitEthernet1/0/24
show ip interface Vlan30
ping 10.0.10.254
```

Une SVI peut rester inactive si aucun port du VLAN n’est actif. Vérifier les ACL et leurs compteurs avant la sauvegarde finale :

```text
show ip access-lists
copy running-config startup-config
```

## 4 Configurer FW1 Hillstone

Créer trois zones de sécurité distinctes et affecter chaque interface en mode routé. Vérifier les libellés réels e0/1, e0/2 et e0/3 dans StoneOS.

| Repère | Interface et fonction | Adresse et préfixe |
| --- | --- | --- |
| FW1 | e0/1 vers R1 ; zone AMONT | 10.0.0.253/29 |
| FW1 | e0/2 vers SW1 ; zone LAN | 10.0.10.254/29 |
| FW1 | e0/3 vers SRV1 ; zone DMZ | 10.0.20.254/24 proposée |

Créer les cinq routes internes via 10.0.10.253 et la route par défaut via 10.0.0.254. Les trois réseaux connectés n’ont pas besoin de route statique.

| Équipement | Destination | Prochain saut |
| --- | --- | --- |
| FW1 | 192.168.10.0/24 ; 192.168.20.0/24<br>192.168.30.0/24 ; 192.168.40.0/24<br>192.168.50.0/24 | 10.0.10.253 |
| FW1 | 0.0.0.0/0 | 10.0.0.254 |

Dans les objets d’adresses, créer les cinq réseaux LAN, PC03, les quatre VM internes `.11` à `.14`, SRV1, les cinq VM DMZ `.2` à `.6`, R1 et les groupes de résolveurs et NTP approuvés. Dans les objets de services, saisir les ports de la section 7. Appliquer les règles de sécurité dans l’ordre indiqué. Les noms des menus varient avec la version StoneOS ; le modèle et la version doivent être relevés avant de convertir ces paramètres en commandes CLI.

Le dernier schéma ajoute e0/0 = 192.168.1.1/24 pour la gestion dédiée de FW1. Cette interface reste isolée des trois zones de données et ne doit pas servir au transit. Autoriser l’accès local depuis le poste temporaire 192.168.1.10 ; le rôle exact de l’interface de gestion dépend du modèle. L’accès complémentaire depuis PC03 192.168.40.10 sur e0/2 doit être activé séparément si retenu. Tester HTTPS ou SSH avant de désactiver un ancien mode d’administration. Les règles de transit LAN vers DMZ ne suffisent pas à protéger le pare-feu lui-même.

## 5 Configurer R1 et le NAT

Sur le TP-Link, configurer le port 4 avec `10.0.0.254/29`. Vérifier que le réseau /29 peut être affecté à ce port ou à son groupe LAN et qu’aucun autre port ou Wi-Fi non prévu ne permet de rejoindre le transit. Configurer le port 1 sur le réseau amont `172.16.50.0/24` ; son adresse, son mode d’attribution et sa passerelle ne sont pas indiqués sur le schéma et doivent être relevés.

Le port 5 de R1 porte `192.168.0.1/24` pour la gestion locale. Le maintenir distinct des ports 4 et 1. La procédure de maintenance de la section 9 utilise une liaison directe ; aucune route vers `192.168.0.0/24` n’est diffusée dans le LAN.

| Destination | Masque | Prochain saut |
| --- | --- | --- |
| 192.168.10.0 | 255.255.255.0 | 10.0.0.253 |
| 192.168.20.0 | 255.255.255.0 | 10.0.0.253 |
| 192.168.30.0 | 255.255.255.0 | 10.0.0.253 |
| 192.168.40.0 | 255.255.255.0 | 10.0.0.253 |
| 192.168.50.0 | 255.255.255.0 | 10.0.0.253 |
| 10.0.10.248 | 255.255.255.248 | 10.0.0.253 |
| 10.0.20.0 | 255.255.255.0 | 10.0.0.253 |

Mode de référence : R1 effectue sur le port 1 le NAT de sortie vers `172.16.50.0/24` pour les cinq VLAN et la DMZ ; FW1 laisse leurs adresses sources inchangées. Vérifier explicitement que le modèle TP-Link traduit les réseaux atteints par des routes statiques. Si cette fonction n’est pas disponible, le repli consiste à faire un SNAT sur FW1 en sortie e0/1 vers `10.0.0.253`, puis le NAT WAN de R1. Appliquer le SNAT uniquement aux destinations Internet et conserver une exemption pour les accès d’administration à R1. Documenter le mode choisi ; le double NAT peut limiter certains usages.

Ne pas traduire les flux LAN vers DMZ. Ne pas activer d’administration WAN, d’UPnP ou de publication globale. Une publication Web future nécessite deux DNAT TCP 80/443 : port 1 de R1 vers `10.0.0.253`, puis FW1 vers le reverse proxy `10.0.20.3`, avec une règle AMONT vers DMZ correspondante. Ne jamais publier directement Web1-Web3. Cette publication reste inactive et dépend de l’adresse amont et de l’absence de blocage supplémentaire.

## 6 Configurer les hyperviseurs et services

| Hôte | Adresse et préfixe | Passerelle | Affectation |
| --- | --- | --- | --- |
| PC01 Dell | 192.168.10.10/24 | 192.168.10.254 | Direction |
| PC02 Dell | 192.168.20.10/24 | 192.168.20.254 | Comptabilité |
| PC03 Dell | 192.168.40.10/24 | 192.168.40.254 | Administration |
| PC04 Dell Proxmox | 192.168.50.10/24 | 192.168.50.254 | Hyperviseur interne |
| AP1 Netis | 192.168.30.2/24 | 192.168.30.254 | Point d’accès en mode pont |
| SRV1 ProLiant Proxmox | 10.0.20.1/24 | 10.0.20.254 | Hyperviseur DMZ |

| VM ou rôle du schéma | Hébergement et services | IP fixe et passerelle |
| --- | --- | --- |
| Windows Server interne | PC04 ; AD DS, DNS interne, DHCP et GLPI | 192.168.50.11/24 ; GW 192.168.50.254 |
| Base de données Debian | PC04 ; moteur de base à confirmer | 192.168.50.12/24 ; GW 192.168.50.254 |
| Monitoring Zabbix | PC04 ; serveur de supervision | 192.168.50.13/24 ; GW 192.168.50.254 |
| Proxy Squid | PC04 ; mode et port à confirmer | 192.168.50.14/24 ; GW 192.168.50.254 |
| Windows Server DNS DMZ | SRV1 ; DNS de DMZ et redirecteur du DNS interne | 10.0.20.2/24 ; GW 10.0.20.254 |
| Reverse proxy | SRV1 ; terminaison et distribution HTTP/HTTPS | 10.0.20.3/24 ; GW 10.0.20.254 |
| Web1 | SRV1 ; serveur Web | 10.0.20.4/24 ; GW 10.0.20.254 |
| Web2 | SRV1 ; serveur Web | 10.0.20.5/24 ; GW 10.0.20.254 |
| Web3 | SRV1 ; serveur Web | 10.0.20.6/24 ; GW 10.0.20.254 |

### Ponts Proxmox

Sur PC04 et SRV1, connecter la carte physique à vmbr0 sans étiquette VLAN. Configurer l’adresse de gestion sur le pont et pas simultanément sur la carte physique. Le nom eno1 ci-dessous est un exemple à remplacer par la carte réellement raccordée ; effectuer le changement depuis la console.

Exemple PC04 dans /etc/network/interfaces :

```text
auto lo
iface lo inet loopback

iface eno1 inet manual

auto vmbr0
iface vmbr0 inet static
    address 192.168.50.10/24
    gateway 192.168.50.254
    bridge-ports eno1
    bridge-stp off
    bridge-fd 0
```

Sur SRV1, utiliser la même structure avec address 10.0.20.1/24 et gateway 10.0.20.254. Raccorder les interfaces des VM à vmbr0, puis configurer leurs IP, passerelles et DNS dans chaque système invité. Les routes de l’hyperviseur ne sont pas héritées par les VM. La DMZ ne nécessite aucune route directe vers R1 ni vers 10.0.0.253.

```text
ip -br address
ip route
bridge link
```

Le pare-feu de Proxmox ou des VM doit également protéger les échanges à l’intérieur du VLAN 50 et de la DMZ, qui restent locaux au pont. Réserver l’administration Proxmox TCP 8006 et SSH TCP 22 à PC03.

### DNS et services applicatifs

Le serveur Windows interne `192.168.50.11` porte AD DS, le DNS interne, DHCP et GLPI. Définir le domaine AD lors de l’installation et créer les enregistrements des services internes dans ce DNS. PC01, PC02 et PC03 utilisent `192.168.50.11`. Le DNS interne redirige les noms externes vers `10.0.20.2` ; le DNS de DMZ utilise les résolveurs externes approuvés. Les autres hôtes DMZ utilisent `10.0.20.2`, sans accès direct au DNS AD.

Limiter la récursion du DNS `10.0.20.2` au serveur Windows interne et aux hôtes DMZ inventoriés. Configurer GLPI sur `192.168.50.11` et n’autoriser son accès à la base Debian `192.168.50.12` que sur le port du moteur retenu. Configurer Zabbix `192.168.50.13` et ses agents avec les seuls ports nécessaires. Décider si Squid `192.168.50.14` est explicite ou transparent, fixer son port et empêcher le contournement seulement si la politique impose le proxy. Le reverse proxy `10.0.20.3` distribue HTTP/HTTPS vers Web1 `.4`, Web2 `.5` et Web3 `.6`. Ces derniers flux restent locaux au pont DMZ et doivent être filtrés par Proxmox ou les pare-feu des VM. Configurer les certificats, noms et contrôles d’intégrité avant la recette applicative.

### DHCP du Wi-Fi

| Paramètre | Valeur |
| --- | --- |
| Réseau et plage | 192.168.30.0/24 ; 192.168.30.100 à 192.168.30.199 |
| Masque et bail proposé | 255.255.255.0 ; 8 heures |
| Option 003 Routeur | 192.168.30.254 |
| Option 006 DNS | 192.168.50.11 |
| Serveur | Windows Server interne 192.168.50.11 ; rôle DHCP autorisé dans AD |
| Relais sur SW1 | SVI VLAN 30 ; `ip helper-address 192.168.50.11` |
| Adresses hors plage | AP1 192.168.30.2 et passerelle .254 ; pas de réservation nécessaire |

Sur le serveur Windows interne, installer le rôle DHCP, l’autoriser dans Active Directory, créer puis activer l’étendue VLAN30. Le suffixe DNS éventuel dépend du domaine choisi. AP1 reste en IP fixe et son serveur DHCP doit être désactivé ; utiliser son port LAN et le mode pont.

Exemple PowerShell, à utiliser seulement après installation et autorisation du rôle, si l’étendue n’existe pas déjà :

```powershell
Add-DhcpServerv4Scope -Name "VLAN30-WIFI" `
  -StartRange 192.168.30.100 -EndRange 192.168.30.199 `
  -SubnetMask 255.255.255.0 -LeaseDuration 0.08:00:00 `
  -State Active
Set-DhcpServerv4OptionValue -ScopeId 192.168.30.0 `
  -Router 192.168.30.254 -DnsServer 192.168.50.11
Get-DhcpServerv4Scope
Get-DhcpServerv4OptionValue -ScopeId 192.168.30.0
Get-DhcpServerv4Lease -ScopeId 192.168.30.0
```

L’ACL de VLAN 30 doit autoriser la demande DHCP initiale depuis 0.0.0.0:68 vers 255.255.255.255:67, les nouvelles diffusions du /24 et le renouvellement unicast vers `192.168.50.11`. L’ACL de VLAN 50 doit laisser revenir le serveur Windows UDP 67 vers le relais `192.168.30.254` UDP 67 et vers les clients VLAN 30 UDP 68. Le relais sélectionne l’étendue grâce à son adresse `192.168.30.254`.

## 7 Appliquer le filtrage

La première règle correspondante est appliquée. Les autorisations précises précèdent les refus de réseaux privés ; le refus général vient en dernier. Les échanges entre VLAN sont filtrés sur SW1, les échanges LAN, DMZ et amont sur FW1. Une communication entre deux hôtes du même VLAN nécessite un contrôle local sur les hôtes ou AP1.

| Groupe | Protocoles et ports de destination |
| --- | --- |
| DNS | UDP et TCP 53 |
| AD_CLIENT | TCP 88, 135, 389, 445, 464, 3268, 49152 à 65535 ; UDP 88, 123, 389, 464 ; DNS ; ICMP vers le serveur Windows interne |
| WEB | TCP 80 et 443 ; GLPI utilise TCP 443 |
| ADMIN | TCP 22, 443 et 8006 pour les hyperviseurs et équipements selon service ; TCP 3389, 5986 et 9389 vers le serveur Windows ; ICMP de diagnostic |
| DHCP | Client UDP 68 vers serveur UDP 67 ; relais UDP 67 vers serveur UDP 67 ; réponses en sens inverse |
| BASE | Port du moteur à confirmer, par exemple TCP 3306 pour MariaDB/MySQL |
| ZABBIX | TCP 10050 vers les agents ; TCP 10051 vers le serveur/proxy, à confirmer |
| SQUID | Port à confirmer, couramment TCP 3128 en proxy explicite |
| NTP | UDP 123 ; clients du domaine vers le serveur Windows interne |

AD_CLIENT vise les postes membres d’un domaine Windows récent. N’ajouter LDAPS TCP 636/3269 que si utilisé. La plage RPC et les besoins entre contrôleurs doivent être ajustés à la version Windows et aux rôles réellement déployés.

### Politique sur SW1

| Ordre | Source | Destination | Service et action |
| --- | --- | --- | --- |
| 10 | Clients Wi-Fi et relais SW1 | Windows interne et diffusion DHCP | Autoriser DHCP vers 192.168.50.11, y compris attribution initiale et renouvellement |
| 20 | VLAN 10, 20, 30 et PC03 | Windows interne 192.168.50.11 | Autoriser DNS ; Wi-Fi limité à ce service interne |
| 30 | VLAN 10, 20 et PC03 | Windows interne 192.168.50.11 | Autoriser AD_CLIENT |
| 40 | VLAN 10, 20 et PC03 | GLPI sur 192.168.50.11 | Autoriser HTTPS TCP 443 |
| 45 | VLAN autorisés | Squid 192.168.50.14 | Autoriser le port du proxy si le mode explicite est retenu |
| 50 | PC03 192.168.40.10 | Équipements, hyperviseurs et VM | Autoriser ADMIN aux seules adresses inventoriées |
| 55 | Zabbix 192.168.50.13 | Hôtes supervisés des VLAN 10, 20, 30 et 40 | Autoriser ZABBIX uniquement vers les agents inventoriés |
| 60 | VLAN 10, 20 et PC03 | Reverse proxy 10.0.20.3 | Autoriser WEB ; décision DMZ finale sur FW1 |
| 70 | Windows interne 192.168.50.11 | DNS DMZ 10.0.20.2 | Autoriser DNS ; redirection des noms externes |
| 80 | Serveurs et postes administrés | Clients autorisés et PC03 | Autoriser les retours des flux précédents selon protocole |
| 90 | Hôtes de chaque VLAN | Leur propre passerelle | Autoriser ICMP de diagnostic |
| 100 | Chaque VLAN | Autres réseaux privés | Refuser les autres échanges ; journaliser |
| 110 | Hôtes explicitement autorisés, dont Squid si utilisé | Internet via FW1 | Autoriser les services nécessaires ; limiter la sortie directe si Squid devient obligatoire |
| 999 | Toute source | Toute destination | Refuser et journaliser le reste |

Appliquer les ACL en entrée des SVI 10, 20, 30, 40 et 50 après traduction de cette matrice dans la syntaxe du modèle. Une ACL IOS statique ne suit pas les sessions. Écrire les autorisations de retour pour chaque flux : réponses DNS UDP/TCP 53, réponses AD et NTP, DHCP relayé ou unicast, TCP ACK/RST vers le client et réponses ou erreurs ICMP nécessaires. Le mot-clé established vérifie ACK/RST et ne fournit pas une protection équivalente à celle de FW1. L’exemple ci-dessous couvre VLAN 30 ; il ne remplace pas les quatre autres ACL ni les règles locales des équipements.

Les flux entre les VM internes `.11` à `.14` restent dans le VLAN 50 et ne passent pas par ces ACL. Autoriser localement uniquement le serveur Windows `.11` vers la base `.12` sur le port retenu, Zabbix `.13` vers les agents inventoriés et les clients autorisés vers Squid `.14`. De même, les flux du reverse proxy `.3` vers Web1-Web3 `.4` à `.6` restent sur le pont DMZ et doivent être limités sur Proxmox ou les pare-feu des VM.

### Exemple IOS pour le VLAN 30 isolé

Cet exemple autorise les retours d’administration d’AP1 vers PC03. Les réponses DNS et DHCP arrivent par VLAN 50 et doivent aussi être autorisées par son ACL. Les réponses Web arrivent par FW1. La règle de refus des réseaux privés doit rester avant les deux règles Web Internet. Le trafic HTTPS utilise TCP ; QUIC UDP 443 n’est pas autorisé dans ce profil.

```text
configure terminal
ip access-list extended WIFI_IN
 10 remark DHCP initial et renouvellement
 20 permit udp host 0.0.0.0 eq 68 host 255.255.255.255 eq 67
 30 permit udp 192.168.30.0 0.0.0.255 eq 68 host 255.255.255.255 eq 67
 40 permit udp 192.168.30.0 0.0.0.255 eq 68 host 192.168.50.11 eq 67
 50 remark DNS interne
 60 permit udp 192.168.30.0 0.0.0.255 host 192.168.50.11 eq 53
 70 permit tcp 192.168.30.0 0.0.0.255 host 192.168.50.11 eq 53
 80 remark Diagnostic passerelle et retours AP1 vers PC03
 90 permit icmp 192.168.30.0 0.0.0.255 host 192.168.30.254 echo
 100 permit tcp host 192.168.30.2 host 192.168.40.10 established
 110 permit icmp host 192.168.30.2 host 192.168.40.10 echo-reply
 120 remark Refus des autres destinations privees
 130 deny ip 192.168.30.0 0.0.0.255 10.0.0.0 0.255.255.255 log
 140 deny ip 192.168.30.0 0.0.0.255 172.16.0.0 0.15.255.255 log
 150 deny ip 192.168.30.0 0.0.0.255 192.168.0.0 0.0.255.255 log
 160 remark Web Internet
 170 permit tcp 192.168.30.0 0.0.0.255 any eq 80
 180 permit tcp 192.168.30.0 0.0.0.255 any eq 443
 999 deny ip any any log
exit
interface Vlan30
 ip access-group WIFI_IN in
exit
end
```

### Politique sur FW1

Le groupe Internet exclut les réseaux privés 10.0.0.0/8, 172.16.0.0/12 et 192.168.0.0/16. Les objets de résolveurs et NTP contiennent les adresses approuvées lors de la préparation. Les retours sont traités par le suivi de session du pare-feu ; ils n’autorisent pas de nouvelles sessions depuis la DMZ.

| Ordre | Zone source et hôtes | Zone destination et hôtes | Service et action |
| --- | --- | --- | --- |
| 10 | Sessions déjà autorisées | Sens retour | Accepter les retours par suivi de session ; traiter les erreurs ICMP associées |
| 20 | LAN ; PC03 | DMZ ; SRV1 et VM 10.0.20.2 à .6 | Autoriser ADMIN selon le service de chaque hôte |
| 30 | LAN ; VLAN 10, 20 et PC03 | DMZ ; reverse proxy 10.0.20.3 | Autoriser TCP 80 et 443 |
| 40 | LAN ; Windows interne 192.168.50.11 | DMZ ; DNS 10.0.20.2 | Autoriser UDP et TCP 53 |
| 50 | DMZ ; toute source | LAN ; tous les VLAN | Refuser toute nouvelle session ; journaliser |
| 60 | LAN ; PC03 | AMONT ; R1 10.0.0.254 | Autoriser HTTPS ou SSH si disponible, et ICMP |
| 70 | LAN et DMZ ; toute autre source | AMONT ; réseaux privés | Refuser ; empêcher les contournements par une règle Internet large |
| 80 | LAN ; hôtes autorisés par SW1 | AMONT ; Internet | Autoriser TCP 80 et 443 |
| 90 | DMZ ; SRV1 et VM 10.0.20.2 à .6 | AMONT ; Internet | Autoriser TCP 80 et 443 pour mises à jour |
| 100 | DMZ ; DNS 10.0.20.2 | AMONT ; résolveurs externes approuvés | Autoriser UDP et TCP 53 uniquement |
| 110 | LAN ; serveurs autorisés ; DMZ ; SRV1 et VM .2 à .6 | AMONT ; serveurs NTP approuvés | Autoriser UDP 123 |
| 999 | Toutes zones | Toutes destinations | Refuser et journaliser ; aucune publication WAN active |

### Politique sur R1

| Ordre | Source | Destination | Service et action |
| --- | --- | --- | --- |
| 10 | Sessions sortantes autorisées | Sens retour | Accepter par suivi de session |
| 20 | PC03 192.168.40.10 | R1 10.0.0.254 | Autoriser administration HTTPS ou SSH si disponible et ICMP |
| 25 | PC03 en maintenance 192.168.0.10 | R1 port 5 ; 192.168.0.1 | Autoriser administration locale ; aucun routage vers les autres zones |
| 30 | LAN et DMZ via FW1 ; ou FW1 .253 en mode double NAT | Port 1 / réseau 172.16.50.0/24 | Autoriser les flux sortants déjà filtrés par FW1 et effectuer le NAT WAN |
| 40 | Port 1 / réseau amont | Réseaux internes, DMZ et transit | Refuser toute nouvelle connexion ; journaliser |
| 999 | Toute autre source | Administration de R1 | Refuser ; désactiver administration WAN et ouvertures automatiques UPnP |

Le profil présenté concerne IPv4. Si IPv6 est utilisé, documenter son adressage et son filtrage avant mise en service ; les ACL IPv4 ne filtrent pas les paquets IPv6. Ne pas désactiver arbitrairement IPv6 sur Windows pour masquer un manque de règles.

## 8 Effectuer la recette

Les résultats ci-dessous sont attendus, sans exécution sur le réseau à ce stade. Pour chaque test, enregistrer source, date, preuve et résultat réel. Vérifier un refus par les compteurs ou journaux en plus du résultat client.

| Contrôle | Vérification | Résultat attendu |
| --- | --- | --- |
| Interfaces et câbles | Comparer ports, VLAN, masques et voisins aux tableaux | 9 liens actifs ; C02 sur R1 port 1 ; pas de SW2 en transit |
| Liaisons routées | SW1 vers 10.0.10.254 ; FW1 vers 10.0.0.254 et 10.0.20.1 | Voisins joignables avec diagnostics autorisés |
| Routage retour | Vérifier les routes de R1 et FW1 ; tracer PC03 vers SRV1 | Passage SW1 puis FW1 ; pas de retour direct SRV1 vers R1 |
| DHCP Wi-Fi | Libérer puis renouveler le bail sur un client VLAN 30 | IP .100 à .199 ; masque /24 ; GW .254 ; DNS 192.168.50.11 |
| DNS | Résoudre les noms internes puis un nom Internet via 192.168.50.11 | DNS interne joignable ; noms externes transmis à 10.0.20.2 |
| Domaine | Joindre un poste VLAN 10 puis VLAN 20 ; ouvrir une session et appliquer une GPO | DNS, Kerberos, LDAP, SMB et RPC fonctionnent |
| Applications | Depuis PC01 et PC02, ouvrir GLPI sur 192.168.50.11 et le Web via 10.0.20.3 | Services accessibles ; certificats et noms cohérents ; trafic distribué à Web1-Web3 |
| Base de données | Depuis le serveur Windows .11, joindre la base Debian .12 sur le port retenu ; répéter depuis un client | Flux applicatif autorisé ; client direct refusé |
| Supervision | Vérifier les agents autorisés depuis Zabbix .13 et les tableaux de bord | Hôtes inventoriés remontés ; ports limités aux besoins Zabbix |
| Proxy | Tester un client configuré vers Squid .14 puis un contournement direct | Navigation conforme au mode retenu ; contournement refusé si le proxy est obligatoire |
| Administration | PC03 vers Proxmox TCP 8006 et équipements ; répéter depuis PC01 | PC03 autorisé ; PC01 refusé pour administration |
| Gestion locale | PC03 branché successivement à R1 port 5 puis FW1 e0/0 | Accès à 192.168.0.1 puis 192.168.1.1 avec IP locale adaptée ; retour au VLAN 40 vérifié |
| Isolation Wi-Fi | VLAN 30 vers PC01, GLPI, Proxmox et le reverse proxy ; puis DNS et Internet | Accès privés refusés hors DNS, DHCP et services explicitement retenus |
| Isolation DMZ | Web1 10.0.20.4 vers le serveur Windows .11 TCP 445 et PC03 TCP 3389 | Nouvelles connexions refusées par FW1 et journalisées |
| Internet et NAT | Accès HTTPS depuis un poste LAN et une VM DMZ ; observer R1 port 1 et la traduction | Sortie via 172.16.50.0/24 et retours valides ; pas de NAT LAN vers DMZ |
| Persistance | Sauvegarder, redémarrer selon fenêtre de maintenance, refaire les tests essentiels | Configuration conservée ; résultats datés dans le compte rendu de recette |

Exemples de contrôles depuis les postes Windows, selon le VLAN :

```powershell
ipconfig /all
route print -4
ping 192.168.40.254
tracert -d 10.0.20.1
Resolve-DnsName -Name www.microsoft.com -Server 192.168.50.11
Test-NetConnection 192.168.50.11 -Port 443
Test-NetConnection 10.0.20.3 -Port 443
Test-NetConnection 10.0.20.1 -Port 8006
```

Le ping de 192.168.40.254 et l’administration de SRV1 se testent depuis PC03. Une trace peut être partielle si les réponses ICMP sont filtrées ; utiliser aussi la table de routage et les journaux FW1. Depuis un client Wi-Fi, renouveler le bail :

```text
ipconfig /release
ipconfig /renew
ipconfig /all
```

Depuis une VM DMZ Linux, tenter une nouvelle connexion TCP vers le serveur Windows interne puis vérifier le refus dans FW1 :

```text
nc -vz -w 3 192.168.50.11 445
ip route
```

L’outil nc doit être disponible. Un échec seul n’établit pas que le pare-feu a bloqué le flux ; corréler avec la règle et le journal. Tester aussi une session autorisée, son retour et sa fermeture pour confirmer la différence entre nouvelle session et trafic de réponse.

## 9 Sauvegarder et revenir en arrière

Pour une maintenance locale dédiée, débrancher PC03 de SW1 port 15. Le raccorder au port 5 de R1 et utiliser temporairement `192.168.0.10/24` sans passerelle pour joindre `192.168.0.1` ; pour FW1, le raccorder à e0/0 et utiliser `192.168.1.10/24` sans passerelle pour joindre `192.168.1.1`. Vérifier l’absence de conflit d’adresse. C02 étant affecté au WAN, réutiliser temporairement C07 ou prévoir un câble supplémentaire. Ces accès sont successifs et ne créent aucun pont entre réseaux.

Après intervention, rétablir C07 vers SW1 port 15 puis `192.168.40.10/24`, passerelle `192.168.40.254` et DNS `192.168.50.11` sur PC03. Un accès permanent simultané aux réseaux de gestion demanderait un raccordement supplémentaire, absent du schéma.

Après réussite de la recette, sauvegarder SW1 avec copy running-config startup-config et exporter les configurations de FW1 et R1. Sauvegarder les VM et tester une restauration sur un environnement isolé. Conserver les résultats de recette et le mode NAT choisi avec les versions du matériel.

Si WIFI_IN bloque la mise en service, revenir par console et retirer uniquement son attachement avant d’analyser ses compteurs :

```text
configure terminal
interface Vlan30
 no ip access-group WIFI_IN in
exit
end
```

Le retrait rétablit un routage plus permissif : maintenir le réseau en maintenance jusqu’à correction. Pour un retour complet, restaurer les exports précédents et le câblage correspondant. Ne pas redémarrer un équipement à distance sans accès de secours.

## 10 Références

Schéma de référence : `schéma réseau.pdf`, branche `yanis`, commit `2276171` du 18 septembre 2026.

- [Cisco ACL](https://www.cisco.com/c/en/us/support/docs/ip/access-lists/26448-ACLsamples.html)
- [Cisco relais DHCP](https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/ipaddr_dhcp/configuration/xe-16-11/dhcp-xe-16-11-book/dhcp-relay-agent-xe.html)
- [Microsoft AD](https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/config-firewall-for-ad-domains-and-trusts)
- [Proxmox réseau](https://pve.proxmox.com/wiki/Network_Configuration)
- [Hillstone StoneOS](https://kb.hillstonenet.com/en/wp-content/uploads/2020/10/StoneOS-Cookbook-V9.pdf)
- [Microsoft DHCP PowerShell](https://learn.microsoft.com/en-us/powershell/module/dhcpserver/add-dhcpserverv4scope)
