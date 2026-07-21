"""
ip_planner.py

Calcule un plan d'adressage cohérent pour chaque VLAN d'une base,
à partir du bloc réseau racine défini dans le YAML.

Logique :
- Le bloc racine est découpé en sous-réseaux /24 (ou plus petits si peu d'utilisateurs).
- Chaque VLAN reçoit un sous-réseau dédié, une passerelle (.1), et une plage DHCP.
"""

import ipaddress


def _taille_masque_pour(nb_utilisateurs: int) -> int:
    """Retourne le masque le plus petit qui couvre nb_utilisateurs + marge de 20%."""
    besoin = max(nb_utilisateurs + max(4, int(nb_utilisateurs * 0.2)), 8)
    for prefixe in range(30, 15, -1):
        capacite = 2 ** (32 - prefixe) - 2
        if capacite >= besoin:
            return prefixe
    return 16


def planifier_adressage(base_config: dict) -> list:
    """
    Retourne une liste de dicts, un par VLAN, avec :
    nom, id, cidr, masque, gateway, dhcp_debut, dhcp_fin, zone_fortigate
    """
    reseau_racine = ipaddress.ip_network(base_config["base"]["reseau_racine"])
    vlans = base_config["vlans"]

    # on découpe le bloc racine en sous-réseaux /24 successifs
    sous_reseaux_disponibles = list(reseau_racine.subnets(new_prefix=24))

    plan = []
    for i, vlan in enumerate(vlans):
        if i >= len(sous_reseaux_disponibles):
            raise ValueError(
                f"Bloc racine {reseau_racine} trop petit pour {len(vlans)} VLANs en /24. "
                "Agrandir 'reseau_racine' dans le YAML."
            )

        masque_ideal = _taille_masque_pour(vlan["utilisateurs_estimes"])
        sous_reseau_24 = sous_reseaux_disponibles[i]

        if masque_ideal > 24:
            sous_reseau_final = next(sous_reseau_24.subnets(new_prefix=masque_ideal))
        else:
            sous_reseau_final = sous_reseau_24

        hotes = list(sous_reseau_final.hosts())
        gateway = hotes[0]
        dhcp_debut = hotes[1] if len(hotes) > 1 else hotes[0]
        dhcp_fin = hotes[-1]

        plan.append({
            "nom": vlan["nom"],
            "id": vlan["id"],
            "cidr": str(sous_reseau_final),
            "reseau": str(sous_reseau_final.network_address),
            "masque": str(sous_reseau_final.netmask),
            "wildcard": str(sous_reseau_final.hostmask),
            "gateway": str(gateway),
            "dhcp_debut": str(dhcp_debut),
            "dhcp_fin": str(dhcp_fin),
            "zone_fortigate": vlan["zone_fortigate"],
        })

    return plan


if __name__ == "__main__":
    # test rapide autonome
    exemple = {
        "base": {"reseau_racine": "10.50.0.0/16"},
        "vlans": [
            {"nom": "DATA", "id": 10, "utilisateurs_estimes": 20, "zone_fortigate": "trust"},
            {"nom": "VOIX", "id": 20, "utilisateurs_estimes": 10, "zone_fortigate": "trust"},
        ],
    }
    for v in planifier_adressage(exemple):
        print(v)
