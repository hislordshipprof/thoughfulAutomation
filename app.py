import streamlit as st
import os
from dotenv import load_dotenv
from rapidfuzz import fuzz, process
from openai import OpenAI

# Load environment variables
load_dotenv()

# Predefined Q&A dataset about Thoughtful AI
PREDEFINED_QA = [
    {
        "question": "What does the eligibility verification agent (EVA) do?",
        "answer": "EVA automates the process of verifying a patient's eligibility and benefits information in real-time, eliminating manual data entry errors and reducing claim rejections."
    },
    {
        "question": "What does the claims processing agent (CAM) do?",
        "answer": "CAM streamlines the submission and management of claims, improving accuracy, reducing manual intervention, and accelerating reimbursements."
    },
    {
        "question": "How does the payment posting agent (PHIL) work?",
        "answer": "PHIL automates the posting of payments to patient accounts, ensuring fast, accurate reconciliation of payments and reducing administrative burden."
    },
    {
        "question": "Tell me about Thoughtful AI's Agents.",
        "answer": "Thoughtful AI provides a suite of AI-powered automation agents designed to streamline healthcare processes. These include Eligibility Verification (EVA), Claims Processing (CAM), and Payment Posting (PHIL), among others."
    },
    {
        "question": "What are the benefits of using Thoughtful AI's agents?",
        "answer": "Using Thoughtful AI's Agents can significantly reduce administrative costs, improve operational efficiency, and reduce errors in critical processes like claims management and payment posting."
    }
]

# Fuzzy matching threshold (0-100)
FUZZY_THRESHOLD = 70


def find_best_match(user_question: str) -> tuple[str, float] | None:
    """
    Find the best matching predefined question using fuzzy matching.
    
    Args:
        user_question: The user's input question
        
    Returns:
        Tuple of (answer, score) if match found above threshold, None otherwise
    """
    if not user_question or not user_question.strip():
        return None
    
    # Extract all predefined questions
    questions = [qa["question"] for qa in PREDEFINED_QA]
    
    # Find best match using fuzzy matching
    result = process.extractOne(
        user_question,
        questions,
        scorer=fuzz.token_set_ratio
    )
    
    if result and result[1] >= FUZZY_THRESHOLD:
        matched_question = result[0]
        score = result[1]
        
        # Find the corresponding answer
        for qa in PREDEFINED_QA:
            if qa["question"] == matched_question:
                return (qa["answer"], score)
    
    return None


def get_openai_response(user_question: str, api_key: str) -> str:
    """
    Get a response from OpenAI API when no predefined match is found.
    
    Args:
        user_question: The user's input question
        api_key: OpenAI API key
        
    Returns:
        Response from OpenAI or error message
    """
    try:
        client = OpenAI(api_key=api_key)
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful customer support assistant. Be concise and friendly."},
                {"role": "user", "content": user_question}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"I apologize, but I'm having trouble connecting to my knowledge base. Error: {str(e)}"


def get_agent_response(user_question: str, api_key: str) -> dict:
    """
    Get agent response using fuzzy matching or OpenAI fallback.
    
    Args:
        user_question: The user's input question
        api_key: OpenAI API key
        
    Returns:
        Dictionary with 'answer' and 'source' keys
    """
    # First, try fuzzy matching with predefined Q&A
    match_result = find_best_match(user_question)
    
    if match_result:
        answer, score = match_result
        return {
            "answer": answer,
            "source": f"predefined (match: {score:.0f}%)"
        }
    
    # Fallback to OpenAI
    answer = get_openai_response(user_question, api_key)
    return {
        "answer": answer,
        "source": "OpenAI"
    }


def main():
    """Main Streamlit application."""
    
    # Page configuration
    st.set_page_config(
        page_title="Thoughtful AI Support Agent",
        page_icon="🤖",
        layout="centered"
    )
    
    # Title and description
    st.title("🤖 Thoughtful AI Support Agent")
    st.markdown("Ask me anything about Thoughtful AI's automation agents or general questions!")
    
    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key or api_key == "your_openai_api_key_here":
        st.error("⚠️ OpenAI API key not found! Please set OPENAI_API_KEY in your .env file.")
        st.info("See README.md for setup instructions.")
        st.stop()
    
    # Initialize chat history in session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Hello! I'm here to help you learn about Thoughtful AI's automation agents. You can ask me about EVA, CAM, PHIL, or any general questions you might have!",
            "source": None
        })
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message.get("source"):
                st.caption(f"*Source: {message['source']}*")
    
    # Chat input
    if user_input := st.chat_input("Type your question here..."):
        # Validate input
        if not user_input.strip():
            st.warning("Please enter a valid question.")
            return
        
        # Add user message to chat
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "source": None
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_agent_response(user_input, api_key)
            
            st.markdown(response["answer"])
            st.caption(f"*Source: {response['source']}*")
        
        # Add assistant message to chat
        st.session_state.messages.append({
            "role": "assistant",
            "content": response["answer"],
            "source": response["source"]
        })
    
    # Sidebar with example questions
    with st.sidebar:
        st.header("💡 Example Questions")
        st.markdown("""
        **About Thoughtful AI:**
        - What does EVA do?
        - Tell me about CAM
        - How does PHIL work?
        - What are the benefits?
        
        **General Questions:**
        - What is machine learning?
        - How can AI help healthcare?
        """)
        
        st.divider()
        
        if st.button("🗑️ Clear Chat History"):
            st.session_state.messages = [{
                "role": "assistant",
                "content": "Chat cleared! How can I help you?",
                "source": None
            }]
            st.rerun()


if __name__ == "__main__":
    main()

