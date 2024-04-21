import requests
import getpass
import json
from pathlib import Path
from update_json import load_ois, load_oii, combine_jsons, load_training_tasks, check_evaluated
import os

ONLINE = False

def print_welcome():
    print("BENVENUTO")

def login():
    user = input("Username: ")
    pwd = getpass.getpass("Password: ")

    login_data = {
        "action": "login",
        "username": user,
        "password": pwd,
    }

    r = requests.post(
        'https://training.olinfo.it/api/user',
        headers={'Content-Type': 'application/json'},
        data=json.dumps(login_data)
    )

    d = r.json()

    if not d.get('success', False):
        print('Errore: username o password errati.')
        quit()
    
    cookie = r.headers.get('Set-Cookie', '').split(';')[0]
    key, value = cookie.split("=")
    
    return {
        "username": user,
        "cookie": {key: value},
    }

def get_file_url(hash_file, file_name):
    return f"https://training.olinfo.it/api/files/{hash_file}/{file_name}"

def get_problem_directory(competition, edition, match, problem):
    return Path(f"./downloaded/{competition}/{edition}/{match}/{problem}/")

def download_file(directory, file_name, file_digest):
    directory.mkdir(parents=True, exist_ok=True)
    file_url = get_file_url(file_digest, file_name)

    response = requests.get(file_url)
    if response.status_code == 200:
        with open(directory / file_name, "w") as file:
            file.write(response.text.replace("\r", ""))
    else:
        print(f"Errore nello scaricare il file: {file_url}")

def get_tasks_json(online=True):
    if online:
        response = requests.get("https://olitracker.x0k.it/api/all")
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Errore nel recuperare i dati online.")
    else:
        with open("./files/combined.json") as f:
            return json.loads(f.read())

def download_solved_problems_by_competition(cookie, solved_problems):
    url_submission = "https://training.olinfo.it/api/submission"

    tasks = get_tasks_json(ONLINE)
    
    for competition in tasks:
        competition_name = competition["competition"]
        for edition in competition["details"]:
            edition_name = edition["edition"]
            for match in edition["rounds"]:
                match_name = match["round_name"]
                
                for problem in match["tasks"]:
                    problem_name = problem["name"]
                    
                    if problem_name in solved_problems:
                        
                        submission_data = {
                            "action": "list",
                            "task_name": problem_name,
                        }
                        
                        response = requests.post(
                            url_submission,
                            json=submission_data,
                            cookies=cookie,
                        )
                        
                        if response.status_code != 200:
                            print(f"Errore nel recuperare le sottomissioni di {problem_name}")
                            continue
                        
                        submissions = response.json()["submissions"]

                        for submission in submissions[::-1]:
                            if submission.get("score", 0) == 100:
                                file = submission["files"][0]
                                directory = get_problem_directory(
                                    competition_name,
                                    edition_name,
                                    match_name,
                                    problem_name,
                                )
                                download_file(directory, file["name"], file["digest"])
                                break

def backup():
    login_data = login()
    username = login_data["username"]
    cookie = login_data["cookie"]

    url_user = "https://training.olinfo.it/api/user"
    user_info = requests.post(
        url_user,
        json={"action": "get", "username": username},
        cookies=cookie,
    ).json()
    
    solved_problems = [x["name"] for x in user_info["scores"]]
    
    download_solved_problems_by_competition(cookie, solved_problems)

def update():
    OUTPUT_DIRECTORY = "./files/"

    oii = load_oii.load(OUTPUT_DIRECTORY)
    ois = load_ois.load(OUTPUT_DIRECTORY)

    tmp = load_training_tasks.load(OUTPUT_DIRECTORY)
    training_tasks = tmp["all"]
    training_tasks_raw = tmp["all_raw"]

    combined = combine_jsons.combine(OUTPUT_DIRECTORY, oii=oii, ois=ois)

    with open(os.path.join(OUTPUT_DIRECTORY, "all_tasks_raw.json"), "w") as f:
        f.write(json.dumps(training_tasks_raw, indent=4))

    with open(os.path.join(OUTPUT_DIRECTORY, "combined.json"), "w") as f:
        f.write(json.dumps(combined, indent=4))

    tmp = check_evaluated.check(training_tasks=training_tasks, training_tasks_raw=training_tasks_raw, combined_tasks=combined)
    training_tasks = tmp["checked"]
    remaining = tmp["remaining"]

    with open(os.path.join(OUTPUT_DIRECTORY, "all_tasks.json"), "w") as f:
        f.write(json.dumps(training_tasks, indent=4))

    print("Problemi non ancora collocati in una determinata gara:", len(remaining))
    with open(os.path.join(OUTPUT_DIRECTORY, "remaining.json"), "w") as f:
        f.write(json.dumps(remaining, indent=4))

def main():
    print('''Benvenuto!\nAttendi mentre aggiorno i file con i problemi...''')
    update()
    print("Terminato!")
    backup()

if __name__ == "__main__":
    main()