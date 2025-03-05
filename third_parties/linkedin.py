import os
import requests

def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False) -> str:
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/emarco177/859ec7d786b45d8e3e3f688c6c9139d8/raw/5eaf8e46dc29a98612c8fe0c774123a7a2ac4575/eden-marco-scrapin.json"
        response = requests.get(linkedin_profile_url, timeout=10)
    else:
        #api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
        #headers = {'Authorization': 'Bearer ' + os.environ['PROXYCURL_API_KEY']}
        #params = {'url':linkedin_profile_url}
        #response = requests.get(api_endpoint,
        #                        params=params,
        #                        headers=headers)

        # Now using scrapin.io
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "apikey": os.environ['SCRAPIN_API_KEY'],
            "linkedInUrl": linkedin_profile_url,
        }
        response = requests.get(
            api_endpoint,
            params=params,
            timeout=10,
        )

    data: str = response.json()
    data = {
        key: value
        for key, value in data.items()
        if value not in ([], "", "", None)
        and key not in ["people_also_viewed", "certifications"]
    }
    #if data.get("groups"):
    #    for group_dict in data.get("groups"):
    #        group_dict.pop("profile_pic_url")
    return data

if __name__ == "__main__":
    print(scrape_linkedin_profile("https://www.linkedin.com/in/eden-marco/", mock=False))