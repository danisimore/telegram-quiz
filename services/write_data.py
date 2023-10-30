import json


def write_json(user_data: dict, username) -> None:
    with open("data/users_statistic.json", "rt", encoding="utf-8") as data_file:
        data = json.load(data_file)

    data[username] = {
        "correct_answers": user_data[username]["correct_answers"],
        "incorrect_answers": user_data[username]["incorrect_answers"],
    }

    with open("data/users_statistic.json", "wt", encoding="utf-8") as data_file:
        json.dump(data, data_file, indent=4)
