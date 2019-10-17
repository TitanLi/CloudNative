# 使用OpenStack API
## 取得token
```shell
$ curl -v -s -X POST $OS_AUTH_URL/auth/tokens?nocatalog   -H "Content-Type: application/json"   -d '{ "auth": { "identity": { "methods": ["password"],"password": {"user": {"domain": {"name": "'"$OS_USER_DOMAIN_NAME"'"},"name": "'"$OS_USERNAME"'", "password": "'"$OS_PASSWORD"'"} } }, "scope": { "project": { "domain": { "name": "'"$OS_PROJECT_DOMAIN_NAME"'" }, "name":  "'"$OS_PROJECT_NAME"'" } } }}' \
| python -m json.tool

*   Trying 10.0.1.101...
* Connected to 10.0.1.101 (10.0.1.101) port 35357 (#0)
> POST /v3/auth/tokens?nocatalog HTTP/1.1
> Host: 10.0.1.101:35357
> User-Agent: curl/7.47.0
> Accept: */*
> Content-Type: application/json
> Content-Length: 260
> 
} [260 bytes data]
* upload completely sent off: 260 out of 260 bytes
< HTTP/1.1 201 Created
< Date: Thu, 17 Oct 2019 07:26:00 GMT
< Server: Apache
< Content-Length: 720
< X-Subject-Token: gAAAAABdqBeIVqoDx-0vCvMo8rRqoJKAIjXM4w7-w7cSkL3OOqgZKPydIg2lJgxplZ2CaAzv9KfCPHaCvXTAgR75fsC0UqttWMoBPxWMFqB7FMiOyAoZeUfT0xEjim0U54Q8IVPv8p0aPwB9AhQGi0EcRZwAXKdvFJloJPeifUzTr8dnSyI3KdA
< Vary: X-Auth-Token
< x-openstack-request-id: req-48d96cb7-ec44-415d-aaea-064cd939c36d
< Content-Type: application/json
< 
{ [720 bytes data]
* Connection #0 to host 10.0.1.101 left intact
{
    "token": {
        "audit_ids": [
            "2QKPnAOyQZ-oH6dZowPYXw"
        ],
        "expires_at": "2019-10-18T07:26:00.000000Z",
        "is_domain": false,
        "issued_at": "2019-10-17T07:26:00.000000Z",
        "methods": [
            "password"
        ],
        "project": {
            "domain": {
                "id": "default",
                "name": "Default"
            },
            "id": "ff85695b36394474b2375f1215273760",
            "name": "admin"
        },
        "roles": [
            {
                "id": "ef7f3f56d25044d59126ff4ea492bfcf",
                "name": "heat_stack_owner"
            },
            {
                "id": "4f84ba1836bd40858d978d3d0aadb59f",
                "name": "member"
            },
            {
                "id": "4a207a5ad70c460bba55d4b07f9ab740",
                "name": "reader"
            },
            {
                "id": "b6f41225bedf401390e8c0844091d799",
                "name": "admin"
            }
        ],
        "user": {
            "domain": {
                "id": "default",
                "name": "Default"
            },
            "id": "0920c7fe8d5e4991b8aa25156026bb97",
            "name": "admin",
            "password_expires_at": null
        }
    }
}
```
## Request OpenStack Project API
```shell
$ export OS_TOKEN=gAAAAABdqBeIVqoDx-0vCvMo8rRqoJKAIjXM4w7-w7cSkL3OOqgZKPydIg2lJgxplZ2CaAzv9KfCPHaCvXTAgR75fsC0UqttWMoBPxWMFqB7FMiOyAoZeUfT0xEjim0U54Q8IVPv8p0aPwB9AhQGi0EcRZwAXKdvFJloJPeifUzTr8dnSyI3KdA
$ curl -s -H "X-Auth-Token: $OS_TOKEN" \
http://10.0.1.101:9890/v1.0/vnfds \
| python -m json.tool
```