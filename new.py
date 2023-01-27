import requests,json

def check_requirements():
  with requests.Session() as check_existence:
    check_existence.headers.update({"Authorization": f"Token {token}"})
    challenge_result = check_existence.get(f"{url}/api/v1/challenges",json='').json()

    for name in challenge_result['data']:
      if "XOR Challenge 7" in name['name']:
        challenge_id = str(name['id'])

    for name in challenge_result['data']:
      if "XOR Challenge 6" in name['name']:
        prerequisites_id = str(name['id'])

  update_prereq(challenge_id,prerequisites_id)

def update_prereq(challenge_id,prerequisites_id):
  with requests.Session() as update_session:
    update_session.headers.update({"Authorization": f"Token {token}"})
    payload = '{"requirements":{"prerequisites":['+prerequisites_id+']}}'
    flag_result = update_session.patch(f"{url}/api/v1/challenges/{challenge_id}",json=json.loads(payload))
    if flag_result.status_code > 399:
      print('[e] Challenge '+challenge_id+' prerequisites not updated')



def patch_prereq_name(challenge_name,prereq_name):
  with requests.Session() as check_existence:
    check_existence.headers.update({"Authorization": f"Token {token}"})
    challenge_result = check_existence.get(f"{url}/api/v1/challenges",json='').json()

    for name in challenge_result['data']:
      if challenge_name in name['name']:
        challenge_id = str(name['id'])

    for name in challenge_result['data']:
      if prereq_name in name['name']:
        prerequisites_id = str(name['id'])

  with requests.Session() as update_session:
    update_session.headers.update({"Authorization": f"Token {token}"})
    payload = '{"requirements":{"prerequisites":['+prerequisites_id+']}}'
    flag_result = update_session.patch(f"{url}/api/v1/challenges/{challenge_id}",json=json.loads(payload))
    if flag_result.status_code > 399:
      print('[e] Challenge '+challenge_id+' prerequisites not updated')

def patch_prereq_id(challenge_name,prereq_id):
  with requests.Session() as check_existence:
    check_existence.headers.update({"Authorization": f"Token {token}"})
    challenge_result = check_existence.get(f"{url}/api/v1/challenges",json='').json()

    for name in challenge_result['data']:
      if challenge_name in name['name']:
        challenge_id = str(name['id'])

  with requests.Session() as update_session:
    update_session.headers.update({"Authorization": f"Token {token}"})
    payload = '{"requirements":{"prerequisites":['+prereq_id+']}}'
    flag_result = update_session.patch(f"{url}/api/v1/challenges/{challenge_id}",json=json.loads(payload))
    if flag_result.status_code > 399:
      print('[e] Challenge '+challenge_id+' prerequisites not updated')

def patch_prereq_reverseid(challenge_id,prereq_name):
  with requests.Session() as check_existence:
    check_existence.headers.update({"Authorization": f"Token {token}"})
    challenge_result = check_existence.get(f"{url}/api/v1/challenges",json='').json()

    for name in challenge_result['data']:
      if prereq_name in name['name']:
        prerequisites_id = str(name['id'])

  with requests.Session() as update_session:
    update_session.headers.update({"Authorization": f"Token {token}"})
    payload = '{"requirements":{"prerequisites":['+prerequisites_id+']}}'
    flag_result = update_session.patch(f"{url}/api/v1/challenges/{challenge_id}",json=json.loads(payload))
    if flag_result.status_code > 399:
      print('[e] Challenge '+challenge_id+' prerequisites not updated')



def save_id():
  for n in range(79,150):
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

def update_visibility(challenge_id):
  with requests.Session() as update_session:
    update_session.headers.update({"Authorization": f"Token {token}"})
    payload = '{"state":"visible"}'
    flag_result = update_session.patch(f"{url}/api/v1/challenges/{challenge_id}",json=json.loads(payload))




def check_id():
  count = 0
  with requests.Session() as check_existence:
    check_existence.headers.update({"Authorization": f"Token {token}"})
    challenge_result = check_existence.get(f"{url}/api/v1/challenges",json='').json()

    for name in challenge_result['data']:
      if "XOR Challenge 8" in name['name']:
        challenge_id = name['id']
        check_req(challenge_id)
      elif "Birth Month" in name['name']:
        challenge_id = name['id']
        print(challenge_id)
        check_req(challenge_id)



def check_req(challenge_id):
  with requests.Session() as update_session:
    update_session.headers.update({"Authorization": f"Token {token}"})
    flag_result = update_session.get(f"{url}/api/v1/challenges/{challenge_id}/requirements",json='').json()
    try:
      requirements_id = str(flag_result['data']['prerequisites'][0])
      print(str(challenge_id) + ':'+requirements_id)
    except Exception:
      pass

if __name__ == "__main__":
  token = "15c288f2a166e3cef2ebb182a007212e747947aae7ff55fe103bcbb7f1695e2a"
  url = "http://209.114.126.86"

  # patch_prereq_id("XOR Challenge 8","35")
  # patch_prereq_id("XOR Challenge 7","44")
  # patch_prereq_id("XOR Challenge 4"，“64")
  # patch_prereq("Birth Month 2","38")
  # ### Linux 5 must be hidden at the beginning.
  # patch_prereq_reverseid("31","XOR Challenge 5")
  # update_visibility(31)
  # patch_prereq_id("XOR Challenge 5","22")
  # patch_prereq_reverseid("11","XOR Challenge 6")
  # update_visibility(11)
  # patch_prereq_id("XOR Challenge 6","22")
  # patch_prereq("Break Room 1","XOR Challenge 1")
  # patch_prereq("Firewall 5","XOR Challenge 2")
  # patch_prereq("Name the Attack 3","XOR Challenge 2")
  # patch_prereq("Break Room 2","XOR Challenge 3")
  # patch_prereq("Vulnerability Test,"XOR Challenge 3"")
  # patch_prereq("XOR Challenge 3","Birth Month 1")
  # patch_prereq("Birth Month 1", "Coordination using Zoom Chat")
  # patch_prereq()
  # patch_prereq()
  # patch_prereq()
  # patch_prereq()
  # patch_prereq()
  # patch_prereq()
  # patch_prereq()
  save_id()