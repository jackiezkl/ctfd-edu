import random,json,requests,string


def add_new_user(username,email,fullname,birthmonth):
  with requests.Session() as update_session:
    update_session.headers.update({"Authorization": f"Token {token}"})
    content_string = ''

    payload = '{"name":"'+username+'","email":"'+email+'","password":"passtest","type":"user","verified":false,"hidden":false,"banned":false,"fields":[{"field_id":1,"value":"'+fullname+'"},{"field_id":2,"value":"'+birthmonth+'"}]}'
    # print(payload)
    flag_result = update_session.post(f"{url}/api/v1/users",json=json.loads(payload)).json()

    if flag_result['success'] == True:
      print(f"user {username} added")
    else:
      print("[e] Error when adding new user.")


if __name__ == "__main__":
  token = "15c288f2a166e3cef2ebb182a007212e747947aae7ff55fe103bcbb7f1695e2a"
  url = "http://209.114.126.86"


  while True:
    try:
      userinput = input("Please enter how many user do you want to create?\n")
      number = int(userinput) + 1
      break
    except Exception:
      continue

  months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


  for i in range(1,number):
    username = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=5))
    email = f"{username}@gmail.com"
    fullname = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=5))+" "+''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=5))
    birthmonth = random.choice(months)
    add_new_user(username,email,fullname,birthmonth)

