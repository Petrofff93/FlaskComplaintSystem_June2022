from werkzeug.exceptions import InternalServerError


def wise_response_status_code_check(resp):
    if resp.status_code == 200:
        resp = resp.json()
        return resp["id"]
    else:
        print(resp)
        raise InternalServerError("Payment provider is not available at the moment")
