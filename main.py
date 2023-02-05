import requests,sys,json,csv,random,os,ast

# randomly generate a hex string (8bits) to be used as binaries later
def generate_hex():
  hex_array = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']

  higher_four_bits = random.randint(0,15)
  lower_four_bits = random.randint(0,15)
  full_eight_bits = hex_array[higher_four_bits] + hex_array[lower_four_bits]
  return full_eight_bits

# checks the challenge existance, if so, return the challenge id
def challenge_id_and_existance(challenge_type,n):
  if challenge_type == "xor":
    cname = 'XOR Challenge '+str(n)
  elif challenge_type == "birth":
    cname = 'Birth Month '+str(n)


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

# update the user profile to add binaries to each user
def update_user_profile():
  with open("users_info_record.csv") as users_record:
    heading = next(users_record)
    users_reader = csv.reader(users_record)
    with requests.Session() as user_update_session:
      user_update_session.headers.update({"Authorization": f"Token {token}"})
      for line in users_reader:
        user_id = int(line[0])
        payload = '{"fields":[{"field_id":3,"value":"'+bin(int(line[4], 16))[2:].zfill(8)+'"}]}'
        user_update_session.patch(
          f"{url}/api/v1/users/{user_id}",
          json=json.loads(payload),
          headers={"Content-Type": "application/json"},
        )

# collect username and id information for other functions to use
def get_usernames():
  username_id_csv = open('names_record.csv', 'w', newline='')
  username_id_csv.write('username,id\n')
  # print("[+] Created username record file: names_record.csv")

  with requests.Session() as username_session:
    all_user_info_json = username_session.get(f"{url}/api/v1/users").json()
    total_number_of_users = all_user_info_json['meta']['pagination']['total']

  if total_number_of_users > 1:
    for i in range(total_number_of_users):
      username_id_csv.write('%s,%s\n' % (all_user_info_json['data'][i]['name'],all_user_info_json['data'][i]['id']))
    username_id_csv.close()
    print("[+] Updated names_record.csv")

    if os.path.isfile('users_info_record.csv') == False:
      with open("names_record.csv") as names_record:
        heading = next(names_record)
        id_reader = csv.reader(names_record)
        users_info_csv = open('users_info_record.csv', 'w')
        users_info_csv.write('id,name,field_1_value,field_2_value,hex,paired_name,paired_hex,xor_result\n')
        print("[+] Users' info record file does not exist, file created.")
        print("[+] Filling file content...")
        with requests.Session() as usersinfo_session:
          usersinfo_session.headers.update({"Authorization": f"Token {token}"})
          for line in id_reader:
            users_info_json = usersinfo_session.get(f"{url}/api/v1/users/{line[1]}",headers={"Content-Type": "application/json"}).json()
            user_id = users_info_json['data']['id']
            user_name = users_info_json['data']['name']
            field_1_value = users_info_json['data']['fields'][0]['value']
            field_2_value = users_info_json['data']['fields'][1]['value']
            user_hex = generate_hex()
            users_info_csv.write('%s,%s,%s,%s,%s,%s,%s,%s\n' % (user_id,user_name,field_1_value,field_2_value,user_hex,'','',''))
      print("[+] Accquired every user's information!")
    else:
      print("[+] User info file already exist, checking information...")
      ids = []
      with open("users_info_record.csv") as users_info_csv:
        users_info_reader = csv.DictReader(users_info_csv)

        for col in users_info_reader:
          ids.append(col['id'])

      with open("names_record.csv") as names_record:
        heading = next(names_record)
        names_reader = csv.reader(names_record)
        users_info_record_csv = open('users_info_record.csv', 'a')
        with requests.Session() as add_user_info_session:
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
        print("[+] User information is up to date.")
      return True
  else:
    return False

