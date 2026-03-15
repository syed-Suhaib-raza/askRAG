import re


class QueryRewriter:
    def __init__(self):
        pass

    def rewrite(self, query, conversation_memory=None):
        """
        Rewrites the query for better retrieval.

        Args:
            query (str): user query
            conversation_memory:
                - ConversationMemory object OR
                - list[str] of previous queries

        Returns:
            str: rewritten query
        """

        query = query.strip()

        topic = None

        # Case 1: ConversationMemory object
        if conversation_memory and hasattr(conversation_memory, "get_last_topic"):
            topic = conversation_memory.get_last_topic()

        # Case 2: list of previous queries
        elif isinstance(conversation_memory, list) and conversation_memory:
            topic = conversation_memory[-1]

        # Resolve short follow-up queries
        if topic and len(query.split()) < 4:
            query = f"{query} {topic}"

        # Remove punctuation
        query = re.sub(r"[^\w\s]", "", query)

        # Lowercase for retrieval
        query = query.lower()

        return query