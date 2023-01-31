import json,requests

def get_last_created_xor_id(n):
  cname = 'XOR Challenge '+n
  cid = 82
  while True:
    with requests.Session() as id_check_session:
      id_check_session.headers.update({"Authorization": f"Token {token}"})
      id_check_result = id_check_session.get(f"{url}/api/v1/challenges/{cid}",headers={"Content-Type": "application/json"}).json()
      try:
        if cname in id_check_result['data']['name']:
          return id_check_result['data']['id']
      except Exception:
        pass

      try:
        if "The requested URL was not found on the server" in id_check_result['message']:
          break
      except Exception:
        pass
      cid+=1

def get_last_created_birth_id(n):
  cname = 'Birth Month '+n
  cid = 82
  while True:
    with requests.Session() as id_check_session:
      id_check_session.headers.update({"Authorization": f"Token {token}"})
      id_check_result = id_check_session.get(f"{url}/api/v1/challenges/{cid}",headers={"Content-Type": "application/json"}).json()
      try:
        if cname in id_check_result['data']['name']:
          return id_check_result['data']['id']
      except Exception:
        pass

      try:
        if "The requested URL was not found on the server" in id_check_result['message']:
          break
      except Exception:
        pass
      cid+=1

def challenge_id_existance(challenge_type,n):
  if challenge_type == "xor":
    cname = 'XOR Challenge '+n
  else:
    cname = 'Birth Month '+n

  cid = 82

  while True:
    with requests.Session() as id_check_session:
      id_check_session.headers.update({"Authorization": f"Token {token}"})
      id_check_result = id_check_session.get(f"{url}/api/v1/challenges/{cid}",headers={"Content-Type": "application/json"}).json()
      try:
        if cname in id_check_result['data']['name']:
          return id_check_result['data']['id'],True
      except Exception:
          return 'None',False

      cid+=1

def count_coordination(number_of_breakout_room):
  count = number_of_breakout_room
  cid = 82
  while True:
    with requests.Session() as id_check_session:
      id_check_session.headers.update({"Authorization": f"Token {token}"})
      id_check_result = id_check_session.get(f"{url}/api/v1/challenges/{cid}",headers={"Content-Type": "application/json"}).json()

      try:
        if "XOR Challenge" in id_check_result['data']['name']:
          count += 1
        elif "Birth Month" in id_check_result['data']['name']:
          count += 1
      except Exception:
        break
      cid+=1
  
  new_points = round(500/count)
  print(new_points)
    # if number_of_breakout_room == "1":
    #   update_points("80",new_points)
    #   make_visible("80")
    # elif number_of_breakout_room == "2":
    #   update_points("80",new_points)
    #   update_points("81",new_points)
    #   make_visible("80")
    #   make_visible("81")

    # try:
    #   for name in challenge_result['data']:
    #     if "XOR Challenge" in name['name']:
    #       update_points(str(name['id']),new_points)
    #     elif "Birth Month" in name['name']:
    #       update_points(str(name['id']),new_points)
    #   print('[+] Coordination points changed')
    # except Exception:
    #   print('[e] Coordination points not updated.')
    #   pass


if __name__ == "__main__":
  token = "15c288f2a166e3cef2ebb182a007212e747947aae7ff55fe103bcbb7f1695e2a"
  url = "http://209.114.126.86"
  
  # cid,cstatus = challenge_id_existance('xor',"8")
  # print(cid)
  # print(cstatus)
  count_coordination(2)