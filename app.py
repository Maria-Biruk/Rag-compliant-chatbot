import streamlit as st

from src.rag_pipeline import ask


st.set_page_config(
    page_title="CrediTrust Complaint Assistant"
)


st.title("🤖 CrediTrust Complaint Assistant")

st.write(
    "Ask questions about customer complaints."
)


if "answer" not in st.session_state:
    st.session_state.answer = ""

if "sources" not in st.session_state:
    st.session_state.sources = []


question = st.text_input(
    "Enter your question"
)


col1, col2 = st.columns(2)


with col1:

    if st.button("Ask"):

        if question:

            with st.spinner("Searching complaints..."):

                answer, sources = ask(question)

                st.session_state.answer = answer
                st.session_state.sources = sources


with col2:

    if st.button("Clear"):

        st.session_state.answer = ""
        st.session_state.sources = []


if st.session_state.answer:


    st.subheader("Answer")

    st.write(
        st.session_state.answer
    )


    st.subheader("Sources")

    for i, source in enumerate(
        st.session_state.sources
    ):

        st.write(
            f"Source {i+1}:"
        )

        st.info(source)