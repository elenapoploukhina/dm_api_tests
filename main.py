"""
curl -X 'POST' \
  'http://185.185.143.231:5051/v1/account' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "login": "lenaivanova_1",
  "email": "lenaivanova_1@mail.ru",
  "password": "123456789"
}'
"""
from pprint import pprint

import requests

# url = 'http://185.185.143.231:5051/v1/account'
# headers = {
#     'accept': '*/*',
#     'Content-Type': 'application/json'
# }
# json = {
#     "login": "lenaivanova_2",
#     "email": "lenaivanova_2@mail.ru",
#     "password": "123456789"
# }
#
# response = requests.post(
#     url=url,
#     headers=headers,
#     json=json
# )

url = 'http://185.185.143.231:5051/v1/account/aaeb8bfe-7e76-4783-9684-f7e4b6c055a9'
headers = {
    'accept': 'text/plain'
}
response = requests.put(
    url=url,
    headers=headers
)

print(response.status_code)
response_json = response.json()
pprint(response_json)
print(f"quantity={response_json['resource']['rating']['quantity']}")
