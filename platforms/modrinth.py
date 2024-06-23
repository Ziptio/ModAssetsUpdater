import json

import requests

from platforms.platform import Platform

modrinth_api = "https://api.modrinth.com/v2/project/"


class Modrinth(Platform):

    def __init__(self, platform_id, auth_token):
        super().__init__(platform_id, auth_token)

    def get_mod_body(self, mod_body: dict[str, str]):
        for mod_id in mod_body.keys():
            r = requests.get(modrinth_api + mod_id)
            if r.ok:
                json_data = r.json()
                if 'body' in json_data:
                    mod_body[mod_id] = json_data['body']
            else:
                print("Failed to get modrinth body for: `" + mod_id + "` - status code: `" + str(r.status_code) +
                      "` - error: `" + r.text + "`")

    def set_mod_body(self, mod_body: dict[str, str], auth_token: str):
        headers = {'Authorization': auth_token, 'content-type': 'application/json'}
        for mod_id, body in mod_body.items():
            if body:
                r = requests.patch(modrinth_api + mod_id, json.dumps({'body': body}), headers=headers)
                if r.ok:
                    print("Successfully updated modrinth body for: `" + mod_id + "`")
                else:
                    print("Failed to update modrinth body for: `" + mod_id + "` - status code: `" +
                          str(r.status_code) + "` - error: `" + r.text + "`")
