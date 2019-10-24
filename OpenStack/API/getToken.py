import json
import os
import requests


# 取得token
OS_AUTH_URL = 'http://10.0.1.101:35357'
OS_USER_DOMAIN_NAME = 'Default'
OS_USERNAME = 'admin'
OS_PASSWORD = '2bYiAgHvccZoaDIZyeGhbVlR5ZkQt1LgNV76bp7Q'
OS_PROJECT_DOMAIN_NAME = 'Default'
OS_PROJECT_NAME = 'admin'


def get_token():
    get_token_url = OS_AUTH_URL + '/v3/auth/tokens'
    get_token_body = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "domain": {
                            "name": OS_USER_DOMAIN_NAME
                        },
                        "name": OS_USERNAME,
                        "password": OS_PASSWORD
                    }
                }
            },
            "scope": {
                "project": {
                    "domain": {
                        "name": OS_PROJECT_DOMAIN_NAME
                    },
                    "name": OS_PROJECT_NAME
                }
            }
        }
    }
    get_token_response = requests.post(get_token_url, data=json.dumps(get_token_body))
    print("Get OpenStack token status: " + str(get_token_response.status_code))
    get_token_result = get_token_response.headers['X-Subject-Token']
    print("Token:" + get_token_result)
    return get_token_result

get_token()