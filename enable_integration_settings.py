import requests
import json


# INPUT PARAMS
    
org_id = ""
target_name = ""
target_ref = ""


HEADERS = {
        'accept': '*/*',
        'authorization': 'token xxx',  # Replace with your actual API key
}

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
        if name == "github": 
            return id

def enable_pr_check_org(orgId,integrationId):

    # https://snyk.docs.apiary.io/#reference/integrations/integration-settings/update
    url = f'https://api.snyk.io/v1/org/{orgId}/integrations/{integrationId}/settings'

    values ={
        "pullRequestInheritance": "custom",
        "pullRequestTestCodeEnabled": True,
        "pullRequestFailOnAnyCodeIssues": False,
        "pullRequestTestCodeSeverity": "medium",
        "pullRequestTestEnabled": True,
        "pullRequestFailOnAnyVulns": False,
        "pullRequestFailOnlyForHighSeverity": True,
        "pullRequestFailOnlyForIssuesWithFix": True
    }
    print(f"[+] TRYING ORG: {orgId}")
    response = requests.put(url, json=values, headers=HEADERS)
    print(f"RESPONSE CODE for {orgId}: {str(response.status_code)}")


# driver code 
integration_ids = list_integration_id(org_id)
ghe_id = find_id(integration_ids)
enable_pr_check_org(org_id,ghe_id)