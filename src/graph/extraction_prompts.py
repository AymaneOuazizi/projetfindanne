def build_graph_extraction_prompt(
    chunk_content: str,
) -> str:
    return f"""
You are extracting a structured knowledge graph
from a source passage.

The source may contain SAP/domain knowledge or
general knowledge from a user-uploaded document.

Extract ONLY facts that are explicitly supported by
the provided passage.

Do not use outside knowledge.
Do not infer relationships that are not supported.
Do not invent entities.
Do not invent facts.

Allowed entity types:

SAP/domain entity types:

- Module
- Process
- BusinessObject
- Concept

Generic entity types:

- Person
- Organization
- Location
- Product
- System

Definitions:

Module:
A SAP functional module such as SAP MM, SAP SD,
or SAP FI.

Process:
A business process or business activity such as
Procurement, Billing, Shipping, or Accounts Payable.

BusinessObject:
A business document or business object such as
Purchase Order, Purchase Requisition, Sales Order,
Delivery, or Goods Receipt.

Concept:
An important domain concept that does not fit
the previous categories.

Person:
A named human person explicitly mentioned
in the passage.

Organization:
A named company, university, school, institution,
department, association, or other organization.

Location:
A named geographic place such as a city, country,
region, or physical location.

Product:
A named product, application, platform, or
commercial offering.

System:
A named technical system, software system,
information system, or infrastructure component.

Allowed relationship types:

CONTAINS_PROCESS
Use only when the text explicitly indicates that a
module contains, covers, or includes a process.

USES_OBJECT
Use only when the text explicitly indicates that a
process uses or involves a business object.

PRECEDES
Use only when the text explicitly indicates that one
business object or process occurs before another.

WORKS_AT
Use when the text explicitly states that a person
works for or works at an organization.

STUDIES_AT
Use when the text explicitly states that a person
studies at, attends, or is a student at an
educational organization.

MEMBER_OF
Use when the text explicitly states that an entity
is a member of an organization or group.

PART_OF
Use when the text explicitly states that an entity
is part of another entity.

LOCATED_IN
Use when the text explicitly states that an entity
is located in a named location.

USES
Use when the text explicitly states that an entity
uses another entity and no more specific allowed
relationship applies.

RELATED_TO
Use only when the passage explicitly states a
relationship but none of the more specific allowed
relationship types accurately represents it.

Rules:

1. Extract only explicitly supported information.
2. Do not infer missing facts or steps.
3. Do not create relationships merely because two
   entities appear in the same passage.
4. Relationship source and target names must match
   names present in the entities list.
5. Use concise canonical names.
6. Preserve meaningful names and acronyms such as
   SAP, ISGA, SAP MM, and S/4HANA.
7. Remove duplicate entities.
8. Remove duplicate relationships.
9. Prefer a specific relationship over RELATED_TO.
10. Do not create RELATED_TO merely because two
    entities occur in the same passage.
11. Return JSON only.
12. Do not include Markdown.
13. Do not include explanations.

Example 1:

SOURCE:
"Aymane is a student at ISGA."

OUTPUT:

{{
    "entities": [
        {{
            "name": "Aymane",
            "type": "Person"
        }},
        {{
            "name": "ISGA",
            "type": "Organization"
        }}
    ],
    "relationships": [
        {{
            "source": "Aymane",
            "target": "ISGA",
            "type": "STUDIES_AT"
        }}
    ]
}}

Example 2:

SOURCE:
"Procurement in SAP MM uses purchase orders."

OUTPUT:

{{
    "entities": [
        {{
            "name": "SAP MM",
            "type": "Module"
        }},
        {{
            "name": "Procurement",
            "type": "Process"
        }},
        {{
            "name": "Purchase Order",
            "type": "BusinessObject"
        }}
    ],
    "relationships": [
        {{
            "source": "SAP MM",
            "target": "Procurement",
            "type": "CONTAINS_PROCESS"
        }},
        {{
            "source": "Procurement",
            "target": "Purchase Order",
            "type": "USES_OBJECT"
        }}
    ]
}}

If there are no valid entities or relationships,
return empty lists.

SOURCE PASSAGE:

{chunk_content}
""".strip()