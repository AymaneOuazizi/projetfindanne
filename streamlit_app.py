import time

import streamlit as st

from src.generation.unified_rag import (
    ask_rag,
)
from src.ingestion.upload import (
    save_uploaded_file,
)
from src.ingestion.upload_pipeline import (
    ingest_uploaded_files,
)

st.set_page_config(
    page_title=(
        "SAP RAG Platform"
    ),
    page_icon="🧠",
    layout="wide",
)


# ============================================================
# Header
# ============================================================

st.title(
    "SAP Knowledge RAG Platform"
)

st.caption(
    "Vector RAG • Hybrid RAG • GraphRAG"
)

st.write(
    "Ask questions about your SAP documents "
    "and compare different retrieval "
    "architectures."
)


# ============================================================
# Session state
# ============================================================

if "uploaded_document_names" not in (
    st.session_state
):
    st.session_state[
        "uploaded_document_names"
    ] = []


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:
    st.header(
        "Document Ingestion"
    )

    st.write(
        "Upload text-based SAP documents "
        "to add them to the knowledge base."
    )

    uploaded_files = st.file_uploader(
        "Upload documents",
        type=[
            "txt",
            "md",
            "markdown",
            "pdf",
        ],
        accept_multiple_files=True,
    )

    ingest_button = (
        st.button(
            "Ingest Documents",
            use_container_width=True,
            type="primary",
        )
    )

    if ingest_button:
        if not uploaded_files:
            st.warning(
                "Please select at least "
                "one TXT or PDF file."
            )

        else:
            saved_paths = []

            try:
                progress = (
                    st.progress(0)
                )

                status = (
                    st.empty()
                )

                total_files = len(
                    uploaded_files
                )

                for index, uploaded_file in (
                    enumerate(
                        uploaded_files,
                        start=1,
                    )
                ):
                    status.info(
                        "Saving "
                        f"{uploaded_file.name}..."
                    )

                    path = (
                        save_uploaded_file(
                            filename=(
                                uploaded_file.name
                            ),
                            content=(
                                uploaded_file
                                .getvalue()
                            ),
                        )
                    )

                    saved_paths.append(
                        path
                    )

                    progress.progress(
                        int(
                            (
                                index
                                / total_files
                            )
                            * 40
                        )
                    )

                status.info(
                    "Ingesting documents, "
                    "generating embeddings "
                    "and rebuilding the "
                    "knowledge graph..."
                )

                progress.progress(
                    50
                )

                ingested = (
                    ingest_uploaded_files(
                        saved_paths
                    )
                )

                progress.progress(
                    100
                )

                st.session_state[
                    "uploaded_document_names"
                ].extend(
                    [
                        item["title"]
                        for item in ingested
                    ]
                )

                status.success(
                    "Documents ingested "
                    "successfully."
                )

            except Exception as exc:
                st.error(
                    "Ingestion failed:"
                )

                st.exception(
                    exc
                )

    st.divider()

    st.subheader(
        "Knowledge Base"
    )

    if st.session_state[
        "uploaded_document_names"
    ]:
        for document_name in (
            st.session_state[
                "uploaded_document_names"
            ]
        ):
            st.write(
                f"• {document_name}"
            )

    else:
        st.caption(
            "No documents uploaded "
            "during this session."
        )

    st.divider()

    st.caption(
        "Supported formats: TXT, PDF"
    )


# ============================================================
# Main tabs
# ============================================================

ask_tab, compare_tab = (
    st.tabs(
        [
            "Ask a Question",
            "Compare Architectures",
        ]
    )
)


# ============================================================
# Ask tab
# ============================================================