# pair up users so the coordination challenges can be created
def generate_pair_and_xor():
  ids=[]
  full_name=[]
  user_hex=[]
  paired_name=[]
  paired_hex=[]
  xor_result=[]

  with open("users_info_record.csv") as users_info_record:
    user_info_dictreader = csv.DictReader(users_info_record)
    for col in user_info_dictreader:
      ids.append(col['id'])
      full_name.append(col['field_1_value'])
      user_hex.append(col['hex'])
      paired_name.append(col['paired_name'])
      paired_hex.append(col['paired_hex'])
      xor_result.append(col['xor_result'])

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
    col_names = ['id', 'user_name','user_hex','paired_name','paired_hex','xor_result','challenge_added','challenge_number']
    writer = csv.DictWriter(xor_record, fieldnames=col_names)

    for n in range(len(ids)):
      cid,cstatus = challenge_id_and_existance('xor',n+1)
      if cstatus == True:
        print(f"[i] XOR Challenge {n+1} already exist, skip.")
        pass
      elif cstatus == False:
        if add_new_xor_challenge(full_name[n],paired_name[n],xor_result[n],str(int(n)+1)) is True:
          row="{'id':'"+ids[n]+"', 'user_name':'"+full_name[n]+"','user_hex':'"+user_hex[n]+"','paired_name':'"+paired_name[n]+"','paired_hex':'"+paired_hex[n]+"','xor_result':'"+xor_result[n]+"','challenge_added':'yes','challenge_number':'"+str(int(n)+1)+"'}"
          row_dict = ast.literal_eval(row)
          writer.writerow(row_dict)
          row=''
        else:
          pass



# add new coordination challenges
def add_new_xor_challenge(first_name,second_name,xor,n):
  if second_name == '':
    pass
  else:
    with requests.Session() as update_session:
      update_session.headers.update({"Authorization": f"Token {token}"})
      payload = '{"name":"XOR Challenge '+n+'","category":"Coordination","description":"Each of the player is assigned a binary code, you can find your code in the Profile page.\\r\\nNow, retrieve secret codes from **'+first_name+'** and **'+second_name+'**. Return the XOR of the two binary sequances.\\r\\n\\r\\nThe flag is in the format <code>flag{01010101}</code> \\r\\n\\r\\nPlease speak quietly or use private one-on-one chat function(if there is one) when asking codes from another player.","value":"24","state":"hidden","type":"standard"}'
      challenge_result = update_session.post(f"{url}/api/v1/challenges",json=json.loads(payload)).json()
      add_challenge_result = challenge_result['success']

      last_id,cstatus = challenge_id_and_existance('xor',n)

      result = add_new_xor_flag(last_id,n,xor,add_challenge_result)

      return result

# add corresponding flags for the new challenges
def add_new_xor_flag(last_id,n,xor,add_challenge_result):
  with requests.Session() as update_session:
    update_session.headers.update({"Authorization": f"Token {token}"})
    if add_challenge_result == True:
      payload = '{"challenge_id":"'+str(last_id)+'","content":"'+xor+'","type":"static","data":""}'
      flag_result = update_session.post(f"{url}/api/v1/flags",json=json.loads(payload)).json()

      if flag_result['success'] == True:
        print(f"[+] Added new challenge {last_id} and its flag.")
        return True
      else:
        print(f"[+] Error when adding challenge {last_id} flag.")
        return False
    else:
      print("[+] Error when adding challenge.")
      return False

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

##--------------below are for creating birth day challenges--------------
# check how many birth month challenge already exist
def does_birth_challenge_exist():
  print('[i] Checking the challenge status...')
  cid2,cstatus2 = challenge_id_and_existance('birth','2')
  cid1,cstatus1 = challenge_id_and_existance('birth','1')

  if cstatus2 == True:
    print('[i] There are aleady two birth month challenges, checking new user...\r')
    return 2
  elif cstatus1 == True:
    print('[e] There is one birth month challenge already, I can\'t handle this situation right now. Please remove the existing challenge and retry.\r')
    return 1
  else:
    print('[i] No existing birth month challenge, don\'t worry, I\'ll create them.\r')
    return 0

