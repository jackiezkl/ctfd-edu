import requests,sys,json,csv,random,os

def generate_hex():
  hex_array = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']

  higherbits = random.randint(0,15)
  lowerbits = random.randint(0,15)
  fullbits = hex_array[higherbits] + hex_array[lowerbits]
#   first_binary = (bin(int(first_fullbits, 16))[2:].zfill(8))
#   higherbits = random.randint(0,15)
#   lowerbits = random.randint(0,15)
#   second_fullbits = hex_array[higherbits] + hex_array[lowerbits]
#   second_binary = (bin(int(second_fullbits, 16))[2:].zfill(8))
#   xor_result = (bin(int(first_fullbits, 16) ^ int(second_fullbits, 16))[2:].zfill(8))
  return fullbits

def create_code_assign_record(url,token):
  if os.path.isfile('code_assign_record.csv') == False:
    code_assign_csv = open('code_assign_record.csv', 'w', newline='')

    code_assign_csv.write('ID,Full Name,Birth Month,User Binary,Paired Name,Paired Binary,XOR Result\n')
    print("[+] Code assign record file does not exist, file created.")
    print("[+] Filling file content...")

    userinfo_session = requests.Session()
    userinfo_session.headers.update({"Authorization": f"Token {token}"})
    with open("names_record.csv") as names_record:
      heading = next(names_record)

      names_reader = csv.reader(names_record)
      for line in names_reader:
        try:
          user_info = userinfo_session.get(f"{url}/api/v1/users/{line[1]}",headers={"Content-Type": "application/json"}).json()
          user_full_name,user_birth_month = user_info['data']['fields'][0]['value'],user_info['data']['fields'][1]['value']
          fullbits = generate_hex()
          code_assign_csv.write('%s,%s,%s,%s,%s,%s,%s\n' % (line[1],user_full_name,user_birth_month,fullbits,'','',''))
        except Exception:
          continue
  else:
    print("[+] File already exist, checking information...")
    ids = []
    with open("code_assign_record.csv") as code_assign:
      code_assign_reader = csv.DictReader(code_assign)

      for col in code_assign_reader:
        ids.append(col['ID'])
      code_assign.close()

    with open("names_record.csv") as names_record:
      heading = next(names_record)
      names_reader = csv.reader(names_record)
      code_assign_csv = open('code_assign_record.csv', 'a')
      userinfo_session = requests.Session()
      userinfo_session.headers.update({"Authorization": f"Token {token}"})
      for line in names_reader:
        if line[1] in ids:
          pass
        else:
          try:
            user_info = userinfo_session.get(f"{url}/api/v1/users/{line[1]}",headers={"Content-Type": "application/json"}).json()
            user_full_name,user_birth_month = user_info['data']['fields'][0]['value'],user_info['data']['fields'][1]['value']
            fullbits = generate_hex()
            code_assign_csv.write('%s,%s,%s,%s,%s,%s,%s\n' % (line[1],user_full_name,user_birth_month,fullbits,'','',''))
          except Exception:
            continue


def create_xor_record():
  csv = open('xor_record.csv', 'w', newline='')

  csv.write('Name1,code1,name2,code2,XOR\n')
  print("[+] Created XOR record file: xor_record.csv")
  csv.close()

def get_usernames(url):
  csv = open('names_record.csv', 'w', newline='')

  csv.write('User Name, id\n')
  print("[+] Created username record file: names_record.csv")

  username_session = requests.Session()
  all_user_info_json = username_session.get(f"{url}/api/v1/users").json()
  total_number_of_users = all_user_info_json['meta']['pagination']['total']

  for i in range(total_number_of_users):
    csv.write('%s,%s\n' % (all_user_info_json['data'][i]['name'],all_user_info_json['data'][i]['id']))

  csv.close()
  print("[+] Saved to names_record.csv")

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

  get_usernames(url)
  create_code_assign_record(url,token)
  
#   add_new_challenge(url,token)
