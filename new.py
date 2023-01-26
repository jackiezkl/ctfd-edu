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



def patch_prereq(challenge_name,prereq_name):
  with requests.Session() as check_existence:
    check_existence.headers.update({"Authorization": f"Token {token}"})
    challenge_result = check_existence.get(f"{url}/api/v1/challenges",json='').json()

    for name in challenge_result['data']:
      if challenge_name in name['name']:
        challenge_id = str(name['id'])

    for name in challenge_result['data']:
      if prereq_name in name['name']:
        prerequisites_id = str(name['id'])
  print(challenge_id)
  print(prerequisites_id)
  with requests.Session() as update_session:
    update_session.headers.update({"Authorization": f"Token {token}"})
    payload = '{"requirements":{"prerequisites":['+prerequisites_id+']}}'
    flag_result = update_session.patch(f"{url}/api/v1/challenges/{challenge_id}",json=json.loads(payload))
    if flag_result.status_code > 399:
      print('[e] Challenge '+challenge_id+' prerequisites not updated')

def save_id():
  for n in range(0,150):
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
  token = "e1e0c697d7ed975182df847918d0e0fee4c99b48d0eac461e3a2bcfdb3e72e3c"
  url = "http://209.114.126.86"

  # patch_prereq("XOR Challenge 8","Windows Basics 1")
  # patch_prereq("XOR Challenge 7","In need of ...")
  # patch_prereq()
  # patch_prereq()
  # patch_prereq()
  # patch_prereq()
  # patch_prereq()
  # patch_prereq()
  # patch_prereq()
  # patch_prereq()
  # patch_prereq()
  # patch_prereq()
  # patch_prereq()
  # patch_prereq()
  # patch_prereq()
  # patch_prereq()
  # patch_prereq()
  # patch_prereq()
  # patch_prereq()
  # patch_prereq()
  # patch_prereq()
  # patch_prereq()
  save_id()