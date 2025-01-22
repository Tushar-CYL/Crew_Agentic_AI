import streamlit as st
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def create_crew(query):
    """Create and return a CrewAI instance for the given query."""
    llm = LLM(model="gemini/gemini-1.5-pro-latest", temperature=0.7)
    search_tool = SerperDevTool(n=10)
    
    # Define agents
    research_analyst = Agent(
        role="Senior Research Analyst",
        goal=f"Research and analyze information about: {query}",
        backstory="You're an expert research analyst who can find and analyze information on any topic. "
                  "You focus on providing accurate, up-to-date information with proper citations.",
        allow_delegation=False,
        verbose=True,
        tools=[search_tool],
        llm=llm
    )

    content_writer = Agent(
        role="Content Writer",
        goal="Transform research findings into clear, engaging responses.",
        backstory="You're a skilled writer who excels at making complex information accessible and engaging. "
                  "You maintain accuracy while ensuring the content is easy to understand.",
        allow_delegation=False,
        verbose=True,
        llm=llm
    )

    # Define tasks
    task_research = Task(
        description=f"""Research the following query thoroughly: {query}
        1. Find relevant and up-to-date information.
        2. Verify facts and cross-reference sources.
        3. Include citations for key information.""",
        expected_output="""A concise research summary with:
        - Key findings and facts.
        - Verified information.
        - Relevant citations.""",
        agent=research_analyst
    )

    writing_task = Task(
        description=f"""Create a clear, engaging response about: {query}
        1. Use the research findings to answer the query.
        2. Make the information accessible and interesting.
        3. Include relevant citations.
        4. Keep the tone conversational but informative.""",
        expected_output="""A well-written response that:
        - Directly answers the query.
        - Is easy to understand.
        - Includes source citations.
        - Maintains engagement.""",
        agent=content_writer
    )

    # Define and return the crew
    crew = Crew(
        agents=[research_analyst, content_writer],
        tasks=[task_research, writing_task],
        verbose=True
    )
    
    return crew

def respond(query, chat_history):
    """Generate a response to the user's query."""
    if not query:
        return "Please provide a query.", chat_history
    
    try:
        crew = create_crew(query)
        result = crew.kickoff(inputs={"query": query})
        # Add interaction to chat history
        chat_history.append(("You", query))
        chat_history.append(("Assistant", result))
        return result, chat_history
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        chat_history.append(("You", query))
        chat_history.append(("Assistant", error_message))
        return error_message, chat_history

# Streamlit app
st.set_page_config(page_title="AI Research Assistant", layout="wide")

st.title("AI Research Assistant")
st.markdown("Ask me anything! I'll research and provide detailed, sourced information about any topic.")

# Chat history (use Streamlit session state to persist it)
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input text box for user query
query = st.text_input("Your Question:", placeholder="Ask me anything...")

# Button to submit query
if st.button("Send"):
    if query.strip():
        with st.spinner("Researching and generating response..."):
            result, st.session_state.chat_history = respond(query, st.session_state.chat_history)
        st.text_input("Your Question:", value="", placeholder="Ask me anything...", key="clear_input")

# Display chat history
if st.session_state.chat_history:
    st.markdown("### Chat History:")
    for user, assistant in st.session_state.chat_history:
        if user == "You":
            st.markdown(f"**You:** {assistant}")
        else:
            st.markdown(f"**Assistant:** {assistant}")
