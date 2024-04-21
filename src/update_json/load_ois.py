from importlib import resources
import requests
import json

wanted_fields = [
    "id",
    "name", 
    "title",
    "year"
]

final = {
    "id" : "final",
    "name" : "final",
    "title" : "Final"
}

def get_editions():
    ret = []
    all_editions = json.loads(requests.get("https://squadre.olinfo.it/json/edition.json").text)["editions"]

    for e in all_editions:
        tmp = {}
        for field in wanted_fields:
            tmp[field] = str(e[field])
        ret.append(tmp)

    return ret

def get_final(edition):
    tmp = final.copy()
    tmp["tasks"] = []
    final_info = json.loads(requests.get("https://squadre.olinfo.it/json/edition." + edition + ".round.final.json").text)
    tmp["tasks"] = final_info["tasks"]
    return tmp

def define_editions(edition):
    edition_info = json.loads(requests.get("https://squadre.olinfo.it/json/edition." + edition + ".json").text)
    t = edition_info["contests"]
    t.append(get_final(edition))
    return t

def load_ois():
    editions = get_editions()
    for i in range(len(editions)):
        editions[i]["contests"] = define_editions(editions[i]["id"])

    return editions

def build_ois_json(iiot_path):
    iiot = {}
    with resources.files(__package__).joinpath(iiot_path).open('r') as f:
        iiot = json.load(f)

    tmp = load_ois()
    ois = []
    for ed in tmp:
        app = {}
        app["edition"] = ed["year"]
        app["rounds"] = []
        for round in ed["contests"]:
            tmp = {}
            tmp["round_name"] = round["title"]
            tmp["tasks"] = []
            for task in round["tasks"]:
                task["name"] = "ois_"+str(task["name"])
                tmp["tasks"].append(task)
            app["rounds"].append(tmp)

        if app["edition"] in iiot.keys():
            app["rounds"].append(iiot[app["edition"]])

        ois.append(app)
    return {"competition" : "OIS", "details" : ois}

def save_on_file(output_file_path, iiot_path):
    f = open(output_file_path, "w")
    f.write(json.dumps(build_ois_json(iiot_path=iiot_path), indent=4))
    f.close()

def load(directory, save_file = False):
    PATH_IIOT = "static/ois/iiot.json"
    OUTPUT_PATH = directory + "json_dumps/ois.json"
    if save_file:
        save_on_file(output_file_path=OUTPUT_PATH, iiot_path=PATH_IIOT)
    else:
        return build_ois_json(iiot_path=PATH_IIOT)

if __name__ == "__main__":
    load("./")