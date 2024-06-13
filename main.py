from langchain.prompts.prompt import PromptTemplate
from langchain_openai import AzureChatOpenAI
import os

from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import linkedin_lookup_agent

def ice_break_with(name: str) -> str:
    linkedin_username: str = linkedin_lookup_agent(name= name)
    linkedin_data: str = scrape_linkedin_profile(linkedin_profile_url=linkedin_username, mock=True)

    summary_template: str = """
        given the Linkedin information {information} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them
    """

    summary_prompt_template: PromptTemplate = PromptTemplate(input_variables=["information"],
                                                            template=summary_template)

    llm: AzureChatOpenAI = AzureChatOpenAI(temperature=0, azure_deployment=os.environ["AZURE_DEPLOYMENT_NAME"])

    chain = summary_prompt_template | llm

    result = chain.invoke(input={"information": linkedin_data})

    print(result)

if __name__ == '__main__':
    ice_break_with(name= "Eden Marco")