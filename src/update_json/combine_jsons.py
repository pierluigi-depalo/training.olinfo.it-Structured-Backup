from importlib import resources
import json

def combine_jsons(json_directory, oii, ois):
    combined = [oii, ois]
    for entry in resources.files("update_json").joinpath(json_directory).iterdir():
        if not entry.is_file():
            continue
        with resources.files("update_json").joinpath(json_directory, entry.name).open('r') as f:
            combined.append(json.load(f))

    return combined

def save_on_file(output_path, json_directory, oii, ois):
    tmp_json = json.dumps(combine_jsons(json_directory=json_directory, oii=oii, ois=ois), indent=4)
    tmp_json = tmp_json.replace("/", "-")
    with open(output_path, "w") as f:
        f.write(tmp_json)

def combine(directory, oii, ois, save_file = False):
    JSON_DIRECTORY = "static"
    OUTPUT_PATH = directory + "combined.json"
    if save_file:
        save_on_file(output_path=OUTPUT_PATH, json_directory=JSON_DIRECTORY, oii=oii, ois=ois)
    else:
        return combine_jsons(json_directory=JSON_DIRECTORY, oii=oii, ois=ois)

if __name__ == "__main__":
    combine("./")