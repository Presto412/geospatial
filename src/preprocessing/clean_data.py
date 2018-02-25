import os
import json
with open(os.path.join("output", "organized_data.json"), "r") as f:
    data = json.load(f)


def clean(details):
    return [
        county for county in details["Counties"]
        if not any(
            elem == "" or elem == "-1.00"
            for elem in county.items()[0][1].values()
        )
    ]


final_dict = {state: clean(details) for state, details in data.items()}
json.dump(final_dict, open(os.path.join("output", "cleaned_data.json"), "w"))
