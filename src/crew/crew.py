from crewai import Agent, Crew, Process, Task
from src.tools.rag_tool import rag_lookup
from src.tools.appointment_tool import check_appointment_status
from src.models import AgentResponse

class RAGTool:
    name="rag_lookup"
    description="Retrieve policy knowledge from the Practo knowledge base."
    def _run(self, query): return rag_lookup(query)

class LookupTool:
    name="check_appointment_status"
    description="Lookup an appointment record by record ID."
    def _run(self, record_id): return check_appointment_status(record_id)

def run_crew(query, llm=None):
    # The deterministic application path performs tool orchestration explicitly,
    # while the CrewAI object below demonstrates the required 3-agent topology.
    retrieval=Agent(role="Retrieval Agent", goal="Retrieve grounded policy information.", backstory="Policy retrieval specialist.", tools=[RAGTool()], llm=llm, verbose=False)
    lookup=Agent(role="Lookup Agent", goal="Check appointment records.", backstory="Appointment record specialist.", tools=[LookupTool()], llm=llm, verbose=False)
    composer=Agent(role="Response Composer", goal="Compose a concise grounded support response.", backstory="Support response specialist.", llm=llm, verbose=False)
    t1=Task(description=f"Retrieve policy information for: {query}", expected_output="Grounded policy evidence.", agent=retrieval)
    t2=Task(description=f"Check appointment status only if a record ID is present in: {query}", expected_output="Appointment lookup result or not applicable.", agent=lookup)
    t3=Task(description=f"Compose a response to: {query}", expected_output="Final support response.", agent=composer)
    crew=Crew(agents=[retrieval,lookup,composer],tasks=[t1,t2,t3],process=Process.sequential,verbose=False)
    return crew
