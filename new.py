import requests,json

def count_coordination():
  count = 0
  with requests.Session() as check_existence:
    check_existence.headers.update({"Authorization": f"Token {token}"})
    challenge_result = check_existence.get(f"{url}/api/v1/challenges",json='').json()
    # print(n)
    for name in challenge_result['data']:
      if "XOR Challenge" in name['name']:
        count+=1
      elif "Birth Month" in name['name']:
        count+=1

  print(count)
  update_points()

def update_points():
  print('done')

if __name__ == "__main__":
  token = "099b06d2394093117dfd53ca9e01f23a9437fda5579bdd82a317861740f1b35f"
  url = "http://209.114.126.86"

  count_coordination()
