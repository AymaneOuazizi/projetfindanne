from src.config import settings
from src.graph.database import driver

ENTITY_DOCUMENT_MAPPING = [
    {
        "label": "Module",
        "entity_id": "sap_mm",
        "document_title": "sap_mm",
    },
    {
        "label": "Process",
        "entity_id": "procurement",
        "document_title": "sap_mm",
    },
    {
        "label": "Process",
        "entity_id": "inventory_management",
        "document_title": "sap_mm",
    },
    {
        "label": "BusinessObject",
        "entity_id": "purchase_requisition",
        "document_title": "sap_mm",
    },
    {
        "label": "BusinessObject",
        "entity_id": "purchase_order",
        "document_title": "sap_mm",
    },
    {
        "label": "BusinessObject",
        "entity_id": "goods_receipt",
        "document_title": "sap_mm",
    },

    {
        "label": "Module",
        "entity_id": "sap_sd",
        "document_title": "sap_sd",
    },
    {
        "label": "Process",
        "entity_id": "sales_order_processing",
        "document_title": "sap_sd",
    },
    {
        "label": "Process",
        "entity_id": "shipping",
        "document_title": "sap_sd",
    },
    {
        "label": "Process",
        "entity_id": "billing",
        "document_title": "sap_sd",
    },
    {
        "label": "BusinessObject",
        "entity_id": "sales_order",
        "document_title": "sap_sd",
    },
    {
        "label": "BusinessObject",
        "entity_id": "delivery",
        "document_title": "sap_sd",
    },

    {
        "label": "Module",
        "entity_id": "sap_fi",
        "document_title": "sap_fi",
    },
    {
        "label": "Process",
        "entity_id": "accounts_payable",
        "document_title": "sap_fi",
    },
    {
        "label": "Process",
        "entity_id": "accounts_receivable",
        "document_title": "sap_fi",
    },
    {
        "label": "Process",
        "entity_id": "general_ledger",
        "document_title": "sap_fi",
    },
]


ALLOWED_LABELS = {
    "Module",
    "Process",
    "BusinessObject",
    "Concept",
}


def create_entity_provenance() -> int:
    created_mappings = 0

    with driver.session(
        database=settings.neo4j_database
    ) as session:

        for mapping in (
            ENTITY_DOCUMENT_MAPPING
        ):
            label = mapping["label"]

            if label not in ALLOWED_LABELS:
                raise ValueError(
                    f"Invalid graph label: "
                    f"{label}"
                )

            query = f"""
            MATCH (
                entity:{label} {{
                    entity_id: $entity_id
                }}
            )

            MATCH (
                document:Document {{
                    title: $document_title
                }}
            )

            MATCH (
                document
            )-[:HAS_CHUNK]->(
                chunk:Chunk
            )

            MERGE (
                entity
            )-[:SUPPORTED_BY]->(
                chunk
            )
            """

            session.run(
                query,
                entity_id=(
                    mapping["entity_id"]
                ),
                document_title=(
                    mapping[
                        "document_title"
                    ]
                ),
            ).consume()

            created_mappings += 1

    return created_mappings