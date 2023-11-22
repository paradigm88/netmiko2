import requests

# Define the Check Point server IP, username, and password
server = 'https://YOUR_MANAGEMENT_IP'
username = 'YOUR_USERNAME'
password = 'YOUR_PASSWORD'

# Login to the server
login_response = requests.post(
    f'{server}/web_api/login',
    json={'user': username, 'password': password},
    verify=False
)

# Get the session ID
sid = login_response.json().get('sid')

# Define the headers for the subsequent API calls
headers = {'X-chkp-sid': sid}

# Get all access rulebases
rulebases_response = requests.get(
    f'{server}/web_api/show-access-rulebases',
    headers=headers,
    verify=False
)

# For each rulebase, get all access rules
for rulebase in rulebases_response.json().get('objects'):
    rulebase_name = rulebase.get('name')
    rules_response = requests.get(
        f'{server}/web_api/show-access-rulebase',
        headers=headers,
        json={'name': rulebase_name, 'details-level': 'full'},
        verify=False
    )
    print(f'Rules for {rulebase_name}:')
    for rule in rules_response.json().get('rulebase'):
        print(rule)

# Logout from the server
requests.post(
    f'{server}/web_api/logout',
    headers=headers,
    verify=False
)
