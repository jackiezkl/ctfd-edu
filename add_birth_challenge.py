import csv,requests,time,os,random,json,ast

# check if the birth month challenge is already exist
def does_challenge_exist():
  print('[i] Checking the challenge status...')
  flag = 0
  with requests.Session() as check_existence:
    check_existence.headers.update({"Authorization": f"Token {token}"})
    challenges_list = check_existence.get(f"{url}/api/v1/challenges",json='').json()

  for challenge in challenges_list['data']:
    if challenge['name'] == "Birth Month 2":
      flag += 1
    elif challenge['name'] == "Birth Month 1":
      flag += 1
    else:
      pass

  if flag == 2:
    print('[e] There are aleady two birth month challenges, quitting now...\r')
    return 2
  elif flag == 1:
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
    print('[e] There are less than 3 players. In theory, birth challenge doesn\'t make a lot sense\r')
    exit()
  elif len(set(month_used)) == 2:
    print('[e] CTF showing no birth challenge; however, csv file showing two. Please remove the "birth_month_record.csv" file and try again.\r')
    exit()
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
  # #following case is not used, this program only handles no challenge or 2 challenges situation.
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

  #   # if does_challenge_exist() == 1:
  #     if add_new_challenge(picked_id,picked_full_name,picked_birth_month,2) is True:
  #       for n in range(len(picked_id))
  #         row="{'full_name_used':'"+picked_full_name[n]+"','birth_month':'"+picked_birth_month+"','challenge_exist':'yes','challenge_number':'2'}"
  #         row_dict = ast.literal_eval(row)
  #         birth_month_writer.writerow(row_dict)
  #         row=''
  #     else:
  #       pass
  #   # elif does_challenge_exist() == 2 or does_challenge_exist() == 0:
  #   #   print("[+] Something's wrong. There should be only one birth month challenge; however, the record shows a different number.")
  #   #   pass
  else:
    print('[e] CTF showing no birth month challenge; however, csv file showing one. Pelase remove the "birth_month_record.csv" file, and run this program again.\r')
    pass

# get the challenge if od the created challenge, so we can set flag for that challenge
def get_last_created_id(n):
  with requests.Session() as id_check_session:
    id_check_session.headers.update({"Authorization": f"Token {token}"})
    id_check_result = id_check_session.get(f"{url}/api/v1/challenges",headers={"Content-Type": "application/json"}).json()
    for name in id_check_result['data']:
      if name['name'] == 'Birth Month '+str(n):
        id_check_session.close()
        return name['id']
      else:
        pass
    pass

# add new birth month challenges
def add_new_birth_challenge(picked_full_name,picked_birth_month,challenge_birth_month,birth_challenge_number):
  with requests.Session() as update_session:
    update_session.headers.update({"Authorization": f"Token {token}"})
    payload = '{"name":"Birth Month '+str(birth_challenge_number)+'","category":"Coordination","description":"There should be at least one player that was born in '+challenge_birth_month+'. Could you provide the first name of at least one?\\r\\n\\r\\nEnter their first name as the flag.","value":"34","state":"visible","type":"standard"}'
    challenge_result = update_session.post(f"{url}/api/v1/challenges",json=json.loads(payload)).json()
    add_challenge_result = challenge_result['success']

  last_id = get_last_created_id(birth_challenge_number)

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
      payload = '{"challenge_id":"'+str(last_id)+'","content":"'+content_string+'","type":"regex","data":""}'
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

def check_token():
  check_token_result = {}

  with requests.Session() as check_token_session:
    check_token_session.headers.update({"Authorization": f"Token {token}"})
    check_token_result = check_token_session.get(f"{url}/api/v1/users/1",headers={"Content-Type": "application/json"})
  if check_token_result.status_code == 200:
    pass
  else:
    print('[e] Cannot access CTFd api, please check token or IP settings')
    exit()

if __name__ == "__main__":
  token = "ecf6ddb1175aff108aae66d4c136035b7abc7e4c432bd2865af6650f1993881"
  url = "http://209.114.126.72" 

  check_token()

  if os.path.isfile('birth_month_record.csv') == False:
    with open("birth_month_record.csv",'w',newline='') as birth_month_record:
      col_names = ['full_name_used','birth_month','challenge_added','challenge_number']
      writer = csv.DictWriter(birth_month_record, fieldnames=col_names)

      writer.writeheader()
      birth_month_record.close()
  else:
    pass

  if does_challenge_exist() == 0:
    birthmonth_challenge()
  else:
    exit()
