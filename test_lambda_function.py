if __name__ == "__main__":
    from dotenv import load_dotenv
    from lambda_function import lambda_handler

    load_dotenv()

    sample_event = {
        "version": "2.0",
        "routeKey": "$default",
        "rawPath": "/my/path",
        "rawQueryString": "parameter1=value1&parameter1=value2&parameter2=value",
        "cookies": [
            "cookie1",
            "cookie2"
        ],
        "headers": {
            "header1": "value1",
            "header2": "value1,value2"
        },
        "queryStringParameters": {
            "parameter1": "value1,value2",
            "parameter2": "value"
        },
        "requestContext": {
            "accountId": "123456789012",
            "apiId": "api-id",
            "authentication": {
            "clientCert": {
                "clientCertPem": "CERT_CONTENT",
                "subjectDN": "www.example.com",
                "issuerDN": "Example issuer",
                "serialNumber": "a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1:a1",
                "validity": {
                "notBefore": "May 28 12:30:02 2019 GMT",
                "notAfter": "Aug  5 09:36:04 2021 GMT"
                }
            }
            },
            "authorizer": {
            "jwt": {
                "claims": {
                "claim1": "value1",
                "claim2": "value2"
                },
                "scopes": [
                "scope1",
                "scope2"
                ]
            }
            },
            "domainName": "id.execute-api.us-east-1.amazonaws.com",
            "domainPrefix": "id",
            "http": {
            "method": "POST",
            "path": "/my/path",
            "protocol": "HTTP/1.1",
            "sourceIp": "192.0.2.1",
            "userAgent": "agent"
            },
            "requestId": "id",
            "routeKey": "$default",
            "stage": "$default",
            "time": "12/Mar/2020:19:03:58 +0000",
            "timeEpoch": 1583348638390
        },
        "body": "{\"events\":[{\"name\":\"Safe Group\",\"description\":\"Event in Wagga on Wednesday 6th March 2024.\",\"location\":\"Wagga\",\"enddate\":\"2022-08-10T10:25:41.953+00:00\",\"startdate\":\"2022-08-10T10:25:41.953+00:00\"}]}",
        "pathParameters": {
            "parameter1": "value1"
        },
        "isBase64Encoded": False,
        "stageVariables": {
            "stageVariable1": "value1",
            "stageVariable2": "value2"
        }
        }

    result = lambda_handler(
        event=sample_event,
        context=None,
    )

    print(result)
    
    exit(0)
