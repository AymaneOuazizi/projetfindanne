def build_graph_extraction_prompt(
    chunk_content: str,
) -> str:
    return f"""
You are extracting a structured SAP knowledge graph
from a source passage.

Extract ONLY facts that are explicitly supported by
the provided passage.

Do not use outside knowledge.
Do not infer relationships that are not supported.
Do not invent entities.
Do not invent SAP facts.

Allowed entity types:

- Module
- Process
- BusinessObject
- Concept

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
An important SAP domain concept that does not fit
the previous categories.

Allowed relationship types:

CONTAINS_PROCESS
Use only when the text explicitly indicates that a
SAP module contains, covers, or includes a process.

USES_OBJECT
Use only when the text explicitly indicates that a
process uses or involves a business object.

PRECEDES
Use only when the text explicitly indicates that one
business object occurs before another in a process.

Rules:

1. Extract only explicitly supported information.
2. Do not infer missing steps.
3. Do not create relationships merely because two
   entities appear in the same passage.
4. Relationship source and target names must match
   names present in the entities list.
5. Use concise canonical names.
6. Remove duplicate entities.
7. Remove duplicate relationships.
8. Return JSON only.
9. Do not include Markdown.
10. Do not include explanations.

Return exactly this structure:

{{
    "entities": [
        {{
            "name": "Purchase Order",
            "type": "BusinessObject"
        }}
    ],
    "relationships": [
        {{
            "source": "Purchase Requisition",
            "target": "Purchase Order",
            "type": "PRECEDES"
        }}
    ]
}}

If there are no valid entities or relationships,
return empty lists.

SOURCE PASSAGE:

{chunk_content}
""".strip()