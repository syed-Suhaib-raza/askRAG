import streamlit as st

from context.context_builder import ContextBuilder
from generation.generator import Generator


# -------------------------
# System Initialization
# -------------------------

@st.cache_resource
def load_system():
    context_builder = ContextBuilder()
    generator = Generator()
    return context_builder, generator


context_builder, generator = load_system()


# -------------------------
# Streamlit Page Config
# -------------------------

st.set_page_config(
    page_title="askRAG",
    page_icon="📚",
    layout="wide"
)

st.title("📚 askRAG")
st.caption("Offline Wikipedia RAG Assistant")


# -------------------------
# Chat History
# -------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -------------------------
# User Input
# -------------------------

if prompt := st.chat_input("Ask a question about Wikipedia..."):

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # -------------------------
    # Build Context
    # -------------------------

    result = context_builder.build(prompt)

    context = result["context"]
    rewritten_query = result["query"]

    pages = result.get("pages", [])
    sections = result.get("sections", [])
    chunks = result.get("chunks", [])

    # -------------------------
    # Debug Panels
    # -------------------------

    with st.expander("🔧 Retrieval Debug"):
        st.write("Pages retrieved:", len(pages))
        st.write("Sections retrieved:", len(sections))
        st.write("Chunks retrieved:", len(chunks))

    with st.expander("📄 Retrieved Chunk Text"):
        for i, chunk in enumerate(chunks):
            st.write(f"Chunk {i+1}")
            st.code(chunk)

    # -------------------------
    # Generate Answer
    # -------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            answer = generator.generate(
                context=context,
                question=rewritten_query
            )

        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    # -------------------------
    # Update Memory
    # -------------------------

    context_builder.memory.add_turn(
        user_query=prompt,
        assistant_response=answer
    )