# the main program
def birthmonth_challenge():
  with open("users_info_record.csv") as users_info_record:
    user_info_dictreader = csv.DictReader(users_info_record)
    ids=[]
    full_name=[]
    user_birth_months=[]
    for col in user_info_dictreader:
      ids.append(col['id'])
      full_name.append(col['field_1_value'])
      user_birth_months.append(col['field_2_value'])

  print('[i] Player information collected.')
  with open("birth_month_record.csv") as month_record:
    month_dictreader = csv.DictReader(month_record)
    name_used = []
    month_used = []
    for col in month_dictreader:
      name_used.append(col['full_name_used'])
      month_used.append(col['birth_month'])

  if len(set(user_birth_months)) < 3:
    print('[e] There\'re less than 3 players. In practice, birth challenge doesn\'t make a lot sense.\n    Continue checking.\r')
    pass
  elif len(set(month_used)) == 2:
    print('[e] CTF showing no birth challenge; however, csv file showing two. Please remove the "birth_month_record.csv" file and try again.\r')
    sys.exit()
  elif len(set(month_used)) == 0:
    print('[i] Creating challenge now...')
    month_to_add = random.sample(list(set(user_birth_months)),k=2)

    picked_id = []
    picked_full_name = []
    picked_birth_month = []

    for i in range(2):
      for n in range(len(user_birth_months)):
        if user_birth_months[n] == month_to_add[i]:
          picked_id.append(ids[n])
          picked_full_name.append(full_name[n])
          picked_birth_month.append(user_birth_months[n])
        else:
          pass

    with open("birth_month_record.csv",'a') as birth_month_record:
      col_names = ['full_name_used','birth_month','challenge_added','challenge_number']
      birth_month_writer = csv.DictWriter(birth_month_record, fieldnames=col_names)

      for birth_challenge_number in range(len(month_to_add)):
        # print()
        if add_new_birth_challenge(picked_full_name,picked_birth_month,month_to_add[birth_challenge_number],birth_challenge_number+1) is True:
          for n in range(len(picked_full_name)):
            if picked_birth_month[n] == month_to_add[birth_challenge_number]:
              row="{'full_name_used':'"+picked_full_name[n]+"','birth_month':'"+picked_birth_month[n]+"','challenge_added':'yes','challenge_number':'"+str(birth_challenge_number+1)+"'}"
              row_dict = ast.literal_eval(row)
              birth_month_writer.writerow(row_dict)
              row=''
        else:
          pass
  # #following case with 1 existing birth challenge is not finalized, thus not used. 
  # elif len(set(month_used)) == 1:
  #   while True:
  #     month_to_add = random.sample(list(set(user_birth_months)),k=1)
  #     if month_to_add[0] == month_used[0]:
  #       continue
  #     else:
  #       break
  #   picked_id = []
  #   picked_full_name = []
  #   picked_birth_month = []

  #   for n in range(len(ids)):
  #     if user_birth_months[n] == month_to_add[0]:
  #       picked_id.append(ids[n])
  #       picked_full_name.append(full_name[n])
  #       picked_birth_month.append(user_birth_months[n])
  #     else:
  #       pass

  #   with open("birth_month_record.csv",'a') as birth_month_record:
  #     col_names = ['full_name_used','birth_month','challenge_exist','challenge_number']
  #     birth_month_writer = csv.DictWriter(birth_month_record, fieldnames=col_names)

  #   # if does_birth_challenge_exist() == 1:
  #     if add_new_birth_challenge(picked_id,picked_full_name,picked_birth_month,2) is True:
  #       for n in range(len(picked_id))
  #         row="{'full_name_used':'"+picked_full_name[n]+"','birth_month':'"+picked_birth_month+"','challenge_exist':'yes','challenge_number':'2'}"
  #         row_dict = ast.literal_eval(row)
  #         birth_month_writer.writerow(row_dict)
  #         row=''
  #     else:
  #       pass
  #   # elif does_birth_challenge_exist() == 2 or does_birth_challenge_exist() == 0:
  #   #   print("[+] Something's wrong. There should be only one birth month challenge; however, the record shows a different number.")
  #   #   pass
  else:
    print('[e] CTF showing no birth month challenge; however, csv file showing one. Pelase remove the "birth_month_record.csv" file, and run this program again.\r')
    pass

# add new birth month challenges
def add_new_birth_challenge(picked_full_name,picked_birth_month,challenge_birth_month,birth_challenge_number):
  with requests.Session() as update_session:
    update_session.headers.update({"Authorization": f"Token {token}"})
    payload = '{"name":"Birth Month '+str(birth_challenge_number)+'","category":"Coordination","description":"There should be at least one player that was born in '+challenge_birth_month+'. Could you provide the first name of at least one?\\r\\n\\r\\nEnter their first name as the flag.","value":"34","state":"hidden","type":"standard"}'
    challenge_result = update_session.post(f"{url}/api/v1/challenges",json=json.loads(payload)).json()
    add_challenge_result = challenge_result['success']

  last_id,cstatus = challenge_id_and_existance('birth',birth_challenge_number)

  result = add_new_birth_flag(last_id,picked_full_name,picked_birth_month,challenge_birth_month,add_challenge_result)
  return result

