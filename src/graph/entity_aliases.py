from src.graph.normalization import (
    normalize_entity_id,
)

ENTITY_ALIASES = {
    # Business objects
    "purchase_order": [
        "purchase order",
        "commande d'achat",
        "bon de commande",
    ],

    "purchase_requisition": [
        "purchase requisition",
        "demande d'achat",
        "demande d'approvisionnement",
    ],

    "sales_order": [
        "sales order",
        "commande client",
        "commande de vente",
    ],

    "goods_receipt": [
        "goods receipt",
        "réception de marchandises",
        "reception de marchandises",
    ],

    "delivery": [
        "delivery",
        "livraison",
    ],

    # Processes / concepts
    "procurement": [
        "procurement",
        "approvisionnement",
        "processus d'approvisionnement",
        "achats",
    ],

    "accounts_payable": [
        "accounts payable",
        "comptes fournisseurs",
        "comptabilité fournisseurs",
        "comptabilite fournisseurs",
    ],

    "billing": [
        "billing",
        "facturation",
    ],

    "shipping": [
        "shipping",
        "expédition",
        "expedition",
    ],

    # SAP modules
    "sap_mm": [
        "sap mm",
        "module mm",
        "gestion des articles",
        "materials management",
    ],

    "sap_sd": [
        "sap sd",
        "module sd",
        "sales and distribution",
        "ventes et distribution",
    ],

    "sap_fi": [
        "sap fi",
        "module fi",
        "financial accounting",
        "comptabilité financière",
        "comptabilite financiere",
    ],
}


def get_normalized_aliases(
    entity_id: str,
) -> list[str]:
    aliases = ENTITY_ALIASES.get(
        entity_id,
        [],
    )

    return [
        normalize_entity_id(alias)
        for alias in aliases
        if alias.strip()
    ]