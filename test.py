import csv

# def birthmonth_challenge(url,token):
#   with open("users_info_record.csv") as users_info_record:
#     user_info_dictreader = csv.DictReader(users_info_record)
#     ids=[]
#     full_name=[]
#     birth_month=[]
#     for col in user_info_dictreader:
#       ids.append(col['id'])
#       full_name.append(col['field_1_value'])
#       birth_month.append(col['field_2_value'])
#     users_info_record.close()
    
#   challenge_flag = random.choice.list(birth_month)
#   picked_id = []
#   picked_full_name = []
#   picked_birth_month = []
  
#   for n in range(len(ids)):
#     if birth_month[n] == challenge_flage:
#       picked_id.append(ids[n])
#       picked_full_name.append(full_name[n])
#       picked_birth_month.append(birth_month[n])
#     else:
#       pass
    
#   with open("birth_month_record.csv",'a') as birth_month_record:
#     col_names = ['id', 'user_name','user_hex','paired_name','paired_hex','xor_result','challenge_exist','challenge_number']
#     writer = csv.DictWriter(birth_month_record, fieldnames=col_names)

#     for n in range(len(ids)):
#       if does_challenge_exist(n+1) == True:
#         print("[+] Challenge already exist, skip.")
#         pass
#       elif does_challenge_exist(n+1) == False:
#         if add_new_challenge(url,token,full_name[n],paired_name[n],xor_result[n],str(int(n)+1)) is True:
#           row="{'id':'"+ids[n]+"', 'user_name':'"+full_name[n]+"','user_hex':'"+user_hex[n]+"','paired_name':'"+paired_name[n]+"','paired_hex':'"+paired_hex[n]+"','xor_result':'"+xor_result[n]+"','challenge_exist':'yes','challenge_number':'"+str(int(n)+1)+"'}"
#           row_dict = ast.literal_eval(row)
#           writer.writerow(row_dict)
#           row=''
#         else:
#           pass

# def does_challenge_exist(n):
#   flag1 = ''
#   flag2 = 'no'
#   check_existence = requests.Session()
#   check_existence.headers.update({"Authorization": f"Token {token}"})
#   challenge_result = check_existence.get(f"{url}/api/v1/challenges",json='').json()
#   # print(n)
#   for name in challenge_result['data']:
#     if name['name'] == "Who was born in this month "+str(n):
#       flag1 = "yes"
#       break
#     else:
#       flag1 = "no"
#       pass
#   check_existence.close()
#   if flag1 == flag2:
#     return False
#   elif flag1 != flag2:
#     return True

def does_challenge_exist(url,token):
  flag = 0

  check_existence = requests.Session()
  check_existence.headers.update({"Authorization": f"Token {token}"})
  challenge_result = check_existence.get(f"{url}/api/v1/challenges",json='').json()

  for name in challenge_result['data']:
    if name['name'] == "Who was born in this month 2":
      check_existence.close()
      return 2
    elif name['name'] == "Who was born in this month 1":
      check_existence.close()
      return 1
    else:
      check_existence.close()
      return 0
def choose_a_month():
  month_used = []
  with open("birth_month_record.csv",'a') as month_record:
    month_dicreader = csv.DictReader(month_record)
    for col in month_dictreader:
      month_used = col[birth_month]
  return True
  return False

def add_birthmonth_challenge(url,token):
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
  
  if len(ids) < 3:
    exit()
  else:
    challenge_flag = random.choice.list(birth_month)
    picked_id = []
    picked_full_name = []
    picked_birth_month = []

    for n in range(len(ids)):
      if birth_month[n] == challenge_flag:
        picked_id.append(ids[n])
        picked_full_name.append(full_name[n])
        picked_birth_month.append(birth_month[n])
      else:
        pass

    with open("birth_month_record.csv",'a') as birth_month_record:
      col_names = ['full_name','birth_month','challenge_exist','challenge_number']
      writer = csv.DictWriter(birth_month_record, fieldnames=col_names)

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

if __name__ == "__main__":
  token = "3faf06e19cc198608a2aa9c5ee1f736f93f6c29e8f92bd633dfc4b3af5900e96"
  url = "http://209.114.126.34"

  if os.path.isfile('birth_month_record.csv') == False:
      with open("birth_month_record.csv",'w',newline='') as birth_month_record:
        col_names = ['full_name','birth_month','challenge_exist','challenge_number']
        writer = csv.DictWriter(birth_month_record, fieldnames=col_names)

        writer.writeheader()
        birth_month_record.close()
  else:
    pass

  number_of_exist_challenge = does_challenge_exist(url,token)

  if number_of_exist_challenge < 2:
    add_birthmonth_challenge(url,token,number_of_exist_challenge)
  else:
    exit()


