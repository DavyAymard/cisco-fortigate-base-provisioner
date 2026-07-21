"""
main.py

Point d'entrée CLI. Prend un fichier YAML de base en entrée,
calcule le plan d'adressage, génère les configs Cisco et FortiGate,
et écrit une checklist de déploiement personnalisée.

Usage :
    python generator/main.py config/base_exemple.yaml
    python generator/main.py config/base_exemple.yaml --output output/ma_base
"""

import argparse
import sys
import yaml

from ip_planner import planifier_adressage
from render import generer_tous


def charger_config(chemin_yaml: str) -> dict:
    with open(chemin_yaml, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def generer_checklist(config: dict, plan: list, dossier_sortie: str):
    base = config["base"]
    liaisons = config["liaisons"]

    lignes = [
        f"# Checklist de déploiement - {base['nom']} ({base['code_site']})",
        "",
        "## 1. Avant intervention",
        "- [ ] Config Cisco et FortiGate générées et relues par un second technicien",
        "- [ ] Adressage IP validé, pas de conflit avec un autre site connu",
        f"- [ ] Liaison principale confirmée disponible sur site : {liaisons['principale']}",
    ]

    if liaisons["secours"] != "aucune":
        lignes.append(f"- [ ] Liaison de secours testée : {liaisons['secours']}")

    lignes += [
        "",
        "## 2. Déploiement switch (Cisco)",
        "- [ ] VLANs créés et nommés correctement",
        "- [ ] Trunk configuré vers switches d'accès",
        "- [ ] SVI up/up avec la bonne IP de passerelle",
        "",
        "## 3. Déploiement FortiGate",
        "- [ ] Interfaces VLAN créées avec le bon rôle (lan/dmz)",
        "- [ ] DHCP actif sur chaque VLAN, plage conforme au plan",
        "- [ ] Policies inter-VLAN testées (deny confirmé entre GUEST et DATA)",
        "- [ ] SD-WAN configuré si liaison de secours présente",
        "",
        "## 4. Tests post-installation",
        "- [ ] Ping inter-VLAN bloqué là où attendu",
        "- [ ] Accès Internet fonctionnel depuis chaque VLAN",
        "- [ ] Bascule sur liaison de secours testée manuellement (coupure wan1)",
        "- [ ] Un utilisateur test par VLAN confirme un accès normal",
        "",
        "## 5. Clôture",
        "- [ ] Configs versionnées dans le repo (commit avec date + nom du technicien)",
        "- [ ] Schéma réseau mis à jour",
        "- [ ] Coordination informée de la mise en service",
    ]

    chemin = f"{dossier_sortie}/checklist_deploiement.md"
    with open(chemin, "w", encoding="utf-8") as f:
        f.write("\n".join(lignes))
    return chemin


def main():
    parser = argparse.ArgumentParser(
        description="Génère les configs Cisco/FortiGate d'une base à partir d'un YAML."
    )
    parser.add_argument("config_yaml", help="Chemin vers le fichier YAML de la base")
    parser.add_argument(
        "--output", default=None,
        help="Dossier de sortie (défaut : output/<code_site>)"
    )
    args = parser.parse_args()

    config = charger_config(args.config_yaml)
    plan = planifier_adressage(config)

    dossier_sortie = args.output or f"output/{config['base']['code_site']}"

    fichiers = generer_tous(config, plan, dossier_sortie)
    checklist = generer_checklist(config, plan, dossier_sortie)

    print(f"Base : {config['base']['nom']} ({config['base']['code_site']})")
    print(f"VLANs planifiés : {len(plan)}")
    print("Fichiers générés :")
    for f in fichiers:
        print(f"  - {f}")
    print(f"  - {checklist}")


if __name__ == "__main__":
    sys.exit(main())
