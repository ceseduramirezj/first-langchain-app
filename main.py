from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
import os

information: str = """
Alexander Volkanovski (born 29 September 1988) is an Australian professional mixed martial artist. He currently competes in the Featherweight division of the Ultimate Fighting Championship (UFC), where he is the former UFC Featherweight Champion. He is also a former Australian Fighting Championship (AFC) Featherweight champion. Prior to his UFC debut, Volkanovski competed as a professional boxer in 2015. As of 20 February 2024, he is #1 in the UFC featherweight rankings[7] and as of 16 April 2024, he is #7 in the UFC men's pound-for-pound rankings.

Volkanovski was born on 29 September 1988, in Wollongong, New South Wales. Alex began training in Greco-Roman wrestling at an early age and won a national title twice at the age of 12. He decided to give up wrestling at the age of 14 and instead focused on a career in rugby league as a front rower. Volkanovski attended Lake Illawarra High School throughout his teenage years and worked as a concreter after graduation.

Volkanovski then decided to quit rugby league at 23 years of age to pursue a professional career in Mixed Martial Arts in the latter half of 2011.[20] He claims to have watched Ultimate Fighting Championship events since childhood and would often rent UFC VHS tapes from Blockbuster as well as purchase UFC pay per views from 14 years of age.
"""

summary_template: str = """
    given the information {information} about a person from I want you to create:
    1. a short summary
    2. two interesting facts about them
"""

summary_prompt_template = PromptTemplate(input_variables=["information"],
                                                         template=summary_template)

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

chain = summary_prompt_template | llm

if __name__ == '__main__':
    result = chain.invoke(input={"information": information})
    print(result)