# add corresponding birth month flags
def add_new_birth_flag(last_id,picked_full_name,picked_birth_month,challenge_birth_month,add_challenge_result):
  with requests.Session() as update_session:
    update_session.headers.update({"Authorization": f"Token {token}"})
    content_string = ''

    for n in range(len(picked_full_name)):
      if picked_birth_month[n] == challenge_birth_month:
        content_string = content_string+"|"+picked_full_name[n].split()[0]
    content_string = '('+content_string.lstrip('|')+')'

    if add_challenge_result == True:
      payload = '{"challenge_id":"'+str(last_id)+'","content":"'+content_string+'","type":"regex","data":"case_insensitive"}'
      # print(payload)
      flag_result = update_session.post(f"{url}/api/v1/flags",json=json.loads(payload)).json()

      if flag_result['success'] == True:
        print("[+] The birth month challenge and coressponding flag was added.")
        return True
      else:
        print("[e] Error when adding flag.")
        return False
    else:
      print("[e] Error when adding challenge.")
      return False
      
##--------------the section below check new user's birth month and update existing challenges--------------
# check if new user joined the game, and check the new user's birth month
def new_user_birth_check():
  field_1_value = []
  field_2_value = []
  with open("users_info_record.csv") as users_info_csv:
    users_info_reader = csv.DictReader(users_info_csv)
    for col in users_info_reader:
      field_1_value.append(col['field_1_value'])
      field_2_value.append(col['field_2_value'])

  full_name_used = []
  birth_month = []
  challenge_number = []
  with open("birth_month_record.csv") as birth_challenge_record:
    birth_challenge_reader = csv.DictReader(birth_challenge_record)
    for col in birth_challenge_reader:
      full_name_used.append(col['full_name_used'])
      birth_month.append(col['birth_month'])
      challenge_number.append(col['challenge_number'])

  used_months = list(set(birth_month))

  if used_months:
    monthdict = {birth_month[a]:challenge_number[a] for a in range(len(birth_month))}

    with open("birth_month_record.csv",'a') as birth_month_record:
      col_names = ['full_name_used','birth_month','challenge_added','challenge_number']
      birth_month_writer = csv.DictWriter(birth_month_record, fieldnames=col_names)

      for n in range(2):
        for j in range(len(field_1_value)):
          if used_months[n] == field_2_value[j] and field_1_value[j] not in full_name_used:
            new_full_name = field_1_value[j]
            cid,cstatus = challenge_id_and_existance('birth',monthdict[used_months[n]])
            # flag_id,flag_content = birth_flag_id(birth_challenge_id(monthdict[used_months[n]]))          
            flag_id,flag_content = birth_flag_id(cid)
            if patch_birth_flag(flag_id,flag_content,new_full_name) is True:
              row="{'full_name_used':'"+new_full_name+"','birth_month':'"+used_months[n]+"','challenge_added':'yes','challenge_number':'"+str(monthdict[used_months[n]])+"'}"
              row_dict = ast.literal_eval(row)
              birth_month_writer.writerow(row_dict)
          else:
            pass
  else:
    pass

# # get the birth month challenge id
# def birth_challenge_id(birth_challenge_number):
#   with requests.Session() as id_check_session:
#     id_check_session.headers.update({"Authorization": f"Token {token}"})
#     id_check_result = id_check_session.get(f"{url}/api/v1/challenges",headers={"Content-Type": "application/json"}).json()
#     for name in id_check_result['data']:
#       if name['name'] == 'Birth Month '+str(birth_challenge_number):
#         return name['id']
#       else:
#         pass
#     pass

# add birth month flag by using the birth month challenge id
def birth_flag_id(challenge_id):
  with requests.Session() as id_check_session:
    id_check_session.headers.update({"Authorization": f"Token {token}"})
    id_check_result = id_check_session.get(f"{url}/api/v1/flags",headers={"Content-Type": "application/json"}).json()
    for flag_content in id_check_result['data']:
      if flag_content['challenge_id'] == challenge_id:
        return flag_content['id'],flag_content['content']
      else:
        pass
    pass

# patch the existing birth month challenge to use the new user information
def patch_birth_flag(flag_id,flag_content,new_full_name):
  print('[+] New user found! Patching existing birth month challenge...')
  new_content = flag_content.rstrip(')') + '|'+new_full_name.split()[0]+')'
  with requests.Session() as update_session:
    update_session.headers.update({"Authorization": f"Token {token}"})
    # content_string = ''

    payload = '{"content": "'+new_content+'", "data": "case_insensitive", "type": "regex", "id": "'+str(flag_id)+'"}'
    flag_result = update_session.patch(f"{url}/api/v1/flags/{flag_id}",json=json.loads(payload)).json()

    if flag_result['success'] == True:
      print("[i] Birth month challenge flag was updated.")
      return True
    else:
      print("[e] Error when adding flag.")
      return False

