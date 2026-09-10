from src.generation.graph_service import (
    generate_graph_answer,
)
from src.graph.search import (
    GraphSearchResult,
    search_graph_with_evidence,
)


def answer_question_graph(
    question: str,
    max_hops: int = 2,
) -> tuple[
    str,
    GraphSearchResult,
]:
    graph_result = (
        search_graph_with_evidence(
            question=question,
            max_hops=max_hops,
        )
    )

    answer = generate_graph_answer(
        question=question,
        graph_result=graph_result,
    )

    return (
        answer,
        graph_result,
    )