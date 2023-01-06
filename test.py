import csv,requests,time

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
    user_birth_months=[]
    for col in user_info_dictreader:
      ids.append(col['id'])
      full_name.append(col['field_1_value'])
      user_birth_months.append(col['field_2_value'])

  with open("birth_month_record.csv",'a') as month_record:
    name_used = []
    month_used = []
    month_dicreader = csv.DictReader(month_record)
    for col in month_dictreader:
      name_used.append(col[birth_month])
      month_used.append(col[birth_month])

  if len(set(user_birth_months)) < 3:
    exit()
  elif len(set(month_used)) == 2:
    exit()
  elif len(set(month_used)) == 0:
    month_to_add = random.sample(set(user_birth_months),k=2)

    picked_id = []
    picked_full_name = []
    picked_birth_month = []

    for i in range(2):
      for n in range(len(ids)):
        if user_birth_months[n] == month_to_add[i]:
          picked_id.append(ids[n])
          picked_full_name.append(full_name[n])
          picked_birth_month.append(user_birth_months[n])
        else:
          pass

    with open("birth_month_record.csv",'a') as birth_month_record:
      col_names = ['full_name_used','birth_month','challenge_exist','challenge_number']
      birth_month_writer = csv.DictWriter(birth_month_record, fieldnames=col_names)

    # if does_challenge_exist() == 1:
    for birth_challenge_number in range(1,3)
      if add_new_challenge(picked_id,picked_full_name,picked_birth_month,birth_challenge_number) is True:
        for n in range(len(picked_id))
          row="{'full_name_used':'"+picked_full_name[n]+"','birth_month':'"+picked_birth_month+"','challenge_exist':'yes','challenge_number':'"+birth_challenge_number+"'}"
          row_dict = ast.literal_eval(row)
          birth_month_writer.writerow(row_dict)
          row=''
      else:
        pass
  # elif len(set(month_used)) == 1:
  #   while True:
  #     month_to_add = random.sample(set(user_birth_months),k=1)
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
    print('There is 1 esixting birth month challenge, I cannot handle this situation. I believe an error happened last time, pelase remove the birth_month_record.csv file, and run this program again.')
    pass
def get_last_created_id(n):
  id_check_session = requests.Session()
  id_check_session.headers.update({"Authorization": f"Token {token}"})
  id_check_result = id_check_session.get(f"{url}/api/v1/challenges",headers={"Content-Type": "application/json"}).json()
  for name in id_check_result['data']:
    if name['name'] == 'Birth Month '+n:
      id_check_session.close()
      return name['id']
    else:
      pass
  pass
# add new birth month challenges
def add_new_birth_challenge(picked_id,picked_full_name,picked_birth_month,n):
  with requests.Session() as update_session:
    update_session.headers.update({"Authorization": f"Token {token}"})
    payload = '{"name":"Birth Month "'+n+',"category":"Coordination","description":"There should be at least one player that was born in '+picked_birth_month+'. Could you provide the first name of at least one?\\r\\nEnter their first name as the flag.","value":"34","state":"visible","type":"standard"}'
    challenge_result = update_session.post(f"{url}/api/v1/challenges",json=json.loads(payload)).json()
    add_challenge_result = challenge_result['success']

  last_id = get_last_created_id(n)

  result = add_new_birth_flag(last_id,picked_full_name,picked_birth_month,add_challenge_result)
  return result

# add corresponding birth month flags
def add_new_birth_flag(last_id,picked_full_name,picked_birth_month,add_challenge_result):
  with requests.Session() as update_session:
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
        print("[+] New birth month challenge and flag added.")
        return True
      else:
        print("[+] Error when adding flag.")
        return False
    else:
      print("[+] Error when adding challenge.")
      return False
  

if __name__ == "__main__":
  token = "ecf6ddb1175aff108aae66d4c136035b7abc7e4c432bd2865af6650f19938812"
  url = "http://209.114.126.72" 

  if os.path.isfile('birth_month_record.csv') == False:
    with open("birth_month_record.csv",'w',newline='') as birth_month_record:
      col_names = ['full_name_used','birth_month','challenge_exist','challenge_number']
      writer = csv.DictWriter(birth_month_record, fieldnames=col_names)

      writer.writeheader()
      birth_month_record.close()
  else:
    pass

  if does_challenge_exist() < 2:
    birthmonth_challenge(number_of_exist_challenge)
  else:
    exit()