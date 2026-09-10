from src.config import settings
from src.graph.database import driver

MODULES = [
    {
        "entity_id": "sap_mm",
        "name": "SAP MM",
    },
    {
        "entity_id": "sap_sd",
        "name": "SAP SD",
    },
    {
        "entity_id": "sap_fi",
        "name": "SAP FI",
    },
]


PROCESSES = [
    {
        "entity_id": "procurement",
        "name": "Procurement",
    },
    {
        "entity_id": "inventory_management",
        "name": "Inventory Management",
    },
    {
        "entity_id": "sales_order_processing",
        "name": "Sales Order Processing",
    },
    {
        "entity_id": "shipping",
        "name": "Shipping",
    },
    {
        "entity_id": "billing",
        "name": "Billing",
    },
    {
        "entity_id": "accounts_payable",
        "name": "Accounts Payable",
    },
    {
        "entity_id": "accounts_receivable",
        "name": "Accounts Receivable",
    },
    {
        "entity_id": "general_ledger",
        "name": "General Ledger",
    },
]


BUSINESS_OBJECTS = [
    {
        "entity_id": "purchase_requisition",
        "name": "Purchase Requisition",
    },
    {
        "entity_id": "purchase_order",
        "name": "Purchase Order",
    },
    {
        "entity_id": "goods_receipt",
        "name": "Goods Receipt",
    },
    {
        "entity_id": "sales_order",
        "name": "Sales Order",
    },
    {
        "entity_id": "delivery",
        "name": "Delivery",
    },
]


def seed_nodes(session) -> None:
    session.run(
        """
        UNWIND $rows AS row

        MERGE (
            node:Module {
                entity_id: row.entity_id
            }
        )

        SET
            node.name = row.name
        """,
        rows=MODULES,
    ).consume()

    session.run(
        """
        UNWIND $rows AS row

        MERGE (
            node:Process {
                entity_id: row.entity_id
            }
        )

        SET
            node.name = row.name
        """,
        rows=PROCESSES,
    ).consume()

    session.run(
        """
        UNWIND $rows AS row

        MERGE (
            node:BusinessObject {
                entity_id: row.entity_id
            }
        )

        SET
            node.name = row.name
        """,
        rows=BUSINESS_OBJECTS,
    ).consume()


def seed_module_relationships(
    session,
) -> None:
    relationships = [
        (
            "sap_mm",
            "procurement",
        ),
        (
            "sap_mm",
            "inventory_management",
        ),
        (
            "sap_sd",
            "sales_order_processing",
        ),
        (
            "sap_sd",
            "shipping",
        ),
        (
            "sap_sd",
            "billing",
        ),
        (
            "sap_fi",
            "accounts_payable",
        ),
        (
            "sap_fi",
            "accounts_receivable",
        ),
        (
            "sap_fi",
            "general_ledger",
        ),
    ]

    for module_id, process_id in relationships:
        session.run(
            """
            MATCH (
                module:Module {
                    entity_id: $module_id
                }
            )

            MATCH (
                process:Process {
                    entity_id: $process_id
                }
            )

            MERGE (
                module
            )-[:CONTAINS_PROCESS]->(
                process
            )
            """,
            module_id=module_id,
            process_id=process_id,
        ).consume()


def seed_process_object_relationships(
    session,
) -> None:
    relationships = [
        (
            "procurement",
            "purchase_requisition",
        ),
        (
            "procurement",
            "purchase_order",
        ),
        (
            "procurement",
            "goods_receipt",
        ),
        (
            "sales_order_processing",
            "sales_order",
        ),
        (
            "shipping",
            "delivery",
        ),
    ]

    for process_id, object_id in relationships:
        session.run(
            """
            MATCH (
                process:Process {
                    entity_id: $process_id
                }
            )

            MATCH (
                object:BusinessObject {
                    entity_id: $object_id
                }
            )

            MERGE (
                process
            )-[:USES_OBJECT]->(
                object
            )
            """,
            process_id=process_id,
            object_id=object_id,
        ).consume()


def seed_process_flow(
    session,
) -> None:
    relationships = [
        (
            "purchase_requisition",
            "purchase_order",
        ),
        (
            "purchase_order",
            "goods_receipt",
        ),
        (
            "sales_order",
            "delivery",
        ),
    ]

    for source_id, target_id in relationships:
        session.run(
            """
            MATCH (
                source:BusinessObject {
                    entity_id: $source_id
                }
            )

            MATCH (
                target:BusinessObject {
                    entity_id: $target_id
                }
            )

            MERGE (
                source
            )-[:PRECEDES]->(
                target
            )
            """,
            source_id=source_id,
            target_id=target_id,
        ).consume()


def seed_initial_graph() -> None:
    with driver.session(
        database=settings.neo4j_database
    ) as session:
        seed_nodes(session)

        seed_module_relationships(
            session
        )

        seed_process_object_relationships(
            session
        )

        seed_process_flow(
            session
        )