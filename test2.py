import csv,requests,json

def patch_coor_practice():
  names = []
  with open("users_info_record.csv") as users_info_csv:
    users_info_reader = csv.DictReader(users_info_csv)
    
    for col in users_info_reader:
      names.append(col['field_1_value'])
  challenge_flag = ''
  for name in names:
    challenge_flag = challenge_flag + "|" + name.split()[0]
  challenge_flag = "("+challenge_flag.lstrip("|")+")"
  print(challenge_flag)

  with requests.Session() as update_session:
    update_session.headers.update({"Authorization": f"Token {token}"})

    payload = '{"content": "'+challenge_flag+'", "data": "case_insensitive", "type": "regex", "id": "88"}'
    flag_result = update_session.patch(f"{url}/api/v1/flags/88",json=json.loads(payload)).json()

    if flag_result['success'] == True:
      print("[i] Coordination practice challenge flag was updated.")
      return True
    else:
      print("[e] Error when patching coordination practice flag.")
      return False

if __name__ == "__main__":
  token = "15c288f2a166e3cef2ebb182a007212e747947aae7ff55fe103bcbb7f1695e2a"
  url = "http://209.114.126.86"

  patch_coor_practice()