from typing import Tuple

from langchain.prompts.prompt import PromptTemplate
from langchain_openai import AzureChatOpenAI
import os

from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import scrape_user_tweets
from agents.linkedin_lookup_agent import linkedin_lookup_agent
from agents.twitter_lookup_agent import twitter_lookup_agent

from output_parsers import summary_parser, Summary

def ice_break_with(name: str) -> Tuple[Summary, str] :
    linkedin_username: str = linkedin_lookup_agent(name=name)
    linkedin_data: str = scrape_linkedin_profile(linkedin_profile_url=linkedin_username, mock=True)

    twitter_username: str = twitter_lookup_agent(name=name)
    tweets: list[dict] = scrape_user_tweets(username=twitter_username, mock=True)

    summary_template: str = """
        given the information about a person from linkedin {information},
        and twitter posts {twitter_posts} I want you to create:
        1. a short summary
        2. two interesting facts about them

        Use both information from twitter and Linkedin
        \n{format_instructions}
    """

    summary_prompt_template: PromptTemplate = PromptTemplate(input_variables=["information", "twitter_posts"],
                                                            template=summary_template,
                                                            partial_variables={"format_instructions": summary_parser.get_format_instructions()})

    llm: AzureChatOpenAI = AzureChatOpenAI(temperature=0, azure_deployment=os.environ["AZURE_DEPLOYMENT_NAME"])

    chain = summary_prompt_template | llm | summary_parser

    result: Summary = chain.invoke(input={"information": linkedin_data, "twitter_posts": tweets})

    return result, linkedin_data.get("profile_pic_url")

if __name__ == '__main__':
    ice_break_with(name= "Eden Marco")