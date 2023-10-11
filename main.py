import json
import os
from configparser import ConfigParser
import pandas as pd
from github import Github
from dataclasses import dataclass


def print_dict_content(dict_to_print):
    """for debugging"""
    for values in dict_to_print.values():
        print(values)


@dataclass
class ImportWebsites:
    url: str
    end: str  # placed at the end of the printed message
    table_names: tuple
    id_dict: dict
    debug_mode: bool

    def request_tables(self):
        tables = pd.read_html(self.url)  # Returns list of all tables on page.

        for counter, table in enumerate(tables):
            dict_table = table.to_dict('records')
            for entry in dict_table:
                has_name = 'Name' in entry and entry['Name'] == entry['Name']
                has_desc = 'Description' in entry and entry['Description'] == entry['Description']
                has_notes = 'Notes' in entry and entry['Notes'] == entry['Notes']

                self.id_dict[entry['ProgramId']] = \
                    (f"The ID {entry['ProgramId']} is part of the category \"{self.table_names[counter]}\". "
                     f"{f"It is described as \"{entry['Name']}\". " if has_name else ""}"
                     f"{f"It is described as \"{entry['Description']}\". " if has_desc else ""}"
                     f"{f"Note: {entry['Notes']}" if has_notes else ""}"
                     f"{"But there is no information about this ID." if not (has_name or has_desc or has_notes) else ""}"
                     f"{self.end if self.end else ""}")
        return self.id_dict


def print_user_list(title_id_dict, path, allow_path_input, allow_user_input):
    ids = []
    if allow_path_input:
        try:
            ids.extend(
                [folder_name for folder_name in os.listdir(path) if os.path.isdir(os.path.join(path, folder_name))])
        except FileNotFoundError:
            print(f"No such file or directory: {path}")
    if allow_user_input:
        ids.extend(get_user_input())

    for folder_name in ids:
        try:
            print(f"-> \"{title_id_dict[folder_name]}\" is the Name of \"{folder_name}\"")
        except KeyError:
            print(f"-> There is no known Name for \"{folder_name}\"")


def get_user_input():
    input_list = []
    print("Enter folder names/title ids one per line, leave empty to proceed")
    while True:
        user_input = input()
        if user_input:
            input_list.append(user_input)
        else:
            break
    return input_list


def main():
    # loading config
    config = ConfigParser()
    config.read('config.ini')
    path = config.get('config', 'path')
    allow_path_input = config.getboolean('config', 'allow_path_input')
    allow_user_input = config.getboolean('config', 'allow_user_input')
    obtain_data = config.getboolean('config', 'obtain_data')
    debug_mode = config.getboolean('config', 'debug_mode')

    if obtain_data:
        # obtain Homebrew sysmodules from ndeadly
        id_dict = {}
        raw_gist = Github().get_gist("a4b8c01bb453028cd0008f282098f696").raw_data['files']['sysmodules.txt']['content']
        for sysmodule in raw_gist.split("/* Homebrew sysmodules */\n")[-1].splitlines():
            l = sysmodule.split("	")
            id_dict[l[
                0]] = f"The ID {l[0]} is the ID for the Homebrew sysmodule {l[1]}. Check it out on GitHub for more information."
        # obtains Nintendo sysmodules from the switchbrew wiki
        id_dict = id_dict = ImportWebsites(
            url=r'https://switchbrew.org/wiki/Title_list/Games',
            end=f"Note: if this ID is in your /atmosphere/contents folder, the content is likely a mod.",
            table_names=(
                "Applications / Games", "Demos"),
            debug_mode=debug_mode,
            id_dict=id_dict).request_tables()
        id_dict = ImportWebsites(
            url=r'https://switchbrew.org/wiki/Title_list',
            end="",
            table_names=(
                "System Modules", "System Data Archives", "System Applets",
                "Development System Applets",
                "Debug System Modules", "Development System Modules", "Bdk System Modules",
                "New Development System Modules", "System Applications",
                "Pre-release System Applets",
                "Pre-release System Modules", "User Applications"),
            debug_mode=debug_mode,
            id_dict=id_dict).request_tables()
        if debug_mode:
            print_dict_content(id_dict)
        with open('title-ids.json', 'w') as fp:
            json.dump(id_dict, fp, indent=2)
    else:
        try:
            id_dict = json.load(open('title-ids.json'))
        except FileNotFoundError:
            print("The file title-ids.json could not be found. Please change \"obtain_data\" in \"config.ini\" to True.")
            return

    if allow_path_input or allow_user_input:
        print_user_list(id_dict, path, allow_path_input, allow_user_input)
    else:
        print("Allow at least one input type in the config")


if __name__ == '__main__':
    main()
