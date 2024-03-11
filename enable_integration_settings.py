import requests
import json


# INPUT PARAMS
    
org_id = ""


HEADERS = {
        'accept': '*/*',
        'authorization': 'token 01959aaa-f781-4dec-b29b-587610de46b3',  # Replace with your actual API key
}

def get_org_ids():
    ids = []
    # Make the first API request to get org IDs
    api_url = f"https://api.snyk.io/rest/orgs"
    api_params = {
        'version': '2024-01-04~experimental',
        'limit': '100'
    }


    response = requests.get(api_url, params=api_params, headers=HEADERS)
    response_data = response.json()
    orgs = response_data["data"]
    

    for org in orgs:
        id = org["id"]
        # response_data.get('data', [])[i].get('id')
        # slug = response_data.get('data', [])[i].get('attributes').get('slug')
        # for org_name in org_name_list: 
        #     if slug == org_name: 
        # id = response_data.get('data', [])[i].get('id')
        ids.append(id)
    
    print(ids)
    return ids 
def list_integration_id(orgId):
    # https://snyk.docs.apiary.io/#reference/integrations/integrations/list
    url = f'https://api.snyk.io/v1/org/{orgId}/integrations'

    response = requests.get(url, headers=HEADERS)
    response_byte_str = response.content.decode('utf-8')
    response_json = json.loads(response_byte_str)
    return response_json
# 
def find_id(integration_ids):
    print(integration_ids)
    for name, id in integration_ids.items(): 
        if name == "github-enterprise": 
            return id

def enable_pr_check_org(orgId,integrationId):

    # https://snyk.docs.apiary.io/#reference/integrations/integration-settings/update
    url = f'https://api.snyk.io/v1/org/{orgId}/integrations/{integrationId}/settings'

    values ={
        "pullRequestInheritance": "custom",
        "pullRequestTestCodeEnabled": True,
        "pullRequestFailOnAnyCodeIssues": False,
        "pullRequestTestCodeSeverity": "high",
        "pullRequestTestEnabled": True,
        "pullRequestFailOnAnyVulns": False,
        "pullRequestFailOnlyForHighSeverity": True,
        "pullRequestFailOnlyForIssuesWithFix": True
    }
    print(f"[+] TRYING ORG: {orgId}")
    response = requests.put(url, json=values, headers=HEADERS)
    print(f"RESPONSE CODE for {orgId}: {str(response.status_code)}")


# driver code 
ids_ = get_org_ids()

for id in ids_: 
    integration_ids = list_integration_id(id)
    ghe_id = find_id(integration_ids)
    enable_pr_check_org(id,ghe_id)