# importing the requests library
import requests
import re

def login_to_kajgana(username, password):
    URL = "https://forum.kajgana.com/login/login"
    login_form_data = {
        'login':username,
        'password':password
    }
    headers = {
        # 'Content-Type':'application/x-www-form-urlencoded',
        # 'Content-Length':'',
        # 'Host':'',
        # 'User-Agent':'PostmanRuntime/7.31.1',
        # 'Accept':'*/*',
        # 'Accept-Encoding':'gzip,deflate,br',
        # 'Connection':'keep-alive'
    }
    response = requests.request(
        "POST", 
        URL, 
        data = login_form_data, 
        headers = headers)
    data = response.text
    f = open("test.html", "wb")
    f.write(data.encode('ascii', 'ignore'))
    f.close()


    

def go_to_thread(url):
    URL = url
    r = requests.get(url = URL)
    data = r.text
    assert "attachment_hash" in data, "Invalid login"
    occurences = re.findall(r'<input type="hidden" name="attachment_hash" value="([a-f0-9]+)" />', data)
    print(occurences)

login_to_kajgana("Ihanoidwhimdo", "steff1q2w3e4r")
go_to_thread("https://forum.kajgana.com/threads/%D0%90%D1%98%D0%B4%D0%B5-%D0%B4%D0%B0-%D0%B8%D0%B7%D0%B1%D1%80%D0%BE%D0%B8%D0%BC%D0%B5-%D0%B4%D0%BE-100-000.54309/page-2545")