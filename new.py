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
  prerequisites_id = ''
  challenge_id = ''
  flag_challenge = 0
  flag_prereq = 0
  with requests.Session() as check_existence:
    check_existence.headers.update({"Authorization": f"Token {token}"})
    challenge_result = check_existence.get(f"{url}/api/v1/challenges",json='').json()

    for name in challenge_result['data']:
      if challenge_name in name['name']:
        challenge_id = str(name['id'])
      else:
        flag_challenge = 1

    for name in challenge_result['data']:
      if prereq_name in name['name']:
        prerequisites_id = str(name['id'])
      else:
        flag_prereq = 1

  with requests.Session() as update_session:
    update_session.headers.update({"Authorization": f"Token {token}"})
    payload = '{"requirements":{"prerequisites":['+prerequisites_id+']}}'
    flag_result = update_session.patch(f"{url}/api/v1/challenges/{challenge_id}",json=json.loads(payload))
    if flag_result.status_code > 399 and flag_challenge == 1 and flag_prereq == 0:
      print("[e] '"+challenge_name+"' doesn't exist, nothing changed.")
    elif flag_result.status_code > 399 and flag_prereq == 1 and flag_challenge == 0:
      print( "[e] '"+prereq_name+"' doesn't exist, prerequisites not updated")
    elif flag_result.status_code > 399 and flag_challenge == 1 and flag_prereq == 1:
      print("[e] Neither '"+challenge_name+"' and '"+prereq_name+"' esixts, nothing changed.")
    else:
      print("[e] Something's wrong, nothing changed.")

def patch_prereq_id(challenge_name,prereq_id):
  challenge_id = ''
  flag_challenge = 0
  with requests.Session() as check_existence:
    check_existence.headers.update({"Authorization": f"Token {token}"})
    challenge_result = check_existence.get(f"{url}/api/v1/challenges",json='').json()

    for name in challenge_result['data']:
      if challenge_name in name['name']:
        challenge_id = str(name['id'])
      else:
        flag_challenge = 1

  with requests.Session() as update_session:
    update_session.headers.update({"Authorization": f"Token {token}"})
    payload = '{"requirements":{"prerequisites":['+prereq_id+']}}'
    flag_result = update_session.patch(f"{url}/api/v1/challenges/{challenge_id}",json=json.loads(payload))
    if flag_result.status_code > 399 and flag_challenge == 1:
      print("[e] '"+challenge_name+"' doesn\'t exist, nothing changed.")
    else:
      print("[e] Something's wrong, nothing changed.")

def patch_prereq_reverseid(challenge_id,prereq_name):
  prerequisites_id = ''
  flag_prereq = 0
  with requests.Session() as check_existence:
    check_existence.headers.update({"Authorization": f"Token {token}"})
    challenge_result = check_existence.get(f"{url}/api/v1/challenges",json='').json()

    for name in challenge_result['data']:
      if prereq_name in name['name']:
        prerequisites_id = str(name['id'])
      else:
        flag_prereq = 1

  with requests.Session() as update_session:
    update_session.headers.update({"Authorization": f"Token {token}"})
    payload = '{"requirements":{"prerequisites":['+prerequisites_id+']}}'
    flag_result = update_session.patch(f"{url}/api/v1/challenges/{challenge_id}",json=json.loads(payload))
    if flag_prereq == 1:
      print("[e] '"+prereq_name+"' doesn\'t exist, nothing changed.")
    else:
      print("[e] Something's wrong, nothing changed.")



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

def make_visible(challenge_id):
  with requests.Session() as update_session:
    update_session.headers.update({"Authorization": f"Token {token}"})
    payload = '{"state":"visible"}'
    flag_result = update_session.patch(f"{url}/api/v1/challenges/{challenge_id}",json=json.loads(payload))





def check_name(challenge_name):
  with requests.Session() as check_existence:
    check_existence.headers.update({"Authorization": f"Token {token}"})
    challenge_result = check_existence.get(f"{url}/api/v1/challenges",json='').json()

    for name in challenge_result['data']:
      if challenge_name in name['name']:
        return True

def patch_new_prereq():
  if check_name("XOR Challenge 8") == True:
    patch_prereq_id("XOR Challenge 8","35")
  else:
    pass

  if check_name("XOR Challenge 7") == True:
    patch_prereq_id("XOR Challenge 7","44")
  else:
    pass

  if check_name("XOR Challenge 4") == True:
    patch_prereq_id("XOR Challenge 4","64")
  else:
    pass

  if check_name("Birth Month 2") == True:
    patch_prereq_id("Birth Month 2","38")
  else:
    pass

### 31 Linux 5 must be hidden at the beginning.
  if check_name("XOR Challenge 5") == True:
    patch_prereq_reverseid("31","XOR Challenge 5")
    make_visible(31)
  else:
    pass

  if check_name("XOR Challenge 5") == True:
    patch_prereq_id("XOR Challenge 5","22")
  else:
    pass

  if check_name("XOR Challenge 6") == True:
    patch_prereq_reverseid("11","XOR Challenge 6")
    make_visible(11)
  else:
    pass

  if check_name("XOR Challenge 6") == True:
    patch_prereq_id("XOR Challenge 6","22")
  else:
    pass

  if check_name("Break Room 1") == True and check_name("XOR Challenge 1") == True:
    patch_prereq_name("Break Room 1","XOR Challenge 1")
  else:
    pass

  if check_name("XOR Challenge 2") == True:
    patch_prereq_reverseid("71","XOR Challenge 2")
    make_visible(71)
  else:
    pass

  if check_name("XOR Challenge 2") == True:
    patch_prereq_reverseid("47","XOR Challenge 2")
    make_visible(47)
  else:
    pass

  if check_name("Break Room 2") == True and check_name("XOR Challenge 3") == True:
    patch_prereq("Break Room 2","XOR Challenge 3")
  else:
    pass

  if check_name("XOR Challenge 3") == True:
    patch_prereq("12","XOR Challenge 3")
    make_visible(12)
  else:
    pass

  if check_name("XOR Challenge 3") == True and check_name("Birth Month 1") == True:
    patch_prereq_name("XOR Challenge 3","Birth Month 1")
  else:
    pass

  if check_name("Birth Month 1") == True and check_name("Coordination Practice") == True:
    patch_prereq("Birth Month 1", "Coordination Practice")
  else:
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

  patch_new_prereq()
  # 
  # patch_prereq()
  # patch_prereq()
  # patch_prereq()
  # patch_prereq()
  # patch_prereq()
  # patch_prereq()
  # patch_prereq()
  # save_id()
  # for n in range(1,80):
  #   check_req(n)
  