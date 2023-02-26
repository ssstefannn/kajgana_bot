import requests
import json
import re
import os
import sys
import time
import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()

attachment_hash = ""
xf_token = ""
xf_token_pattern = r'<input type="hidden" name="_xfToken" value="([0-9]+,[a-f0-9]+)" />'
attachment_hash_pattern = r'<input type="hidden" name="attachment_hash" value="([a-f0-9]+)" />'
five_digit_number_pattern = r'(\d)\D*(\d)\D*(\d)\D*(\d)\D*(\d)'
assert\
    len(sys.argv) == 2 and\
    int(sys.argv[1]) > 0,\
    "Usage: python bot.py <last_number_posted_on_the_thread>"
current_number = int(sys.argv[1])
seed_value = int(current_number/10000) * 10000 + int(current_number/1000)%10 * 1000
number_to_post = 0
last_number_posted_by_me = 0
response = None

session = requests.Session()
session.headers.update({
    'User-Agent': \
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
        AppleWebKit/537.36 (KHTML, like Gecko)\
        Chrome/110.0.0.0 Safari/537.36'
    })

def print_response_info(response):
    print("Info for HTTP request/response:")
    print("URL: ", response.request.url)
    print("Method: ", response.request.method)
    print("Status code: ", response.status_code)
    print("Request headers: ")
    print_http_headers(response.request.headers)
    print("Request body: ")
    print(response.request.body)
    print("Response headers: ")
    print_http_headers(response.headers)

def print_http_headers(headers):
    print(json.dumps(dict(headers), indent = 4))

def goto_kajgana():
    url = "https://forum.kajgana.com/"
    payload={}
    headers = {}
    session.request("GET", url, headers=headers, data=payload)

def login_to_kajgana():
    url = "https://forum.kajgana.com/login/login"
    username = os.getenv('KAJGANA_USERNAME')
    password = os.getenv('KAJGANA_PASSWORD')
    assert username != None and password != None,\
        "Missing username/password.\n\
            Please follow the steps from the README file in order to fill username and password"
    payload={
        'login': username,
        'password': password
        }
    session.request("POST", url, data=payload)

def synchronize():
    global attachment_hash
    global xf_token
    global current_number
    global last_number_posted_by_me
    global number_to_post
    global seed_value
    url = "https://forum.kajgana.com/threads/%D0%90%D1%98%D0%B4%D0%B5-%D0%B4%D0%B0-%D0%B8%D0%B7%D0%B1%D1%80%D0%BE%D0%B8%D0%BC%D0%B5-%D0%B4%D0%BE-100-000.54309/page-9999"
    response = session.request("GET", url)
    assert "attachment_hash" in response.text, "Invalid login"
    attachment_hash = re.search(attachment_hash_pattern, response.text).group(1)
    xf_token = re.search(xf_token_pattern, response.text).group(1)
    numbers = []
    soup = BeautifulSoup(response.text, 'html.parser')
    divs = soup.find_all('div', class_='bbWrapper')
    for div in divs:
        tuples = re.findall(five_digit_number_pattern, div.text)
        for tuple in tuples:
            number = int(''.join(tuple))
            if number > seed_value and number < seed_value + 1000:
                numbers.append(number)
    numbers.sort()
    assert current_number >= numbers[-1] - 5,\
          f"Couldn't parse html, the current number is {current_number} the html numbers are {numbers} " 
    current_number = numbers[-1]
    number_to_post = current_number + 1


def post_reply():
    global last_number_posted_by_me
    global number_to_post
    url = "https://forum.kajgana.com/threads/%D0%90%D1%98%D0%B4%D0%B5-%D0%B4%D0%B0-%D0%B8%D0%B7%D0%B1%D1%80%D0%BE%D0%B8%D0%BC%D0%B5-%D0%B4%D0%BE-100-000.54309/add-reply"
    payload={
        'message_html': f'<p>{number_to_post}</p>',
        'attachment_hash': attachment_hash,
        '_xfToken': xf_token
        }
    session.request("POST", url, data=payload)
    last_number_posted_by_me = number_to_post


def check_if_should_post():
    synchronize()
    return last_number_posted_by_me != current_number

login_to_kajgana()
while True:
    should_post = check_if_should_post()
    if should_post:
        post_reply()
        print(f"{datetime.datetime.now()}: posted the number {last_number_posted_by_me}!")
    time.sleep(60)



