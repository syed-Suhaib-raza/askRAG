from collections import deque
import re


class ConversationMemory:
    def __init__(self, max_turns=6):
        """
        Stores recent conversation turns.

        Args:
            max_turns (int): number of conversation turns to keep
        """
        self.history = deque(maxlen=max_turns)

    def add_turn(self, user_query, assistant_response, topic=None):
        """
        Add a conversation turn.

        Args:
            user_query (str)
            assistant_response (str)
            topic (str)
        """

        if topic is None:
            topic = self.extract_topic(user_query)

        self.history.append({
            "user": user_query,
            "assistant": assistant_response,
            "topic": topic
        })

    def get_last_topic(self):
        """Return the most recent topic"""
        if not self.history:
            return None

        return self.history[-1]["topic"]

    def get_recent_queries(self, n=3):
        """Return last n user queries"""
        return [h["user"] for h in list(self.history)[-n:]]

    def get_history(self):
        """Return full history"""
        return list(self.history)

    def extract_topic(self, query):
        """
        Very simple entity/topic extraction.

        Example:
        'Tell me about the transistor'
        -> transistor
        """

        query = query.lower()

        # remove question words
        query = re.sub(
            r"\b(what|who|when|where|why|how|tell|me|about|the|is|are|was|were)\b",
            "",
            query
        )

        words = query.split()

        if not words:
            return None

        return words[-1]