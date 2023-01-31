import json,requests

def check_req(challenge_id):
  with requests.Session() as update_session:
    update_session.headers.update({"Authorization": f"Token {token}"})
    flag_result = update_session.get(f"{url}/api/v1/challenges/{challenge_id}/requirements",json='').json()
    try:
      requirements_id = str(flag_result['data']['prerequisites'][0])
      # print(str(challenge_id) + ':'+requirements_id)
      return requirements_id
    except Exception:
      # print(challenge_id)
      return ''

def patch_prereq(challenge_id,prereq_id):
    try:
      with requests.Session() as update_session:
        update_session.headers.update({"Authorization": f"Token {token}"})
        payload = '{"requirements":{"prerequisites":['+prereq_id+']}}'
        flag_result = update_session.patch(f"{url}/api/v1/challenges/{challenge_id}",json=json.loads(payload))
    except Exception:
      print("[e] Something's wrong, nothing changed.")

def make_visible(challenge_id):
  with requests.Session() as update_session:
    update_session.headers.update({"Authorization": f"Token {token}"})
    payload = '{"state":"visible"}'
    flag_result = update_session.patch(f"{url}/api/v1/challenges/{challenge_id}",json=json.loads(payload))

def patch_new_prereq():
  challenge_dict = {}
  cid = 82
  while True:
    try:
      with requests.Session() as check_existence:
        check_existence.headers.update({"Authorization": f"Token {token}"})
        challenge_result = check_existence.get(f"{url}/api/v1/challenges/{cid}",json='').json()
        # print(challenge_result)
        challenge_id = str(challenge_result['data']['id'])
        challenge_name = challenge_result['data']['name']
        challenge_value = str(challenge_result['data']['value'])
        challenge_category = challenge_result['data']['category']
        challenge_prereq = check_req(challenge_id)
        # print(challenge_id+": ['"+challenge_name+"','"+challenge_value+"','"+challenge_category+"','"+challenge_prereq+"'],")
        challenge_dict[challenge_id]=[challenge_name,challenge_value,challenge_category,challenge_prereq]
    except Exception:
      break
    cid+=1

  birth_month1_id = ''
  for key,value in challenge_dict.items():
    if "Birth Month 1" in value:
      if challenge_dict.get(key)[3] == '':
        patch_prereq(key,"79")
        birth_month1_id = key
        make_visible(key)
    elif "XOR Challenge 8" in value:
      if challenge_dict.get(key)[3] == '':
        patch_prereq(key,"35")
        make_visible(key)
    elif "XOR Challenge 7" in value:
      if challenge_dict.get(key)[3] == '':
        patch_prereq(key,"44")
        make_visible(key)
    elif "XOR Challenge 4" in value:
      if challenge_dict.get(key)[3] == '':
        patch_prereq(key,"64")
        make_visible(key)
    elif "Birth Month 2" in value:
      if challenge_dict.get(key)[3] == '':
        patch_prereq(key,"38")
        make_visible(key)
    elif "XOR Challenge 5" in value:
      if challenge_dict.get(key)[3] == '':
        patch_prereq("31",key)
        make_visible (31)
        patch_prereq(key,"22")
        make_visible(key)
    elif "XOR Challenge 6" in value:
      if challenge_dict.get(key)[3] == '':
        patch_prereq("11",key)
        make_visible(11)
        patch_prereq(key,"22")
        make_visible(key)
    elif "XOR Challenge 1" in value:
      if challenge_dict.get(key)[3] == '':
        patch_prereq("80",key)
        make_visible(80)
        patch_prereq(key,"77")
        make_visible(key)
    elif "XOR Challenge 2" in value:
      if challenge_dict.get(key)[3] == '':
        patch_prereq("71",key)
        make_visible(71)
        patch_prereq("47",key)
        make_visible (47)
        patch_prereq(key,"77")
        make_visible(key)
    elif "XOR Challenge 3" in value:
      if challenge_dict.get(key)[3] == '':
        patch_prereq("81",key)
        make_visible(81)
        patch_prereq("12",key)
        make_visible(12)
        patch_prereq(key,birth_month1_id)
        make_visible(key)


#   if check_name("XOR Challenge 3") == True and check_name("Birth Month 1") == True:
#     patch_prereq_name("XOR Challenge 3","Birth Month 1")
#   else:
#     pass


if __name__ == "__main__":
  token = "15c288f2a166e3cef2ebb182a007212e747947aae7ff55fe103bcbb7f1695e2a"
  url = "http://209.114.126.86"
  
  patch_new_prereq()