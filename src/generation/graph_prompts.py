from src.graph.search import (
    GraphSearchResult,
)


def build_graph_context(
    result: GraphSearchResult,
) -> str:
    sections = []

    if result.relationships:
        graph_lines = []

        for index, relation in enumerate(
            result.relationships,
            start=1,
        ):
            chunk_ids = (
                ", ".join(
                    str(chunk_id)
                    for chunk_id
                    in relation.source_chunk_ids
                )
            )

            if not chunk_ids:
                chunk_ids = "unknown"

            graph_lines.append(
                
                    f"[GRAPH FACT {index}]\n"
                    f"{relation.source_name} "
                    f"--{relation.relationship}--> "
                    f"{relation.target_name}\n"
                    f"Supporting chunk IDs: "
                    f"{chunk_ids}"
                
            )

        sections.append(
            "GRAPH FACTS\n"
            + "=" * 60
            + "\n\n"
            + "\n\n".join(
                graph_lines
            )
        )

    if result.evidence_chunks:
        source_lines = []

        for index, chunk in enumerate(
            result.evidence_chunks,
            start=1,
        ):
            source_lines.append(
                
                    f"[SOURCE {index}]\n"
                    f"Document: {chunk.title}\n"
                    f"Source: {chunk.source}\n"
                    f"Chunk ID: {chunk.chunk_id}\n"
                    f"Chunk index: "
                    f"{chunk.chunk_index}\n\n"
                    f"{chunk.content}"
                
            )

        sections.append(
            "SOURCE EVIDENCE\n"
            + "=" * 60
            + "\n\n"
            + "\n\n".join(
                source_lines
            )
        )

    return "\n\n".join(
        sections
    )