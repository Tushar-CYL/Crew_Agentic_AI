import streamlit as st
from crewai import Agent, Crew, Task, Process, LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
# from crewai.llms import LLM

load_dotenv()

topic = "medical industry using generative AI"

llm = LLM(model="gemini/gemini-1.5-pro-latest", temperature=0.7)

search_tool = SerperDevTool(n=10)

# Define YourCrewName class
class YourCrewName:
    def agent_one(self) -> Agent:
        return Agent(
            role="Data Analyst",
            goal="Analyze data trends in the market",
            backstory="An experienced data analyst with a background in economics",
            allow_delegation=False,
            verbose=True,
            tools=[search_tool],
            llm=llm
        )

    def agent_two(self) -> Agent:
        return Agent(
            role="Market Researcher",
            goal="Gather information on market dynamics",
            backstory="A diligent researcher with a keen eye for detail",
            allow_delegation=False,
            verbose=True,
            tools=[search_tool],
            llm=llm
        )

    def task_one(self) -> Task:
        return Task(
            description="Collect recent market data and identify trends.",
            expected_output="A report summarizing key trends in the market.",
            agent=self.agent_one()
        )

    def task_two(self) -> Task:
        return Task(
            description="Research factors affecting market dynamics.",
            expected_output="An analysis of factors influencing the market.",
            agent=self.agent_two()
        )

    def crew(self) -> Crew:
        return Crew(
            agents=[self.agent_one(), self.agent_two()],
            tasks=[self.task_one(), self.task_two()],
            process=Process.sequential,
            verbose=True
        )

# Streamlit App
st.title("Your Crew Management System")

crew_instance = YourCrewName()

# Display Agents
st.header("Agents")
agent_one = crew_instance.agent_one()
st.subheader("Agent One")
st.write(f"**Role:** {agent_one.role}")
st.write(f"**Goal:** {agent_one.goal}")
st.write(f"**Backstory:** {agent_one.backstory}")
st.write(f"**Tool Used:** SerperDevTool (Search Results Limit: 10)")

agent_two = crew_instance.agent_two()
st.subheader("Agent Two")
st.write(f"**Role:** {agent_two.role}")
st.write(f"**Goal:** {agent_two.goal}")
st.write(f"**Backstory:** {agent_two.backstory}")

# Display Tasks
st.header("Tasks")
task_one = crew_instance.task_one()
st.subheader("Task One")
st.write(f"**Description:** {task_one.description}")
st.write(f"**Expected Output:** {task_one.expected_output}")

if st.button("Run Task One"):
    st.write("Task One is being executed...")
    st.write(f"Searching for topic: {topic}")
    search_results = search_tool.search(topic)
    st.write(f"Search Results: {search_results}")


task_two = crew_instance.task_two()
st.subheader("Task Two")
st.write(f"**Description:** {task_two.description}")
st.write(f"**Expected Output:** {task_two.expected_output}")

if st.button("Run Task Two"):
    st.write("Task Two is being executed...")
    # Execute task_two logic if available

# Display Crew
st.header("Crew")
crew = crew_instance.crew()
st.write(f"**Process:** {crew.process}")
st.write(f"**Verbose Mode:** {crew.verbose}")

if st.button("Run Crew"):
    st.write("Executing the Crew...")
    # Execute crew logic if available
