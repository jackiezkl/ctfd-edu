import requests,json

def count_coordination():
  count = 0
  with requests.Session() as check_existence:
    check_existence.headers.update({"Authorization": f"Token {token}"})
    challenge_result = check_existence.get(f"{url}/api/v1/challenges",json='').json()

    for name in challenge_result['data']:
      if "XOR Challenge" in name['name']:
        count+=1
      elif "Birth Month" in name['name']:
        count+=1

    new_points = round(500/count)

    for name in challenge_result['data']:
      if "XOR Challenge" in name['name']:
        update_points(str(name['id']),new_points)
      elif "Birth Month" in name['name']:
        update_points(str(name['id']),new_points)

def update_points(challenge_id,new_points):
  print(challenge_id)
  print(new_points)
  with requests.Session() as update_session:
    update_session.headers.update({"Authorization": f"Token {token}"})
    payload = '{"value":"'+str(new_points)+'"}'
    flag_result = update_session.patch(f"{url}/api/v1/challenges/{challenge_id}",json=json.loads(payload))
    print(flag_result.status_code)


if __name__ == "__main__":
  token = "099b06d2394093117dfd53ca9e01f23a9437fda5579bdd82a317861740f1b35f"
  url = "http://209.114.126.86"

  count_coordination()
