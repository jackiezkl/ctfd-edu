import requests
import sys


def main():
    try:
        url = sys.argv[1]
        token = sys.argv[2]
    except IndexError:
        print("Usage: python3 add_user.py <url> <admin_token>")
        sys.exit(1)

    # Create API Session
    url = url.strip("/")
    s = requests.Session()
    s.headers.update({"Authorization": f"Token {token}"})

    # NOTE: If you wish for the user's credentials to be emailed to them, pass the
    # notify=true parameter in the URL. For example: /api/v1/users?notify=true
    r = s.post(
        f"{url}/api/v1/users",
        json={"name":"user","email":"user@sampleuser.com","password":"user","type":"user","verified":False,"hidden":False,"banned":False,"fields":[]},
        headers={"Content-Type": "application/json"},
    )
    print(r.json())


if __name__ == "__main__":
    main()
