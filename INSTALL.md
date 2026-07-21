# Guide d'installation et d'utilisation

## Prérequis

- Python 3.10 ou supérieur
- Git

Vérifier la version de Python installée :

```
python3 --version
```

## Installation

```
git clone https://github.com/DavyAymard/cisco-fortigate-base-provisioner.git
cd cisco-fortigate-base-provisioner
pip install -r requirements.txt
```

## Utilisation

### 1. Créer le fichier de paramètres de la base

Copier le fichier exemple et l'adapter à la nouvelle base :

```
cp config/base_exemple.yaml config/ma_base.yaml
```

Ouvrir `config/ma_base.yaml` et renseigner :

- Nom de la base et code site
- Bloc réseau racine (ex : `10.60.0.0/16`)
- Nombre d'utilisateurs estimé par VLAN
- Type de liaison principale et de secours (starlink, vsat, 4g, fibre, aucune)
- Présence ou non d'un cluster FortiGate HA

### 2. Lancer le générateur

```
python generator/main.py config/ma_base.yaml
```

Un dossier `output/<code_site>/` est créé avec les fichiers suivants :

| Fichier                       | Usage                                              |
|--------------------------------|-----------------------------------------------------|
| `cisco_vlan_config.txt`         | À coller dans la configuration du switch Cisco       |
| `cisco_acl_recap.txt`           | Document de référence pour audit/revue de sécurité   |
| `fortigate_interfaces.conf`     | À coller ou importer sur le FortiGate                |
| `fortigate_policy.conf`         | À coller ou importer sur le FortiGate                |
| `checklist_deploiement.md`      | À suivre pendant l'installation terrain              |

### 3. Vérifier avant déploiement

Avant toute application sur un équipement réel :

- Faire relire les configurations générées par un second technicien
- Confirmer qu'il n'y a pas de conflit d'adressage avec un autre site déjà en service
- Tester la génération une première fois avec `config/base_exemple.yaml` pour valider l'installation

## Personnaliser un template

Les fichiers `.j2` du dossier `templates/` peuvent être modifiés pour ajuster la configuration générée (ex : ajouter un profil QoS, changer les ACL par défaut). Après modification, relancer simplement le générateur pour appliquer les changements.

## Dépannage

**`ModuleNotFoundError: No module named 'yaml'` ou `'jinja2'`**

Le fichier `requirements.txt` n'a pas été installé. Relancer :
```
pip install -r requirements.txt
```

**`ValueError: Bloc racine ... trop petit`**

Le réseau racine défini dans le YAML est trop petit pour le nombre de VLANs demandé. Agrandir le bloc (ex : passer de `/20` à `/16`).
