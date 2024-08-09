import requests
import json


# INPUT PARAMS
    
BASE_URL = "https://api.snyk.io"
SNYK_TOKEN = ""

HEADERS = {
        'accept': '*/*',
        'authorization': f'token {SNYK_TOKEN}',  # Replace with your actual API key
}

def get_orgs_page(next_url):

    # Add "next url" on to the BASE URL
    url = BASE_URL + next_url

    api_params = {
        'version': '2024-01-04~experimental',
        'limit': '100'
    }

    # return requests.request("GET", url, headers=headers)
    return requests.get(url, params=api_params, headers=HEADERS)

def get_org_data():
    org_data = []
    # Make the first API request to get org IDs
    next_url = f"/rest/orgs"
    

    while next_url is not None:
        res = get_orgs_page(next_url).json()

        if 'links' in res and 'next' in res['links']:
            next_url = res['links']['next']
        else:
            next_url = None

        # add to list
        if 'data' in res:
            org_data.extend(res['data'])

    return org_data 

def get_org_ids(orgs):
    ids = []
    for org in orgs:
        id = org["id"]
        ids.append(id)
    
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
        if name == "azure-repos": 
            return id

def enable_pr_check_org(orgId,integrationId):

    # https://snyk.docs.apiary.io/#reference/integrations/integration-settings/update
    url = f'https://api.snyk.io/v1/org/{orgId}/integrations/{integrationId}/settings'

    values ={
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
org_data_ = get_org_data()
ids_ = get_org_ids(org_data_)

for id in ids_: 
    integration_ids = list_integration_id(id)
    ghe_id = find_id(integration_ids)
    enable_pr_check_org(id,ghe_id)
