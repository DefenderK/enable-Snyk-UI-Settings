# copyright (c) Endeavour drinks and Prash Lallbeeharry
import requests


# INPUT PARAMS
    
org_id = ""
target_name = ""
target_ref = ""


HEADERS = {
        'accept': '*/*',
        'authorization': 'token xxx',  # Replace with your actual API key
}

def get_target_id(org_id,target_name):
    # Make the first API request to get target IDs
    api_url = f"https://api.snyk.io/rest/orgs/{org_id}/targets"
    api_params = {
        'version': '2023-06-19~beta',
        'displayName': target_name,
        "origin": "azure-repos"
    }


    response = requests.get(api_url, params=api_params, headers=HEADERS)
    response_data = response.json()

    # Extract the target ID from the response
    return response_data.get('data', [])[0].get('id')

def get_project_from_target_id(org_id,target_id,target_ref):
    api_url_projects = f"https://api.snyk.io/rest/orgs/{org_id}/projects"
    api_params_projects = {
        'target_id': target_id,
        'version': '2024-01-04',
        'target_reference': f"{target_ref}",
        'limit': 100
    }

    project_ids_response = requests.get(api_url_projects, params=api_params_projects, headers=HEADERS)
    project_ids_data = project_ids_response.json()


    # Extract and print project IDs
    return [project.get('id') for project in project_ids_data.get('data', [])]

def enable_pr_check(orgId,projectId):
    
    url = f'https://api.snyk.io/v1/org/{orgId}/project/{projectId}/settings'

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
    print(f"[+] TRYING PROJECT: {projectId}")
    response = requests.put(url, json=values, headers=HEADERS)
    print(f"RESPONSE CODE for {projectId}: {str(response.status_code)}")



# driver code 
    
targetID = get_target_id(org_id,target_name)
projectIDs = get_project_from_target_id(org_id,targetID,target_ref)

for project in projectIDs:
    enable_pr_check(org_id,project)

