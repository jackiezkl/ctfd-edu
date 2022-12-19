import requests
import sys


def main():
    token = "4fb4c02d643f6667f2d187eb62c081f3b1e0e987978b896d9c1f4ab557db285f"
    url = "http://209.114.126.63"
    url = url.strip("/")
    s = requests.Session()
    s.headers.update({"Authorization": f"Token {token}"})

    r = s.post(
        f"{url}/api/v1/challenges",
        json={"name":"XOR Challenge 4",
              "category":"Coordination",
              "description":"Retrieve \"**Tom**\" and \"**Ashley**\"'s secret  8-bit number\r\n\r\nReturn the XOR of these two binary sequences.\r\n\r\nThe flag is in the format:``flag{01010101}``\r\n\r\nplease use private one-on-one chat function.\r\n",
              "connection_info":"",
              "value":"23",
              "max_attempts":"0",
              "state":"visible"},
    )

#     s.post(
#         f"{url}/api/v1/flags",
#         json={"challenge_id":"2","content":"20101010","type":"static","data":""},
#     )
    
#     s.post(
#         f"{url}/api/v1/challenges/2",
#         json={"state":"visible"},
#     )

if __name__ == "__main__":
    main()
