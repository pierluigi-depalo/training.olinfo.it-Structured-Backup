import requests
import json

def get_task_number():
    response = requests.post("https://training.olinfo.it/api/task", json={"first": 0, "last": 0, "action": "list"}).text
    number_str = json.loads(response)["num"]
    return int(number_str)

def get_all_tasks_response(total):
    return requests.post("https://training.olinfo.it/api/task", json={"first": 0, "last": total+1, "action": "list"})

def get_all_tasks():
    total = get_task_number()
    tasks_response = get_all_tasks_response(total)
    tasks_json = tasks_response.text
    tasks_json = json.loads(tasks_json)["tasks"]
    return tasks_json

def load_training_tasks_to_check():
    wanted_fields = ["title"]

    tasks_json = get_all_tasks()

    tasks = {}

    for t in tasks_json:
        id = t["name"]
        tasks[id] = {}
        for field in wanted_fields:
            tasks[id][field] = t[field]
        tasks[id]["checked"] = False

    return tasks

def load_training_tasks_list():
    wanted_fields = ["name", "title"]

    tasks_json = get_all_tasks()

    tasks = {}

    for t in tasks_json:
        tasks[t["name"]] = {}
        for field in wanted_fields:
            tasks[t["name"]][field] = t[field]

    return tasks

def save_on_file(all_task_path, all_task_raw_path):
    f = open(all_task_path, "w")
    f.write(json.dumps(load_training_tasks_to_check(), indent=4))
    f.close()

    f = open(all_task_raw_path, "w")
    f.write(json.dumps(load_training_tasks_list(), indent=4))
    f.close()

def load(directory, save_file = False):
    ALL_TASK_PATH = directory + "all_tasks.json"
    ALL_TASK_RAW_PATH = directory + "all_tasks_raw.json"
    if save_file:
        save_on_file(all_task_path=ALL_TASK_PATH, all_task_raw_path=ALL_TASK_RAW_PATH)
    else:
        return {"all": load_training_tasks_to_check(), "all_raw" : load_training_tasks_list()}

if __name__ == "__main__":
    load("./")