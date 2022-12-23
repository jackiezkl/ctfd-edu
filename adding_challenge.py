import requests,sys,json,csv,random,os

def generate_hex():
  hex_array = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']

  higherbits = random.randint(0,15)
  lowerbits = random.randint(0,15)
  fullbits = hex_array[higherbits] + hex_array[lowerbits]
  return fullbits

def create_xor_record(first_hex,second_hex):
  first_binary = (bin(int(first_hex, 16))[2:].zfill(8))
  second_binary = (bin(int(second_hex, 16))[2:].zfill(8))
  xor_result = (bin(int(first_fullbits, 16) ^ int(second_fullbits, 16))[2:].zfill(8))
  return first_binary,second_binary,xor_result

def update_user_profile(url,token):
  with open("users_info_record.csv") as users_record:
    heading = next(users_record)
    users_reader = csv.reader(users_record)
    user_update_session = requests.Session()
    user_update_session.headers.update({"Authorization": f"Token {token}"})
    for line in users_reader:
      user_id = int(line[0])
      payload = '{"name":"'+line[1]+'","email":"'+line[2]+'","type":"'+line[3]+'","verified":false,"hidden":false,"banned":false,"fields":[{"field_id":1,"value":"'+line[8]+'"},{"field_id":2,"value":"'+line[10]+'"},{"field_id":3,"value":"'+bin(int(line[11], 16))[2:].zfill(8)+'"}]}'
      r = user_update_session.patch(
        f"{url}/api/v1/users/{user_id}",
        json=f"{payload}",
        headers={"Content-Type": "application/json"},
      )
      print(r.json())
def get_usernames(url,token):
  username_id_csv = open('names_record.csv', 'w', newline='')
  username_id_csv.write('username,id\n')
  print("[+] Created username record file: names_record.csv")

  username_session = requests.Session()
  all_user_info_json = username_session.get(f"{url}/api/v1/users").json()
  total_number_of_users = all_user_info_json['meta']['pagination']['total']

  for i in range(total_number_of_users):
    username_id_csv.write('%s,%s\n' % (all_user_info_json['data'][i]['name'],all_user_info_json['data'][i]['id']))
  username_id_csv.close()
  print("[+] Saved to names_record.csv")

  if os.path.isfile('users_info_record.csv') == False:
    with open("names_record.csv") as names_record:
      heading = next(names_record)
      id_reader = csv.reader(names_record)
      users_info_csv = open('users_info_record.csv', 'w')
      users_info_csv.write('id,name,email,type,verified,hidden,banned,field_id_1,value_1,field_id_2,value_2,hex\n')
      print("[+] Users' info record file does not exist, file created.")
      print("[+] Filling file content...")
      usersinfo_session = requests.Session()
      usersinfo_session.headers.update({"Authorization": f"Token {token}"})
      for line in id_reader:
        users_info_json = usersinfo_session.get(f"{url}/api/v1/users/{line[1]}",headers={"Content-Type": "application/json"}).json()
        user_id = users_info_json['data']['id']
        user_name = users_info_json['data']['name']
        user_email = users_info_json['data']['email']
        user_type = users_info_json['data']['type']
        user_verified = users_info_json['data']['verified']
        user_hidden = users_info_json['data']['hidden']
        user_banned = users_info_json['data']['banned']
        field_id_1 = users_info_json['data']['fields'][0]['field_id']
        value_1 = users_info_json['data']['fields'][0]['value']
        field_id_2 = users_info_json['data']['fields'][1]['field_id']
        value_2 = users_info_json['data']['fields'][1]['value']
        user_hex = generate_hex()
        users_info_csv.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (user_id,user_name,user_email,user_type,user_verified,user_hidden,user_banned,field_id_1,value_1,field_id_2,value_2,user_hex))
    print("[+] Accquired every user's information!")
  else:
    print("[+] File already exist, checking information...")
    ids = []
    with open("users_info_record.csv") as users_info_csv:
      users_info_reader = csv.DictReader(users_info_csv)

      for col in users_info_reader:
        ids.append(col['id'])
      users_info_csv.close()

    with open("names_record.csv") as names_record:
      heading = next(names_record)
      names_reader = csv.reader(names_record)
      users_info_record_csv = open('users_info_record.csv', 'a')
      add_user_info_session = requests.Session()
      add_user_info_session.headers.update({"Authorization": f"Token {token}"})
      for line in names_reader:
        if line[1] in ids:
          pass
        else:
          users_info_json = add_user_info_session.get(f"{url}/api/v1/users/{line[1]}",headers={"Content-Type": "application/json"}).json()
          user_id = users_info_json['data']['id']
          user_name = users_info_json['data']['name']
          user_email = users_info_json['data']['email']
          user_type = users_info_json['data']['type']
          user_verified = users_info_json['data']['verified']
          user_hidden = users_info_json['data']['hidden']
          user_banned = users_info_json['data']['banned']
          field_id_1 = users_info_json['data']['fields'][0]['field_id']
          value_1 = users_info_json['data']['fields'][0]['value']
          field_id_2 = users_info_json['data']['fields'][1]['field_id']
          value_2 = users_info_json['data']['fields'][1]['value']
          user_hex = generate_hex()
          print("[+] New user added.")
          users_info_record_csv.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (user_id,user_name,user_email,user_type,user_verified,user_hidden,user_banned,field_id_1,value_1,field_id_2,value_2,user_hex))
      print("[+] User information is up to date.")


def update_pair(url,token):
  with open("code_assign_record.csv") as code_assign_record:
    heading = next(code_assign_record)

def add_new_challenge(url,token):
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

  get_usernames(url,token)
  update_user_profile(url,token)
#   add_new_challenge(url,token)