with ask_tab:
    st.header(
        "Ask the Knowledge Base"
    )

    architecture = (
        st.selectbox(
            "RAG architecture",
            options=[
                "Vector",
                "Hybrid",
                "Graph",
            ],
            key="ask_architecture",
        )
    )

    question = (
        st.text_area(
            "Question",
            placeholder=(
                "Example: What is a "
                "purchase order?"
            ),
            height=100,
            key="ask_question",
        )
    )

    ask_button = (
        st.button(
            "Generate Answer",
            type="primary",
            key="ask_button",
        )
    )

    if ask_button:
        if not question.strip():
            st.warning(
                "Please enter a question."
            )

        else:
            try:
                with st.spinner(
                    f"Running "
                    f"{architecture} RAG..."
                ):
                    start_time = (
                        time.perf_counter()
                    )

                    result = ask_rag(
                        question=question,
                        architecture=(
                            architecture
                        ),
                    )

                    latency_ms = (
                        (
                            time.perf_counter()
                            - start_time
                        )
                        * 1000
                    )

                st.divider()

                metric_col_1, metric_col_2 = (
                    st.columns(2)
                )

                with metric_col_1:
                    st.metric(
                        "Architecture",
                        architecture,
                    )

                with metric_col_2:
                    st.metric(
                        "Latency",
                        f"{latency_ms:.0f} ms",
                    )

                st.subheader(
                    "Answer"
                )

                st.markdown(
                    result.answer
                )

                st.subheader(
                    "Retrieved Sources"
                )

                if not result.sources:
                    st.info(
                        "No supporting source "
                        "chunks were retrieved."
                    )

                else:
                    for index, source in (
                        enumerate(
                            result.sources,
                            start=1,
                        )
                    ):
                        title = source.get(
                            "title",
                            "Unknown document",
                        )

                        chunk_id = (
                            source.get(
                                "chunk_id"
                            )
                        )

                        expander_title = (
                            f"Source {index} — "
                            f"{title}"
                        )

                        if chunk_id is not None:
                            expander_title += (
                                f" | Chunk "
                                f"{chunk_id}"
                            )

                        with st.expander(
                            expander_title
                        ):
                            st.caption(
                                source.get(
                                    "source",
                                    "",
                                )
                            )

                            st.write(
                                source.get(
                                    "content",
                                    "",
                                )
                            )

            except Exception as exc:
                st.error(
                    "An error occurred while "
                    "generating the answer."
                )

                st.exception(
                    exc
                )


# ============================================================
# Compare tab
# ============================================================

with compare_tab:
    st.header(
        "Compare RAG Architectures"
    )

    st.write(
        "Run the same question through "
        "Vector RAG, Hybrid RAG and "
        "GraphRAG."
    )

    comparison_question = (
        st.text_area(
            "Question to compare",
            placeholder=(
                "Example: Which SAP module "
                "is Purchase Order related "
                "to through Procurement?"
            ),
            height=100,
            key="comparison_question",
        )
    )

    compare_button = (
        st.button(
            "Compare",
            type="primary",
            key="compare_button",
        )
    )

    if compare_button:
        if not (
            comparison_question.strip()
        ):
            st.warning(
                "Please enter a question."
            )

        else:
            architectures = [
                "Vector",
                "Hybrid",
                "Graph",
            ]

            comparison_results = {}

            progress = (
                st.progress(0)
            )

            for index, architecture_name in (
                enumerate(
                    architectures,
                    start=1,
                )
            ):
                try:
                    with st.spinner(
                        f"Running "
                        f"{architecture_name}..."
                    ):
                        start_time = (
                            time.perf_counter()
                        )

                        result = ask_rag(
                            question=(
                                comparison_question
                            ),
                            architecture=(
                                architecture_name
                            ),
                        )

                        latency_ms = (
                            (
                                time.perf_counter()
                                - start_time
                            )
                            * 1000
                        )

                    comparison_results[
                        architecture_name
                    ] = {
                        "result": result,
                        "latency_ms": (
                            latency_ms
                        ),
                        "error": None,
                    }

                except Exception as exc:
                    comparison_results[
                        architecture_name
                    ] = {
                        "result": None,
                        "latency_ms": None,
                        "error": str(exc),
                    }

                progress.progress(
                    int(
                        (
                            index
                            / len(
                                architectures
                            )
                        )
                        * 100
                    )
                )

            st.divider()

            columns = (
                st.columns(3)
            )

            for column, architecture_name in zip(
                columns,
                architectures,
            ):
                data = (
                    comparison_results[
                        architecture_name
                    ]
                )

                with column:
                    st.subheader(
                        architecture_name
                    )

                    if data["error"]:
                        st.error(
                            data["error"]
                        )

                        continue

                    result = (
                        data["result"]
                    )

                    latency_ms = (
                        data["latency_ms"]
                    )

                    st.metric(
                        "Latency",
                        f"{latency_ms:.0f} ms",
                    )

                    st.metric(
                        "Sources",
                        len(
                            result.sources
                        ),
                    )

                    st.markdown(
                        "#### Answer"
                    )

                    st.markdown(
                        result.answer
                    )

                    st.markdown(
                        "#### Sources"
                    )

                    if not result.sources:
                        st.caption(
                            "No sources retrieved."
                        )

                    for source_index, source in (
                        enumerate(
                            result.sources,
                            start=1,
                        )
                    ):
                        title = (
                            source.get(
                                "title",
                                "Unknown",
                            )
                        )

                        with st.expander(
                            f"Source "
                            f"{source_index}: "
                            f"{title}"
                        ):
                            st.write(
                                source.get(
                                    "content",
                                    "",
                                )
                            )

            st.info(
                "Latency displayed here is "
                "a live single-query measurement "
                "and should not be interpreted "
                "as a statistically robust "
                "performance benchmark."
            )