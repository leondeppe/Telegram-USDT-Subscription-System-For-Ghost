import requests
from creds import *
import create_jwt_token as cjt


def add_member(member_data):
    headers = {
        'Authorization': f'Ghost {cjt.create_jwt_token(ADMIN_API_KEY)}',
        'Content-Type': 'application/json'
    }
    response = requests.post(GHOST_ADMIN_API_URL_MEMBERS, json={"members": [member_data]}, headers=headers)
    if response.status_code == 201:
        print("Member successfully added.")
    else:
        print(f"Error: {response.status_code} - {response.text}")


def main(mail):

    new_member = {
    "email": mail,
    "name": "New Member",
    "note": "Automatically authorised"
}
    add_member(new_member)
