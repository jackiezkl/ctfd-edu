import csv

def birthmonth_challenge(url,token):
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
    
    random.choice.list(birth_month)
if __name__ == "__main__":
  token = "3faf06e19cc198608a2aa9c5ee1f736f93f6c29e8f92bd633dfc4b3af5900e96"
  url = "http://209.114.126.34"
  birthmonth_challenge(url,token)
