from langchain.prompts.prompt import PromptTemplate
from langchain_openai import AzureChatOpenAI
import os

from third_parties.linkedin import scrape_linkedin_profile

summary_template: str = """
    given the Linkedin information {information} about a person from I want you to create:
    1. a short summary
    2. two interesting facts about them
"""

summary_prompt_template = PromptTemplate(input_variables=["information"],
                                                         template=summary_template)

llm = AzureChatOpenAI(temperature=0, azure_deployment=os.environ["AZURE_DEPLOYMENT_NAME"])

chain = summary_prompt_template | llm

if __name__ == '__main__':
    linkedin_data = scrape_linkedin_profile("https://www.linkedin.com/in/eden-marco/", mock=True)
    result = chain.invoke(input={"information": linkedin_data})
    print(result)