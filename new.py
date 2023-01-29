import requests,json

def save_id():
  for n in range(1,82):
    try:
      with requests.Session() as check_existence:
        check_existence.headers.update({"Authorization": f"Token {token}"})
        challenge_result = check_existence.get(f"{url}/api/v1/challenges/{n}",json='').json()
        # print(challenge_result)
        challenge_id = str(challenge_result['data']['id'])
        challenge_name = challenge_result['data']['name']
        challenge_value = str(challenge_result['data']['value'])
        challenge_category = challenge_result['data']['category']
        print(challenge_id+": ['"+challenge_name+"','"+challenge_value+"','"+challenge_category+"'],")
    except Exception:
      pass


# def check_id():
#   count = 0
#   with requests.Session() as check_existence:
#     check_existence.headers.update({"Authorization": f"Token {token}"})
#     challenge_result = check_existence.get(f"{url}/api/v1/challenges",json='').json()

#     for name in challenge_result['data']:
#       if "XOR Challenge 8" in name['name']:
#         challenge_id = name['id']
#         check_req(challenge_id)
#       elif "Birth Month" in name['name']:
#         challenge_id = name['id']
#         print(challenge_id)
#         check_req(challenge_id)



def check_req(challenge_id):
  with requests.Session() as update_session:
    update_session.headers.update({"Authorization": f"Token {token}"})
    flag_result = update_session.get(f"{url}/api/v1/challenges/{challenge_id}/requirements",json='').json()
    try:
      requirements_id = str(flag_result['data']['prerequisites'][0])
      print(str(challenge_id) + ':'+requirements_id)
    except Exception:
      print(challenge_id)
      pass

if __name__ == "__main__":
  token = "15c288f2a166e3cef2ebb182a007212e747947aae7ff55fe103bcbb7f1695e2a"
  url = "http://209.114.126.86"

  # save_id()
  for n in range(1,80):
    check_req(n)
  