# verify the token works
def check_token():
  check_token_result = {}

  with requests.Session() as check_token_session:
    check_token_session.headers.update({"Authorization": f"Token {token}"})
    check_token_result = check_token_session.get(f"{url}/api/v1/users/1",headers={"Content-Type": "application/json"})
  if check_token_result.status_code == 200:
    pass
  else:
    print('[e] Cannot access CTFd api, please check token or IP.')
    sys.exit()

##--------------the sectoin below change the points for each new challenge--------------
# count how many coordination challenges
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

  if number_of_breakout_room == "1":
    update_points("80",new_points)
  elif number_of_breakout_room == "2":
    update_points("80",new_points)
    update_points("81",new_points)

  cid2 = 82
  try:
    while True:
      with requests.Session() as id_check_session:
        id_check_session.headers.update({"Authorization": f"Token {token}"})
        id_check_result = id_check_session.get(f"{url}/api/v1/challenges/{cid2}",headers={"Content-Type": "application/json"}).json()
        try:
          if id_check_result['data']['category'] == 'Coordination':
            update_points(str(id_check_result['data']['id']),new_points)
        except Exception:
          break
        cid2+=1
    print('[+] Coordination points changed')
  except Exception:
    print('[e] Coordination points not updated.')
    pass

# assign points to each coordination challenge based on the count number
def update_points(challenge_id,new_points):
  with requests.Session() as update_session:
    update_session.headers.update({"Authorization": f"Token {token}"})
    payload = '{"value":"'+str(new_points)+'"}'
    flag_result = update_session.patch(f"{url}/api/v1/challenges/{challenge_id}",json=json.loads(payload))
    if flag_result.status_code > 399:
      print(f'[e] Challenge {challenge_id} points not updated')

##--------------the section below update the prerequisite for new and existing challenges-------------- 
def check_req(challenge_id):
  with requests.Session() as update_session:
    update_session.headers.update({"Authorization": f"Token {token}"})
    flag_result = update_session.get(f"{url}/api/v1/challenges/{challenge_id}/requirements",json='').json()
    try:
      requirements_id = str(flag_result['data']['prerequisites'][0])
      # print(str(challenge_id) + ':'+requirements_id)
      return requirements_id
    except Exception:
      # print(challenge_id)
      return ''

def patch_prereq(challenge_id,prereq_id):
    try:
      with requests.Session() as update_session:
        update_session.headers.update({"Authorization": f"Token {token}"})
        payload = '{"requirements":{"prerequisites":['+prereq_id+']}}'
        flag_result = update_session.patch(f"{url}/api/v1/challenges/{challenge_id}",json=json.loads(payload))
    except Exception:
      print("[e] Something's wrong, nothing changed.")

def make_visible(challenge_id):
  with requests.Session() as update_session:
    update_session.headers.update({"Authorization": f"Token {token}"})
    payload = '{"state":"visible"}'
    flag_result = update_session.patch(f"{url}/api/v1/challenges/{challenge_id}",json=json.loads(payload))

def make_hidden(challenge_id):
  with requests.Session() as update_session:
    update_session.headers.update({"Authorization": f"Token {token}"})
    payload = '{"state":"hidden"}'
    flag_result = update_session.patch(f"{url}/api/v1/challenges/{challenge_id}",json=json.loads(payload))

