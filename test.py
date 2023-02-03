import os,requests,json

def patch_autoscoreboard_js(parent_path):
  relative_path = "CTFd/CTFd/plugins/ctfd-auto-scoreboard/assets/auto-scoreboard.js"
  dst_path = os.path.join(parent_path, relative_path)
  if os.path.exists(dst_path) == False:
    print("[e] Couldn't find the *auto-scoreboard.js* to work with.")
    exit()

  start_line = 0
  end_line = 0

  with open(dst_path, 'r') as jsfile: 
    lines = jsfile.readlines()
    for i,line in enumerate(lines):
      if line.startswith("    78: ['Introduction','5','Introduction']"):
        start_line = i
      elif line.startswith("var getUserSolvesHistogram"):
        end_line = i

  print(start_line)
  print(end_line)


if __name__ == "__main__":
  token = "15c288f2a166e3cef2ebb182a007212e747947aae7ff55fe103bcbb7f1695e2a"
  url = "http://209.114.126.86"

  current_path=os.getcwd()
  parent_path = os.path.dirname(current_path)+"/"

  challenge_dict = {}
  replace_text = ""
  cid = 79
  while True:
    try:
      with requests.Session() as check_existence:
        check_existence.headers.update({"Authorization": f"Token {token}"})
        challenge_result = check_existence.get(f"{url}/api/v1/challenges/{cid}",json='').json()

        challenge_name = challenge_result['data']['name']
        challenge_value = str(challenge_result['data']['value'])
        challenge_category = challenge_result['data']['category']
        # challenge_prereq = check_req(cid)
        challenge_dict.update({cid:[challenge_name,challenge_value,challenge_category]})
        # print(challenge_id+": ['"+challenge_name+"','"+challenge_value+"','"+challenge_category+"','"+challenge_prereq+"'],")`
    except Exception:
      break
    cid+=1

  for i in challenge_dict:
    replace_text = replace_text+f"{i}: {challenge_dict[i]},\n"

  patch_autoscoreboard_js(parent_path)
