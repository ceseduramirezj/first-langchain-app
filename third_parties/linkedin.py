import os
import requests

def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False) -> str:
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/fad4d7a87e3e934ad52ba2a968bad9eb45128665/eden-marco.json"
        response = requests.get(linkedin_profile_url, timeout=10)
    else:
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
        headers = {'Authorization': 'Bearer ' + os.environ['PROXYCURL_API_KEY']}
        params = {'url':linkedin_profile_url}
        response = requests.get(api_endpoint,
                                params=params,
                                headers=headers)

    data: str = response.json()
    data = {
        key: value
        for key, value in data.items()
        if value not in ([], "", "", None)
        and key not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")
    return data

if __name__ == "__main__":
    print(scrape_linkedin_profile("https://www.linkedin.com/in/eden-marco/", mock=True))