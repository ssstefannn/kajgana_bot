import requests
import json
import re

attachment_hash = ""
xf_token = ""
xf_token_pattern = r'<input type="hidden" name="_xfToken" value="([0-9]+,[a-f0-9]+)" />'
attachment_hash_pattern = r'<input type="hidden" name="attachment_hash" value="([a-f0-9]+)" />'

session = requests.Session()

def print_response_info(response):
    print("Info for HTTP request/response:")
    print("URL: ", response.request.url)
    print("Method: ", response.request.method)
    print("Status code: ", response.status_code)
    print("Request headers: ")
    print_http_headers(response.request.headers)
    print("Response headers: ")
    print_http_headers(response.headers)

def print_http_headers(headers):
    print(json.dumps(dict(headers), indent = 4))

def goto_kajgana():
    url = "https://forum.kajgana.com/"
    payload={}
    headers = {}
    response = session.request("GET", url, headers=headers, data=payload)

def login_to_kajgana():
    url = "https://forum.kajgana.com/login/login"
    payload={
        'login': 'steffpotter@gmail.com',
        'password': 'steff1q2w3e4r'
        }
    response = session.request("POST", url, data=payload, allow_redirects=False)

def goto_thread():
    url = "https://forum.kajgana.com/threads/%D0%90%D1%98%D0%B4%D0%B5-%D0%B4%D0%B0-%D0%B8%D0%B7%D0%B1%D1%80%D0%BE%D0%B8%D0%BC%D0%B5-%D0%B4%D0%BE-100-000.54309/page-2545"
    response = session.request("GET", url)
    assert "attachment_hash" in response.text, "Invalid login"
    attachment_hash = re.search(attachment_hash_pattern, response.text).group(1)
    xf_token = re.search(xf_token_pattern, response.text).group(1)

def post_reply(number):
    url = "https://forum.kajgana.com/threads/%D0%90%D1%98%D0%B4%D0%B5-%D0%B4%D0%B0-%D0%B8%D0%B7%D0%B1%D1%80%D0%BE%D0%B8%D0%BC%D0%B5-%D0%B4%D0%BE-100-000.54309/add-reply"
    payload={
        'message_html': '<p>'+number+'</p>',
        'attachment_hash': attachment_hash,
        '_xfToken': xf_token
        }
    response = session.request("POST", url, data=payload)
    print(response.status_code)
    

# goto_kajgana()
login_to_kajgana()
goto_thread()
post_reply(38179)


