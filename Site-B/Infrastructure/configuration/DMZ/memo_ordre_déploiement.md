| # | Étape | Dépendance |
|---|---|---|
| 0 | Réseau Proxmox, ponts C04 et C09, portable joignable | — |
| 1 | Windows Server DNS DMZ en 10.0.20.2| l'hôte ProLiant |
| 2 | web01 en 10.0.20.4 | le DNS, pour les mises à jour |
| 3 | Clones web02 et web03 | web01 |
| 4 | Ansible sur les trois fronts | SSH + DNS |
| 5 | Reverse proxy en 10.0.20.3 | les fronts |
| 6 | Règles FW1 et publication | tout le reste |