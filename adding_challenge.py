import requests,sys,json,csv,random

def generate_binary():
  hex_array = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']

  i = random.randint(0,15)
  j = random.randint(0,15)
  first_binary = (bin(int(hex_array[i], 16))[2:].zfill(4))
  second_binary = (bin(int(hex_array[j], 16))[2:].zfill(4))
  xor_result = (bin(int(hex_array[i], 16) ^ int(hex_array[j], 16))[2:].zfill(4))
  return first_binary

# def create_code_assign_record():
#   csv = open('code_assign_record.csv', 'w', newline='')

#   csv.write('Name,code\n')
#   print("[+] Created code assign record file: code_assign_record.csv")
#   csv.close()

def create_xor_record():
  csv = open('xor_record.csv', 'w', newline='')

  csv.write('Name1,code1,name2,code2,XOR\n')
  print("[+] Created XOR record file: xor_record.csv")
  csv.close()

def get_usernames(url):
  csv = open('code_assign_record.csv', 'w', newline='')

  csv.write('Name,code\n')
  print("[+] Created code assign record file: code_assign_record.csv")
  
  username_session = requests.Session()
  all_user_info_json = username_session.get(f"{url}/api/v1/users").json()
  total_number_of_users = all_user_info_json['meta']['pagination']['total']

  for i in range(total_number_of_users):
    csv.write('%s,%s\n' % (all_user_info_json['data'][i]['name'],generate_binary())）

  csv.close()

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

#   create_code_assign_record()
#   create_xor_record()

  get_usernames(url)
#   add_new_challenge(url,token)
