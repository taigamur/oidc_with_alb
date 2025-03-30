import base64
import json

def handler(event, context):
    headers = event.get("headers", {})

    # IDトークン（JWT）を取得してデコード
    id_token = headers.get("x-amzn-oidc-data")
    if not id_token:
        return {
            "statusCode": 403,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": "No ID token found"
        }

    # JWTのペイロード部分をデコード（base64）
    payload = id_token.split('.')[1] + '=='
    decoded_bytes = base64.urlsafe_b64decode(payload)
    user_info = json.loads(decoded_bytes)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "email": user_info.get("email"),
            "name": user_info.get("name"),
            "sub": user_info.get("sub")
        })
    }
