# Cisco / FortiGate Base Provisioner

Génère automatiquement les configurations réseau (Cisco IOS + FortiGate) pour
l'ouverture d'une nouvelle base terrain, à partir d'un simple fichier YAML.

## Contexte

Dans un environnement humanitaire multi-sites (missions ONU, ONG), chaque
ouverture de base réinvente la configuration réseau : adressage IP, VLANs,
règles de pare-feu. Cette approche manuelle est lente, source d'erreurs, et
laisse souvent passer des failles de segmentation (ex : VLAN invité non
isolé du réseau interne).

Cet outil standardise le processus : un fichier de paramètres par base,
un script, des configurations prêtes à déployer.

## Ce que ça fait

```
base_exemple.yaml  →  generator/main.py  →  configs Cisco IOS
                                          →  configs FortiGate
                                          →  checklist de déploiement
```

- Calcule un plan d'adressage IP cohérent (un sous-réseau par VLAN,
  dimensionné selon le nombre d'utilisateurs estimé)
- Génère une configuration Cisco IOS : VLANs, SVI, trunks, ACL inter-VLAN
- Génère une configuration FortiGate : interfaces VLAN, zones, DHCP,
  policies de pare-feu, SD-WAN failover si liaison de secours définie
- Produit une checklist de déploiement adaptée à la base

## Stack

- Python 3.10+
- Jinja2 (templating des configurations)
- PyYAML (lecture des paramètres)

## Installation

```bash
git clone https://github.com/DavyAymard/cisco-fortigate-base-provisioner.git
cd cisco-fortigate-base-provisioner
pip install -r requirements.txt
```

## Usage

1. Copier `config/base_exemple.yaml` et adapter les paramètres de la nouvelle base.
2. Lancer le générateur :

```bash
python generator/main.py config/ma_nouvelle_base.yaml
```

3. Récupérer les fichiers générés dans `output/<code_site>/` :
   - `cisco_vlan_config.txt`
   - `cisco_acl_recap.txt`
   - `fortigate_interfaces.conf`
   - `fortigate_policy.conf`
   - `checklist_deploiement.md`

## Exemple déjà généré

Le dossier `examples/base_20_users_vsat_4g/` contient une sortie complète
pour une base de 20 utilisateurs, 4 VLANs (DATA, VOIX, GUEST, IOT), liaison
principale Starlink avec secours 4G — sans avoir besoin d'exécuter le script.

## Points de sécurité pris en compte

- Politique par défaut : deny inter-VLAN, avec exceptions explicites
- VLAN GUEST et IOT isolés en zone dédiée côté FortiGate
- Profils IPS et antivirus appliqués sur le trafic sortant
- SD-WAN avec health-check pour bascule automatique entre liaisons

## Roadmap

- [ ] Support cluster FortiGate HA (actif/passif)
- [ ] Génération d'un schéma réseau (diagramme SVG) à partir du YAML
- [ ] Profil QoS dédié VLAN VOIX
- [ ] Export direct via API REST FortiGate (au lieu du fichier .conf statique)

## Auteur

Davy Aymard LITSE - IT Infrastructure & Cybersécurité
[linkedin.com/in/davylitse](https://linkedin.com/in/davylitse)
