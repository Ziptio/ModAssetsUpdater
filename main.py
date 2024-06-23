import os
import json
from os import environ

from platforms.curseforge import Curseforge
from platforms.modrinth import Modrinth

github_repo = "ModdersAgainstBlockers"
platforms = [Modrinth("modrinth", "MODRINTH_TOKEN")] # Curseforge("curseforge")


def create_replacement_dict():
    domain = f"https://{github_repo}.github.io/"
    replacements = []
    payload = environ.get('PAYLOAD')
    print("type0:" + str(type(payload)))
    print("0: " + str(payload))
    custom_data = json.loads(payload)
    print("type1:" + str(type(custom_data)))
    print("1:" + str(custom_data))
    if 'data' in custom_data:
        data_list = custom_data['data']
        print("type2:" + str(type(data_list)))
        print("2:" + str(data_list))
        for data in data_list:
            to = domain + data['to']
            replacements[data['from']] = to
            if 'last_to' in data:
                replacements[data['last_to']] = to
    return replacements


def main():
    repo_path = '.'
    data_path = os.path.join(repo_path, 'data')

    platform_mods = {}
    for platform in platforms:
        platform_data = os.path.join(data_path, platform.id + '.json')
        if os.path.exists(platform_data):
            with open(platform_data, 'r') as f:
                data = json.load(f)
                if 'ids' in data:
                    platform_mods[platform] = data['ids']
                else:
                    print("No Id's found: " + platform_data)  # TODO: temp
        else:
            print("Missing file: " + platform_data)  # TODO: temp

    if len(platform_mods) == 0:
        print("No mods where found!")
        return

    # Get all mod bodies
    mod_body = {}
    for platform in platforms:
        platform_mod_body = {}
        for mod_id in platform_mods[platform]:
            platform_mod_body[mod_id] = ""
        platform.get_mod_body(platform_mod_body)
        mod_body[platform] = platform_mod_body

    # Create replacements dict
    replacements = create_replacement_dict()

    changes = {}

    # Apply all replacements
    for platform in platforms:
        changes[platform] = {}
        for mod_id, body in mod_body[platform].items():
            new_body = body
            for start, to in replacements:
                new_body = new_body.replace(start, to)
            if new_body != body:
                changes[platform][mod_id] = new_body

    if len(changes) == 0:
        print("No changes made!")
        return

    # Upload changed bodies
    for platform, change in changes.items():
        auth_token = environ.get(platform.auth_token)
        if auth_token is None:
            print("Auth token not found! - " + platform.id)
        platform.set_mod_body(change, auth_token)

    print(str(len(changes)) + " bodies where changed!")


if __name__ == '__main__':
    main()
