from langchain_openai import AzureChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
import os

from tools.tools import get_profile_url_tavily

def linkedin_lookup_agent(name: str) -> str:
    llm: AzureChatOpenAI = AzureChatOpenAI(temperature=0, 
                                           azure_deployment=os.environ["AZURE_DEPLOYMENT_NAME"],)
    
    template: str = """given the full name {name_of_person} I want you to get me a link to their LinkedIn profile page.
    Your answer should contain only a URL."""

    prompt_template: PromptTemplate = PromptTemplate(template=template, 
                                                     input_variables=["name_of_person"],)
    
    tools_for_agent: list[Tool] = [Tool(name="Crawl Google 4 linkedin profile page",
                                 func=get_profile_url_tavily,
                                 description="useful for when you need get the Linkedin Page URL",)]
    
    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm= llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(input={"input": prompt_template.format_prompt(name_of_person=name)})

    linkedin_profile_url: str = result["output"]
    
    return linkedin_profile_url

if __name__ == "__main__":
    linkedin_url: str = linkedin_lookup_agent("Eden Marco")
    print(linkedin_url)