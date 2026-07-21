# Checklist de déploiement - Base_Exemple (EXM)

## 1. Avant intervention
- [ ] Config Cisco et FortiGate générées et relues par un second technicien
- [ ] Adressage IP validé, pas de conflit avec un autre site connu
- [ ] Liaison principale confirmée disponible sur site : starlink
- [ ] Liaison de secours testée : 4g

## 2. Déploiement switch (Cisco)
- [ ] VLANs créés et nommés correctement
- [ ] Trunk configuré vers switches d'accès
- [ ] SVI up/up avec la bonne IP de passerelle

## 3. Déploiement FortiGate
- [ ] Interfaces VLAN créées avec le bon rôle (lan/dmz)
- [ ] DHCP actif sur chaque VLAN, plage conforme au plan
- [ ] Policies inter-VLAN testées (deny confirmé entre GUEST et DATA)
- [ ] SD-WAN configuré si liaison de secours présente

## 4. Tests post-installation
- [ ] Ping inter-VLAN bloqué là où attendu
- [ ] Accès Internet fonctionnel depuis chaque VLAN
- [ ] Bascule sur liaison de secours testée manuellement (coupure wan1)
- [ ] Un utilisateur test par VLAN confirme un accès normal

## 5. Clôture
- [ ] Configs versionnées dans le repo (commit avec date + nom du technicien)
- [ ] Schéma réseau mis à jour
- [ ] Coordination informée de la mise en service