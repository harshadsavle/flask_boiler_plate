import requests

def api_call(**kwrgs):
    try:
        reqArgs = {}
        headers = kwrgs.get("headers")
        reqArgs["headers"] = headers
        url = kwrgs["url"]
        if "data" in kwrgs:
            reqArgs["json"] = kwrgs["data"]
        if "params" in kwrgs:
            reqArgs['params']=kwrgs['params']
        if "files" in kwrgs:
            reqArgs["files"] = kwrgs["files"]
        response = getattr(requests, kwrgs["type"].lower())(url, **reqArgs)

        # Raise error for non-2xx responses
        response.raise_for_status()

        # Handle empty response
        if not response.content:
            return {"success": True, "data": {}}

        # Try parsing JSON, fallback to text
        try:
            data = response.json()
        except ValueError:
            data = response.text

        return {"success": True, "data": data}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out"}
    except requests.exceptions.RequestException as e:
        # All requests errors (connection, too many redirects, etc.)
        return {"success": False, "error": str(e)}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}
