import os,requests,json

token = "15c288f2a166e3cef2ebb182a007212e747947aae7ff55fe103bcbb7f1695e2a"
url = "http://209.114.126.86"

current_path=os.getcwd()
parent_path = os.path.dirname(current_path)+"/"
relative_path = "CTFd/CTFd/plugins/ctfd-auto-scoreboard/assets/challenge_dict.txt"
dst_path = os.path.join(parent_path, relative_path)

challenge_dict = {
  1: ['Flag in a Flag System', '70', 'Analysis'],
  2: ['We are being attacked!', '42', 'Analysis'],
  3: ["Hope it's not a Backdoor", '25', 'Analysis'],
  4: ['Further Attack 1', '40', 'Analysis'],
  5: ['Further Attack 2', '40', 'Analysis'],
  6: ['A File Was Stolen', '45', 'Analysis'],
  7: ['Encoded Message', '25', 'Analysis'],
  8: ['Cryptocurrency Audit', '70', 'Analysis'],
  9: ['Steganography 1', '40', 'Analysis'],
  10: ['Risk Management ROI', '10', 'Analysis'],
  11: ['Lightning Show', '70', 'Analysis'],
  12: ['Vulnerability Test 5', '23', 'Analysis'],
  13: ['Draw a Lock', '40', 'Design'],
  14: ['Draw Your Favorite Animal', '50', 'Design'],
  15: ['Firewall 1', '26', 'Design'],
  16: ['Firewall 2', '26', 'Design'],
  17: ['Firewall 3', '26', 'Design'],
  18: ['Firewall 4', '25', 'Design'],
  19: ['Incident Response Actions', '60', 'Design'],
  20: ['Incident Response Ordering', '50', 'Design'],
  21: ["Prisoner's Dilemma", '90', 'Design'],
  22: ['Remove the Hacker', '60', 'Design'],
  23: ['Steganography 2', '25', 'Design'],
  24: ['System Development Life Cycle', '22', 'Design'],
  25: ['Hardware Encryption', '60', 'Implementation'],
  26: ['Determining User Inputs', '60', 'Implementation'],
  27: ['Linux Basics 1', '20', 'Implementation'],
  28: ['Linux Basics 2', '20', 'Implementation'],
  29: ['Linux Basics 3', '20', 'Implementation'],
  30: ['Linux Basics 4', '20', 'Implementation'],
  31: ['Linux Basics 5', '20', 'Implementation'],
  32: ['Linux Basics 6', '35', 'Implementation'],
  33: ['Linux Basics 7', '21', 'Implementation'],
  34: ['Linux Basics 8', '21', 'Implementation'],
  35: ['Windows Basics 1', '20', 'Implementation'],
  36: ['Windows Basics 2', '21', 'Implementation'],
  37: ['Windows Basics 3', '21', 'Implementation'],
  38: ['Windows Basics 4', '21', 'Implementation'],
  39: ['Windows Basics 5', '21', 'Implementation'],
  40: ['Windows Basics 6', '21', 'Implementation'],
  41: ['Windows Basics 7', '21', 'Implementation'],
  42: ['Windows Basics 8', '35', 'Implementation'],
  43: ['Vulnerability Test 1', '22', 'Implementation'],
  44: ['In need of ...', '10', 'Investigation'],
  45: ['Name the Attack 1', '23', 'Investigation'],
  46: ['Name the Attack 2', '24', 'Investigation'],
  47: ['Name the Attack 3', '24', 'Investigation'],
  48: ['Name the Attack 4', '26', 'Investigation'],
  49: ['Name the Attack 5', '26', 'Investigation'],
  50: ['Name the Attack 6', '26', 'Investigation'],
  51: ['Name the Attack 7', '26', 'Investigation'],
  52: ['Name this Software 1', '24', 'Investigation'],
  53: ['Name this Software 2', '24', 'Investigation'],
  54: ['Name this Software 3', '24', 'Investigation'],
  55: ['Name this Software 4', '24', 'Investigation'],
  56: ['Name this Software 5', '24', 'Investigation'],
  57: ['Name this Software 6', '26', 'Investigation'],
  58: ['Name this Software 7', '24', 'Investigation'],
  59: ['Reverse Image Search', '100', 'Investigation'],
  60: ['Historical Event', '45', 'Investigation'],
  61: ['Program Review', '20', 'Testing and Evaluation'],
  62: ['Mystery JavaScript 1', '50', 'Testing and Evaluation'],
  63: ['Mystery JavaScript 2', '55', 'Testing and Evaluation'],
  64: ['If you know, you know', '28', 'Testing and Evaluation'],
  65: ['Networking 1', '24', 'Testing and Evaluation'],
  66: ['Networking 2', '24', 'Testing and Evaluation'],
  67: ['Regular Expressions 1', '30', 'Testing and Evaluation'],
  68: ['Regular Expressions 2', '33', 'Testing and Evaluation'],
  69: ['Regular Expressions 3', '40', 'Testing and Evaluation'],
  70: ['Regular Expressions 4', '50', 'Testing and Evaluation'],
  71: ['Firewall 5', '24', 'Testing and Evaluation'],
  72: ['Linux Basics 9', '24', 'Testing and Evaluation'],
  73: ['Simple Testing Server', '36', 'Testing and Evaluation'],
  74: ['Vulnerability Test 2', '24', 'Testing and Evaluation'],
  75: ['Vulnerability Test 3', '24', 'Testing and Evaluation'],
  76: ['Vulnerability Test 4', '24', 'Testing and Evaluation'],
  77: ['The Background', '5', 'Introduction'],
  78: ['Introduction', '5', 'Introduction']
}
cid = 79
while True:
  try:
    with requests.Session() as check_existence:
      check_existence.headers.update({"Authorization": f"Token {token}"})
      challenge_result = check_existence.get(f"{url}/api/v1/challenges/{cid}",json='').json()

      challenge_name = challenge_result['data']['name']
      challenge_value = str(challenge_result['data']['value'])
      challenge_category = challenge_result['data']['category']
      challenge_dict.update({cid:[challenge_name,challenge_value,challenge_category]})
  except Exception:
    break
  cid+=1

with open(dst_path, 'w') as dictfile: 
  try:
    dictfile.write(challenge_dict)
    print("[+] challenge_dict file updated.")
  except Exception:
    print("Couldn't write the challenge_dict file.")
# print(challenge_dict)
