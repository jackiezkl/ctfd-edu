import requests,sys,json,csv

def get_usernames(url):
  username_session = requests.Session()
  all_user_info_json = username_session.get(f"{url}/api/v1/users").json()
  total_number_of_users = all_user_info_json['meta']['pagination']['total']

  for i in range(total_number_of_users):
    print(all_user_info_json['data'][i]['name'])


        
def add_new_challenge(url,token)
  s = requests.Session()
  s.headers.update({"Authorization": f"Token {token}"})

  r = s.post(
    f"{url}/api/v1/challenges",
    json={"name":"XOR Challenge 3",
           "category":"Coordination",
           "description":"Retrieve \"**Tom**\" and \"**Ashley**\"'s secret  8-bit number\r\n\r\nReturn the XOR of these two binary sequences.\r\n\r\nThe flag is in the format:``flag{01010101}``\r\n\r\nplease use private one-on-one chat function.",
           "value":"24",
           "state":"visible",
           "type":"standard"},
  )

  s.post(
    f"{url}/api/v1/flags",
    json={"challenge_id":"4","content":"30101010","type":"static","data":""},
  )

if __name__ == "__main__":
  token = "4fb4c02d643f6667f2d187eb62c081f3b1e0e987978b896d9c1f4ab557db285f"
  url = "http://209.114.126.63"    
  get_usernames(url)
#   add_new_challenge(url,token)
