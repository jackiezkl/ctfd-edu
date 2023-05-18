import requests,json

# this program checks all challenges and list their id, name, value, category, and prerequisites
def check_req(challenge_id):
  with requests.Session() as update_session:
    update_session.headers.update({"Authorization": f"Token {token}"})
    flag_result = update_session.get(f"{url}/api/v1/challenges/{challenge_id}/requirements",json='').json()
    try:
      requirements_id = str(flag_result['data']['prerequisites'][0])
      return requirements_id
    except Exception:
      return ''



if __name__ == "__main__":
  token = "15c288f2a166e3cef2ebb182a007212e747947aae7ff55fe103bcbb7f1695e2a"
  url = "http://209.114.126.86"
  replace_text = ''
  challenge_dict = {}

  cid = 1
  while True:
    try:
      with requests.Session() as check_existence:
        check_existence.headers.update({"Authorization": f"Token {token}"})
        challenge_result = check_existence.get(f"{url}/api/v1/challenges/{cid}",json='').json()

        challenge_name = challenge_result['data']['name']
        challenge_value = str(challenge_result['data']['value'])
        challenge_category = challenge_result['data']['category']
        challenge_prereq = check_req(cid)
        # challenge_dict.update({cid:[challenge_name,challenge_value,challenge_category]})
        print(challenge_id+": ['"+challenge_name+"','"+challenge_value+"','"+challenge_category+"','"+challenge_prereq+"'],")
    except Exception:
      break
    cid+=1

  # for i in challenge_dict:
  #   replace_text = replace_text+f"{i}: {challenge_dict[i]},\n"
  # print(replace_text)
