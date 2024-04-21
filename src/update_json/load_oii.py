import requests
import json
import datetime
import importlib.resources as resources

year = datetime.date.today().year

def get_buildId():
    html_page = requests.get("https://stats.olinfo.it/").text
    html_page = html_page.split('"')
    pos = html_page.index("buildId")
    return html_page[pos+2]

def get_tasks(year):
    tmp = requests.get("https://stats.olinfo.it/_next/data/" + get_buildId() + "/contest/" + year + ".json")
    if tmp != 404:
        return json.loads(tmp.text)["pageProps"]["contest"]["tasks"]
    else:
        return None

def load_oii():
    tasks = {}
    for i in range(2001, year):
        tmp = get_tasks(str(i))
        if tmp != None:
            tasks[str(i)] = tmp

    return tasks

def build_oii_json(preoii_path, terry_path, practice_path):
    preoii = {}
    territoriali = {}
    practice = {}

    with resources.files(__package__).joinpath(practice_path).open('r') as f:
        practice = json.load(f)

    with resources.files(__package__).joinpath(preoii_path).open('r') as f:
        preoii = json.load(f)

    with resources.files(__package__).joinpath(terry_path).open('r') as f:
        territoriali = json.load(f)

    tmp = load_oii()
    oii = []
    for year in tmp.keys():
        app = {}
        app["edition"] = year
        app["rounds"] = []
        t = {"round_name" : "Nazionale", "tasks" : []}
        for task in tmp[year]:
            t["tasks"].append({"name" : "oii_"+task["name"], "title" : task["title"]})
        if year in preoii.keys():
            app["rounds"].append(preoii[year])
        if year in practice.keys():
            app["rounds"].append(practice[year])
        if year in territoriali.keys():
            app["rounds"].append(territoriali[year])
        app["rounds"].append(t)
        oii.append(app)
    
    return {"competition" : "OII", "details" : oii}

def save_on_file(file_path, preoii_path, terry_path, practice_path):
    with open(file_path, "w") as f:
        f.write(json.dumps(build_oii_json(preoii_path=preoii_path, terry_path=terry_path, practice_path=practice_path), indent=4))

def load(directory, save_file = False):
    PATH_PREOII = "static/oii/preoii.json"
    PATH_PRACTICE = "static/oii/practice.json"
    PATH_TERRY = "static/oii/territoriali.json"
    PATH_OUTPUT = directory + "json_dumps/oii.json"
    if save_file:
        save_on_file(file_path=PATH_OUTPUT, preoii_path=PATH_PREOII, terry_path=PATH_TERRY, practice_path=PATH_PRACTICE)
    else:
        return build_oii_json(preoii_path=PATH_PREOII, terry_path=PATH_TERRY, practice_path=PATH_PRACTICE)

if __name__ == "__main__":
    load("./")