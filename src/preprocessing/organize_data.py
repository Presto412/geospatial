import json
import os
from pprint import pprint

with open(os.path.join("data", "usa_heartrate_by_county.csv"), "r") as f:
    lines = [i.strip().split(',') for i in f.readlines()]
with open(os.path.join("data", "usa_population_area_by_county.csv"), "r") as f:
    census_lines = [i.strip().split(',') for i in f.readlines()]
with open(os.path.join("data", "usa_bordering_states.csv"), "r") as f:
    state_lines = [i.strip().split(',') for i in f.readlines()]

for county1 in census_lines:
    for county2 in lines:
        if (county2[1] in county1[6]) and (county2[0] in county1[5]):
            county2[4] = county1[9].strip()
            county2[5] = county1[7].strip()
            county2[6] = county1[12].strip()

states = list(set([i[0] for i in lines]))

bordering_states = {state2: [i.strip() for i in state1[1:-1]]
                    for state2 in states for state1 in state_lines if state1[0] == state2}

final_dict = {
    state: {
        "Counties": [{data[1]: {
            "heart_disease_DR": data[3],
            "area": data[4],
            "population": data[5],
            "population_density": data[6]
        }}
            for data in lines if data[0] == state
        ],
        "Bordering States": bordering_states[state] if state in bordering_states else ""
    }
    for state in states
}
with open(os.path.join("output", "organized_data.json"), "w") as f:
    json.dump(final_dict, f)
