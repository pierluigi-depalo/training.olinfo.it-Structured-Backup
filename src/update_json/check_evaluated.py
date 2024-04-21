def update_status(training_tasks, training_tasks_raw, combined_tasks):
    remaining_tasks = training_tasks.copy()
    for competition in combined_tasks:
            for edition in competition["details"]:
                for round in edition["rounds"]:
                    try:
                        for task in round["tasks"]:
                            if task["name"] in training_tasks.keys():
                                training_tasks[task["name"]]["checked"] = True
                                remaining_tasks.pop(task["name"])
                    except:
                        print(round)

    remaining = []
    for t in remaining_tasks.keys():
        remaining.append(training_tasks_raw[t])

    return {"checked" : training_tasks, "remaining" : remaining}

def check(training_tasks, training_tasks_raw, combined_tasks):
    return update_status(training_tasks=training_tasks, training_tasks_raw=training_tasks_raw, combined_tasks=combined_tasks)

if __name__ == "__main__":
    check("./")