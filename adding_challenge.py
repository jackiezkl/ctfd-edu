import requests,sys,json,csv,random,os,ast

# randomly generate a hex string (8bits) to be used as binaries later
def generate_hex():
  hex_array = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']

  higher_four_bits = random.randint(0,15)
  lower_four_bits = random.randint(0,15)
  full_eight_bits = hex_array[higher_four_bits] + hex_array[lower_four_bits]
  return full_eight_bits

# update the user profile to add binaries to each user
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

# collect username and id information for other functions to use
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

# pair up users so the coordination challenges can be created
def generate_pair_and_xor(url,token):
  with open("users_info_record.csv") as users_info_record:
    user_info_dictreader = csv.DictReader(users_info_record)
    ids=[]
    full_name=[]
    user_hex=[]
    paired_name=[]
    paired_hex=[]
    xor_result=[]
    for col in user_info_dictreader:
      ids.append(col['id'])
      full_name.append(col['field_1_value'])
      user_hex.append(col['hex'])
      paired_name.append(col['paired_name'])
      paired_hex.append(col['paired_hex'])
      xor_result.append(col['xor_result'])
    users_info_record.close()

    for n in range(len(paired_name)):
      if paired_name[n] == '':
        try:
          paired_name[n] = full_name[n+1]
          paired_hex[n] = user_hex[n+1]
          xor_result[n] = (bin(int(paired_hex[n], 16) ^ int(user_hex[n], 16))[2:].zfill(8))
          user_hex[n] = bin(int(user_hex[n],16))[2:].zfill(8)
          paired_hex[n] = bin(int(paired_hex[n],16))[2:].zfill(8)
        except Exception:
          pass
      else:
        pass

    with open("xor_record.csv",'a') as xor_record:
      col_names = ['id', 'user_name','user_hex','paired_name','paired_hex','xor_result','challenge_exist','challenge_number']
      writer = csv.DictWriter(xor_record, fieldnames=col_names)

      for n in range(len(ids)):
        if does_challenge_exist(n+1) == True:
          print("[+] Challenge already exist, skip.")
          pass
        elif does_challenge_exist(n+1) == False:
          if add_new_challenge(url,token,full_name[n],paired_name[n],xor_result[n],str(int(n)+1)) is True:
            row="{'id':'"+ids[n]+"', 'user_name':'"+full_name[n]+"','user_hex':'"+user_hex[n]+"','paired_name':'"+paired_name[n]+"','paired_hex':'"+paired_hex[n]+"','xor_result':'"+xor_result[n]+"','challenge_exist':'yes','challenge_number':'"+str(int(n)+1)+"'}"
            row_dict = ast.literal_eval(row)
            writer.writerow(row_dict)
            row=''
          else:
            pass

def does_challenge_exist(n):
  flag1 = ''
  flag2 = 'no'
  check_existence = requests.Session()
  check_existence.headers.update({"Authorization": f"Token {token}"})
  challenge_result = check_existence.get(f"{url}/api/v1/challenges",json='').json()
  # print(n)
  for name in challenge_result['data']:
    if name['name'] == "XOR Challenge "+str(n):
      flag1 = "yes"
      break
    else:
      flag1 = "no"
      pass
  check_existence.close()
  if flag1 == flag2:
    return False
  elif flag1 != flag2:
    return True

def get_last_created_id(url,token,n):
  id_check_session = requests.Session()
  id_check_session.headers.update({"Authorization": f"Token {token}"})
  id_check_result = id_check_session.get(f"{url}/api/v1/challenges",headers={"Content-Type": "application/json"}).json()
  for name in id_check_result['data']:
    if name['name'] == 'XOR Challenge '+n:
      id_check_session.close()
      return name['id']
    else:
      pass

# add new coordination challenges
def add_new_challenge(url,token,first_name,second_name,xor,n):
  if second_name == '':
    exit()
  else:
    update_session = requests.Session()
    update_session.headers.update({"Authorization": f"Token {token}"})
    payload = '{"name":"XOR Challenge '+n+'","category":"Coordination","description":"Retrieve secret codes from **'+first_name+'** and **'+second_name+'**. Return the XOR of the two binary sequances.\\r\\n\\r\\nThe flag is in the format <code>flag{01010101}</code> \\r\\n\\r\\nPlease use private one-on-one chat function.","value":"24","state":"visible","type":"standard"}'
    challenge_result = update_session.post(f"{url}/api/v1/challenges",json=json.loads(payload)).json()
    add_challenge_result = challenge_result['success']
    update_session.close()

    last_id = get_last_created_id(url,token,n)

    result = add_new_flag(url,token,last_id,n,xor,add_challenge_result)

    return result

# add corresponding flags for the new challenges
def add_new_flag(url,token,last_id,n,xor,add_challenge_result):
  update_session = requests.Session()
  update_session.headers.update({"Authorization": f"Token {token}"})
  if add_challenge_result == True:
    payload = '{"challenge_id":"'+str(last_id)+'","content":"'+xor+'","type":"static","data":""}'
    print(payload)
    flag_result = update_session.post(f"{url}/api/v1/flags",json=json.loads(payload)).json()

    if flag_result['success'] == True:
      print("[+] New challenge and flag added.")
      return True
    else:
      print("[+] Error when adding flag.")
      return False
  else:
    print("[+] Error when adding challenge.")
    return False
  update_session.close()

if __name__ == "__main__":
  token = "e2fea1edc567772f9890dbae1e7d4e82a71299d9a71183a030685a6efd8f6ce9"
  url = "http://127.0.0.1"

  if os.path.isfile('xor_record.csv') == False:
      with open("xor_record.csv",'w',newline='') as xor_record:
        col_names = ['id', 'user_name','user_hex','paired_name','paired_hex','xor_result','challenge_exist','challenge_number']
        writer = csv.DictWriter(xor_record, fieldnames=col_names)

        writer.writeheader()
  else:
    pass
  i = 2
  try:
    while i>1:
      get_usernames(url,token)
      update_user_profile(url,token)
      generate_pair_and_xor(url,token)
  except KeyboardInterrupt:
    print("Quit by user...")
#   add_new_challenge(url,token)
