import csv

def does_challenge_exist():
  flag = 0

  with requests.Session() as check_existence:
  check_existence.headers.update({"Authorization": f"Token {token}"})
  challenges_list = check_existence.get(f"{url}/api/v1/challenges",json='').json()

  for challenge in challenges_list['data']:
    if challenge['name'] == "Birth Month 2":
      return 2
    elif challenge['name'] == "Birth Month 1":
      return 1
    else:
      return 0

def birthmonth_challenge(number_of_exist_challenge):
  with open("users_info_record.csv") as users_info_record:
    user_info_dictreader = csv.DictReader(users_info_record)
    ids=[]
    full_name=[]
    birth_month=[]
    for col in user_info_dictreader:
      ids.append(col['id'])
      full_name.append(col['field_1_value'])
      birth_month.append(col['field_2_value'])
    users_info_record.close()

  with open("birth_month_record.csv",'a') as month_record:
    month_used = []
    month_dicreader = csv.DictReader(month_record)
    for col in month_dictreader:
      month_used.append(col[birth_month])
    month_record.close()

  if len(set(birth_month)) < 3:
    exit()
  elif len(set(month_used)) == 2:
    exit()
  elif len(set(month_used)) == 1:
    while True:
      month_to_add = random.choice(set(birth_month))
      if month_to_add == month_used[0]:
        continue
      else:
        break
    picked_id = []
    picked_full_name = []
    picked_birth_month = []

    for n in range(len(ids)):
      if birth_month[n] == month_to_add:
        picked_id.append(ids[n])
        picked_full_name.append(full_name[n])
        picked_birth_month.append(birth_month[n])
      else:
        pass

    with open("birth_month_record.csv",'a') as birth_month_record:
      col_names = ['first_name','birth_month','challenge_exist','challenge_number']
      birth_month_writer = csv.DictWriter(birth_month_record, fieldnames=col_names)

    if does_challenge_exist() == 1:
      if add_new_challenge(picked_id,picked_full_name,picked_birth_month,2) is True:
        row="{'id':'"+ids[n]+"', 'user_name':'"+full_name[n]+"','user_hex':'"+user_hex[n]+"','paired_name':'"+paired_name[n]+"','paired_hex':'"+paired_hex[n]+"','xor_result':'"+xor_result[n]+"','challenge_exist':'yes','challenge_number':'"+str(int(n)+1)+"'}"
        row_dict = ast.literal_eval(row)
        birth_month_writer.writerow(row_dict)
        row=''
      else:
        pass
    elif does_challenge_exist(n+1) == 2 or does_challenge_exist(n+1) == 0:
      print("[+] Something's wrong. There should be only one birth month challenge; however, the record shows a different number.")
      pass
  elif len(set(month_used)) == 0:
    
  else:

def get_last_created_id(,n):
  id_check_session = requests.Session()
  id_check_session.headers.update({"Authorization": f"Token {token}"})
  id_check_result = id_check_session.get(f"{url}/api/v1/challenges",headers={"Content-Type": "application/json"}).json()
  for name in id_check_result['data']:
    if name['name'] == 'Birth Month '+n:
      id_check_session.close()
      return name['id']
    else:
      pass

# add new birth month challenges
def add_new_birth_challenge(picked_id,picked_full_name,picked_birth_month,n):
  update_session = requests.Session()
  update_session.headers.update({"Authorization": f"Token {token}"})
  payload = '{"name":"Birth Month "'+n+',"category":"Coordination","description":"There should be at least one player that was born in '+picked_birth_month+'. Could you provide the first name of at least one?\\r\\nEnter their first name as the flag.","value":"34","state":"visible","type":"standard"}'
  challenge_result = update_session.post(f"{url}/api/v1/challenges",json=json.loads(payload)).json()
  add_challenge_result = challenge_result['success']
  update_session.close()

  last_id = get_last_created_id(n)

  result = add_new_birth_flag(last_id,picked_full_name,picked_birth_month,add_challenge_result)
  return result

# add corresponding birth month flags
def add_new_birth_flag(last_id,last_id,picked_full_name,picked_birth_month,add_challenge_result):
  update_session = requests.Session()
  update_session.headers.update({"Authorization": f"Token {token}"})
  content_string = ''

  for names in picked_full_name:
    content_string = content_string+"|"+names.split()[0]

  content_string = '('+content_string.lstrip('|')+')'

  if add_challenge_result == True:
    payload = '{"challenge_id":"'+str(last_id)+'","content":"'+content_sctring+'","type":"static","data":""}'
    print(payload)
    flag_result = update_session.post(f"{url}/api/v1/flags",json=json.loads(payload)).json()

    if flag_result['success'] == True:
      update_session.close()
      print("[+] New birth month challenge and flag added.")
      return True
    else:
      update_session.close()
      print("[+] Error when adding flag.")
      return False
  else:
    update_session.close()
    print("[+] Error when adding challenge.")
    return False
  

if __name__ == "__main__":
  token = "3faf06e19cc198608a2aa9c5ee1f736f93f6c29e8f92bd633dfc4b3af5900e96"
  url = "http://209.114.126.34"

  if os.path.isfile('birth_month_record.csv') == False:
      with open("birth_month_record.csv",'w',newline='') as birth_month_record:
        col_names = ['first_name','birth_month','challenge_exist','challenge_number']
        writer = csv.DictWriter(birth_month_record, fieldnames=col_names)

        writer.writeheader()
        birth_month_record.close()
  else:
    pass

  number_of_exist_challenge = does_challenge_exist()

  if number_of_exist_challenge < 2:
    birthmonth_challenge(number_of_exist_challenge)
  else:
    exit()
