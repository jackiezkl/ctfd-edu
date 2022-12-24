import requests,sys,json,csv,random,os

def generate_hex():
  hex_array = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']

  higher_four_bits = random.randint(0,15)
  lower_four_bits = random.randint(0,15)
  full_eight_bits = hex_array[higher_four_bits] + hex_array[lower_four_bits]
  return full_eight_bits

# def create_xor_record(first_hex,second_hex):
#   first_binary = (bin(int(first_hex, 16))[2:].zfill(8))
#   second_binary = (bin(int(second_hex, 16))[2:].zfill(8))
#   xor_result = (bin(int(first_fullbits, 16) ^ int(second_fullbits, 16))[2:].zfill(8))
#   return first_binary,second_binary,xor_result

def update_user_profile(url,token):
  with open("users_info_record.csv") as users_record:
    heading = next(users_record)
    users_reader = csv.reader(users_record)
    user_update_session = requests.Session()
    user_update_session.headers.update({"Authorization": f"Token {token}"})
    for line in users_reader:
      user_id = int(line[0])
      payload = '{"fields":[{"field_id":3,"value":"'+bin(int(line[4], 16))[2:].zfill(8)+'"}]}'
      user_update_session.patch(
        f"{url}/api/v1/users/{user_id}",
        json=json.loads(payload),
        headers={"Content-Type": "application/json"},
      )
    users_record.close()

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
      users_info_csv.write('id,name,field_1_value,field_2_value,hex,paired_name,paired_hex,xor_result\n')
      print("[+] Users' info record file does not exist, file created.")
      print("[+] Filling file content...")
      usersinfo_session = requests.Session()
      usersinfo_session.headers.update({"Authorization": f"Token {token}"})
      for line in id_reader:
        users_info_json = usersinfo_session.get(f"{url}/api/v1/users/{line[1]}",headers={"Content-Type": "application/json"}).json()
        user_id = users_info_json['data']['id']
        user_name = users_info_json['data']['name']
        field_1_value = users_info_json['data']['fields'][0]['value']
        field_2_value = users_info_json['data']['fields'][1]['value']
        user_hex = generate_hex()
        users_info_csv.write('%s,%s,%s,%s,%s,%s,%s,%s\n' % (user_id,user_name,field_1_value,field_2_value,user_hex,'','',''))
      names_record.close()
    print("[+] Accquired every user's information!")
  else:
    print("[+] User info file already exist, checking information...")
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
          field_1_value = users_info_json['data']['fields'][0]['value']
          field_2_value = users_info_json['data']['fields'][1]['value']
          user_hex = generate_hex()
          print("[+] New user added.")
          users_info_record_csv.write('%s,%s,%s,%s,%s,%s,%s,%s\n' % (user_id,user_name,field_1_value,field_2_value,user_hex,'','',''))
      names_record.close()
      print("[+] User information is up to date.")

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

# def generate_pair_and_xor(url,token):
#   with open("users_info_record.csv") as users_info_record:
#     heading = next(users_info_record)
#     user_info_dictreader = csv.DictReader(users_info_record)
#     full_name=[]
#     user_hex=[]
#     paired_name=[]
#     paired_hex=[]
#     xor_result=[]
#     for col in user_info_dictreader:
#       full_name.append(col[full name
#                        ids.append(col['id'])
      

if __name__ == "__main__":
  token = "4fb4c02d643f6667f2d187eb62c081f3b1e0e987978b896d9c1f4ab557db285f"
  url = "http://209.114.126.63"

  try:
    while True:
      get_usernames(url,token)
      update_user_profile(url,token)
#       generate_pair_and_xor(url,token)
  except KeyboardInterrupt:
    print("Quit by user...")
      #   add_new_challenge(url,token)
