from retrieval.hierarchichal.page_retriever import PageRetriever
from retrieval.hierarchichal.section_retriever import SectionRetriever
from retrieval.hierarchichal.chunk_retriever import ChunkRetriever

from context.query_rewriter import QueryRewriter
from context.conversation_memory import ConversationMemory


class ContextBuilder:
    def __init__(
        self,
        page_retriever=None,
        section_retriever=None,
        chunk_retriever=None,
        query_rewriter=None,
        conversation_memory=None,
        top_pages=5,
        top_sections=5,
        top_chunks=10
    ):

        self.page_retriever = page_retriever or PageRetriever()
        self.section_retriever = section_retriever or SectionRetriever()
        self.chunk_retriever = chunk_retriever or ChunkRetriever()

        self.query_rewriter = query_rewriter or QueryRewriter()
        self.memory = conversation_memory or ConversationMemory()

        self.top_pages = top_pages
        self.top_sections = top_sections
        self.top_chunks = top_chunks

    def build(self, user_query):

        # -------------------------
        # 1 Rewrite Query
        # -------------------------

        rewritten_query = self.query_rewriter.rewrite(
            user_query,
            self.memory
        )

        # -------------------------
        # 2 Retrieve Pages
        # -------------------------

        pages = self.page_retriever.retrieve(
            rewritten_query,
            top_k=self.top_pages
        )

        page_ids = []
        if pages:
            page_ids = [p["page_id"] for p in pages]

        # -------------------------
        # 3 Retrieve Sections
        # -------------------------

        sections = []
        if page_ids:

            sections = self.section_retriever.retrieve(
                rewritten_query,
                page_ids,
                top_k=self.top_sections
            )

        # -------------------------
        # 4 Retrieve Chunks
        # -------------------------

        chunks = []
        if sections:

            section_ids = [s["section_id"] for s in sections]

            chunks = self.chunk_retriever.retrieve(
                rewritten_query,
                section_ids,
                top_k=self.top_chunks
            )

        # -------------------------
        # 5 Prepare chunk text
        # -------------------------

        chunk_texts = []

        for chunk in chunks:

            if isinstance(chunk, dict):

                text = chunk.get("text", "")
                page = chunk.get("page", "")
                section = chunk.get("section", "")

                formatted = f"[Page: {page} | Section: {section}]\n{text}"

                chunk_texts.append(formatted)

            else:
                chunk_texts.append(chunk)

        # -------------------------
        # 6 Build Final Context
        # -------------------------

        context = "\n\n".join(chunk_texts)

        return {
            "query": rewritten_query,
            "context": context,
            "chunks": chunk_texts,
            "pages": pages,
            "sections": sections
        }