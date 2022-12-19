import requests
import sys


def main():
    token = "4fb4c02d643f6667f2d187eb62c081f3b1e0e987978b896d9c1f4ab557db285f"
    url = "http://209.114.126.63"
    url = url.strip("/")
    s = requests.Session()
    s.headers.update({"Authorization": f"Token {token}"})

    # NOTE: If you wish for the user's credentials to be emailed to them, pass the
    # notify=true parameter in the URL. For example: /api/v1/users?notify=true
    r = s.post(
        f"{url}/api/v1/challenges",
        json={"name":"XOR Challenge 2","category":"Coordination","description":"Retrieve \"**Tom**\" and \"**Ashley**\"'s secret  8-bit number\r\n\r\nReturn the XOR of these two binary sequences.\r\n\r\nThe flag is in the format:``flag{01010101}``\r\n\r\nplease use private one-on-one chat function.","value":"23","state":"hidden","type":"standard"},
    )
    print(r.json())


if __name__ == "__main__":
    main()