def patch_new_prereq(count):
  challenge_dict = {}
  cid = 82
  while True:
    try:
      with requests.Session() as check_existence:
        check_existence.headers.update({"Authorization": f"Token {token}"})
        challenge_result = check_existence.get(f"{url}/api/v1/challenges/{cid}",json='').json()
        # print(challenge_result)
        challenge_id = str(challenge_result['data']['id'])
        challenge_name = challenge_result['data']['name']
        challenge_value = str(challenge_result['data']['value'])
        challenge_category = challenge_result['data']['category']
        challenge_prereq = check_req(challenge_id)
        # print(challenge_id+": ['"+challenge_name+"','"+challenge_value+"','"+challenge_category+"','"+challenge_prereq+"'],")
        challenge_dict[challenge_id]=[challenge_name,challenge_value,challenge_category,challenge_prereq]
    except Exception:
      break
    cid+=1

  print("[+] Checking and updating prerequisite information...")
  
  for key,value in challenge_dict.items():
    if "Birth Month 1" in value:
      if challenge_dict.get(key)[3] == '':
        patch_prereq(key,"79")
        make_visible(key)
    elif "Birth Month 2" in value:
      if challenge_dict.get(key)[3] == '':
        patch_prereq(key,"38")
        make_visible(key)
    elif "XOR Challenge 1" in value:
      if challenge_dict.get(key)[3] == '':
        patch_prereq("80",key)
        patch_prereq(key,"77")
        make_visible(key)
    elif "XOR Challenge 2" in value:
      if challenge_dict.get(key)[3] == '':
        patch_prereq("71",key)
        make_visible(71)
        patch_prereq("47",key)
        make_visible (47)
        patch_prereq(key,"77")
        make_visible(key)
    elif "XOR Challenge 3" in value:
      if challenge_dict.get(key)[3] == '':
        patch_prereq("81",key)
        if count == 2:
          make_visible(81)
        else:
          pass
        patch_prereq("12",key)
        make_visible(12)
        for key2,value2 in challenge_dict.items():
          if "Birth Month 1" in value2:
            patch_prereq(key,key2)
        make_visible(key)
    elif "XOR Challenge 4" in value:
      if challenge_dict.get(key)[3] == '':
        patch_prereq(key,"64")
        make_visible(key)
    elif "XOR Challenge 5" in value:
      if challenge_dict.get(key)[3] == '':
        patch_prereq("31",key)
        make_visible (31)
        patch_prereq(key,"22")
        make_visible(key)
    elif "XOR Challenge 6" in value:
      if challenge_dict.get(key)[3] == '':
        patch_prereq("11",key)
        make_visible(11)
        patch_prereq(key,"22")
        make_visible(key)
    elif "XOR Challenge 7" in value:
      if challenge_dict.get(key)[3] == '':
        patch_prereq(key,"44")
        make_visible(key)
    elif "XOR Challenge 8" in value:
      if challenge_dict.get(key)[3] == '':
        patch_prereq(key,"35")
        make_visible(key)
    else:
      if challenge_dict.get(key)[3] == '':
        patch_prereq(key,"77")
        make_visible(key)

    if count == 0:
      make_hidden(80)
      make_hidden(81)
    elif count == 1:
      make_visible(80)
      make_hidden(81)
    elif count == 2:
      make_visible(80)
      make_visible(81)
    else:
      pass
if __name__ == "__main__":
  token = "15c288f2a166e3cef2ebb182a007212e747947aae7ff55fe103bcbb7f1695e2a"
  url = "http://209.114.126.86"

# make sure the token is working 
  check_token()
  global birth_month1_id 
# ask for how many breakout room
  while True:
    number_of_breakout_room = input("How many Breakout Rooms?(Answer 0,1, or 2)\n")
    if number_of_breakout_room == "0":
      count = 0
      break
    elif number_of_breakout_room == "1":
      count = 1
      break
    elif number_of_breakout_room == "2":
      count = 2
      break
    else:
      print("You need to answer 0,1, or 2.")
      continue

# check the xor_record file, if doesn't exist, create the file
  if os.path.isfile('xor_record.csv') == False:
      with open("xor_record.csv",'w',newline='') as xor_record:
        col_names = ['id', 'user_name','user_hex','paired_name','paired_hex','xor_result','challenge_added','challenge_number']
        writer = csv.DictWriter(xor_record, fieldnames=col_names)
        writer.writeheader()
  else:
    pass

# check the birth_month_record file, if doesn't exist, create the file
  if os.path.isfile('birth_month_record.csv') == False:
    with open("birth_month_record.csv",'w',newline='') as birth_month_record:
      col_names = ['full_name_used','birth_month','challenge_added','challenge_number']
      writer = csv.DictWriter(birth_month_record, fieldnames=col_names)
      writer.writeheader()
  else:
    pass

# run the main program
  try:
    while True:
      if get_usernames() == True:
        update_user_profile()
        patch_coor_practice()
        generate_pair_and_xor()
        flag = does_birth_challenge_exist()
        if flag == 0:
          try:
            birthmonth_challenge()
            # new_user_birth_check()
          except Exception:
            print('[e] No enough user to add birth challenges.\r')
            pass
        elif flag == 2:
          new_user_birth_check()
          count_coordination(count)
          patch_new_prereq(count)
        else:
          pass
      else:
        pass
  except KeyboardInterrupt:
    print("[i] Quit by user...")
