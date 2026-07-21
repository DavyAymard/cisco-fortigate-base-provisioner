"""
render.py

Charge les templates Jinja2 et injecte le contexte (base, vlans planifiés,
liaisons, sécurité) pour produire les fichiers de configuration finaux.
"""

import os
from jinja2 import Environment, FileSystemLoader

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "..", "templates")


def _env():
    return Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )


def rendre(template_nom: str, contexte: dict) -> str:
    env = _env()
    template = env.get_template(template_nom)
    return template.render(**contexte)


def generer_tous(config: dict, plan: list, dossier_sortie: str):
    contexte = {
        "base": config["base"],
        "plan": plan,
        "liaisons": config["liaisons"],
        "securite": config["securite"],
    }

    os.makedirs(dossier_sortie, exist_ok=True)

    fichiers = {
        "cisco_vlan.j2": "cisco_vlan_config.txt",
        "cisco_acl.j2": "cisco_acl_recap.txt",
        "fortigate_interfaces.j2": "fortigate_interfaces.conf",
        "fortigate_policy.j2": "fortigate_policy.conf",
    }

    chemins_generes = []
    for template_nom, nom_sortie in fichiers.items():
        contenu = rendre(template_nom, contexte)
        chemin = os.path.join(dossier_sortie, nom_sortie)
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(contenu)
        chemins_generes.append(chemin)

    return chemins_generes
