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

    try:
      for name in challenge_result['data']:
        if "XOR Challenge" in name['name']:
          update_points(str(name['id']),new_points)
        elif "Birth Month" in name['name']:
          update_points(str(name['id']),new_points)
      print('[+] Coordination points changed')
    except Exception:
      print('[e] Coordination points not updated.')
      pass
def update_points(challenge_id,new_points):
  with requests.Session() as update_session:
    update_session.headers.update({"Authorization": f"Token {token}"})
    payload = '{"value":"'+str(new_points)+'"}'
    flag_result = update_session.patch(f"{url}/api/v1/challenges/{challenge_id}",json=json.loads(payload))
    if flag_result.status_code > 399:
      print('[e] Challenge '+challenge_id+' points not updated')


if __name__ == "__main__":
  token = "e1e0c697d7ed975182df847918d0e0fee4c99b48d0eac461e3a2bcfdb3e72e3c"
  url = "http://209.114.126.86"

  count_coordination()
