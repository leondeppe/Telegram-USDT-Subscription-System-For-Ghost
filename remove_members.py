import requests
import create_jwt_token as cjt
from creds import *


def get_member_id(email):
    headers = {
        'Authorization': f'Ghost {cjt.create_jwt_token(ADMIN_API_KEY)}',
        'Content-Type': 'application/json'
    }
    response = requests.get(GHOST_ADMIN_API_URL_MEMBERS, headers=headers)
    members = response.json()['members']

    for member in members:
        if member['email'] == email:
            return member['id']


def delete_member(member_id):
    url = f"{GHOST_ADMIN_API_URL_MEMBERS}{member_id}/"
    headers = {
        'Authorization': f'Ghost {cjt.create_jwt_token(ADMIN_API_KEY)}',
        'Content-Type': 'application/json'
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print("Member successfully removed.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def main(email_to_remove):
    member_id = get_member_id(email_to_remove)

    if member_id:
        delete_member(member_id)
    else:
        print("Member not found.")
