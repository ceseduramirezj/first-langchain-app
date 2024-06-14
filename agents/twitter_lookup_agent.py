from langchain_openai import AzureChatOpenAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
import os

from tools.tools import get_profile_url_tavily

def twitter_lookup_agent(name: str) -> str:
    llm: AzureChatOpenAI = AzureChatOpenAI(temperature=0, 
                                           azure_deployment=os.environ["AZURE_DEPLOYMENT_NAME"],)
    
    template = """
        given the name {name_of_person} I want you to find a link to their Twitter profile page, and extract from it their username.
        In your Final answer only the person's username
    """

    prompt_template: PromptTemplate = PromptTemplate(template=template, 
                                                     input_variables=["name_of_person"],)
    
    tools_for_agent: list[Tool] = [Tool(name="Crawl Google 4 Twitter profile page",
                                 func=get_profile_url_tavily,
                                 description="useful for when you need get the Twitter Page URL",)]
    
    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm= llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(input={"input": prompt_template.format_prompt(name_of_person=name)})

    twitter_profile_username: str = result["output"]
    
    return twitter_profile_username

if __name__ == "__main__":
    twitter_username: str = twitter_lookup_agent("Eden Marco")
    print(twitter_username)