"""Reads and saves csv data to json in organized format
"""
import json
import os
from decimal import Decimal


def get_disease_data(details):
    """returns only necessary disease data

    Arguments:
        details {list} -- details of each county
    """
    return {
        "state_name": details[0].upper(),
        "name": details[1].upper(),
        "death_rates": float(Decimal(details[3]))
    }


def get_census_data(details):
    """returns only required data from census

    Arguments:
        details {list} -- details of each county
    """
    try:
        return {
            "state_name": details[5].split('-')[1].strip().upper(),
            "name": details[6].upper().replace(' COUNTY', ''),
            "population": int(details[7].split('(')[0]),
            "area": float(Decimal(details[9].split('(')[0])),
        }
    except IndexError:
        return None


def get_state_data(details):
    """returns bordering states for a state

    Arguments:
        details {list} -- details of each state
    """
    return {"name": details[0].upper(), "bordering_states": details[1:-1]}


def aggregate_county_data(county, census_data):
    """aggregates county data for given county

    Arguments:
        county {string}
        census_data {list}
    """
    for item in census_data:
        if county["name"] in item["name"] and item["state_name"] == county["state_name"]:
            county.update(item)
    return county


def get_county_data_by_state(state, disease_data, census_data):
    """gets county data for given state

    Arguments:
        state {[type]} -- [description]
        disease_data {[type]} -- [description]
        census_data {[type]} -- [description]
    """
    return [
        aggregate_county_data(county, census_data) for county in disease_data
        if county["state_name"] == state["name"]
    ]


def aggregate(disease_data, census_data, state_data):
    """aggregates all county data

    Arguments:
        disease_data {list}
        census_data {list}
        state_data {list}
    """
    return {
        state["name"]: {
            "Counties":
            get_county_data_by_state(state, disease_data, census_data),
            "Bordering States":
            state["bordering_states"]
        }
        for state in state_data
    }


def main():
    """Organizes data into /outputs
    """
    disease_data_fp = os.path.join("data", "usa_heartrate_by_county.csv")
    census_data_fp = os.path.join("data", "usa_population_area_by_county.csv")
    state_data_fp = os.path.join("data", "usa_bordering_states.csv")
    output_fp = os.path.join("output", "organized_data.json")

    with open(disease_data_fp, "r") as fobj:
        disease_data = [
            get_disease_data(i.strip().split(',')) for i in fobj.readlines()
        ]
    with open(census_data_fp, "r") as fobj:
        census_data = [
            get_census_data(i.strip().split(',')) for i in fobj.readlines()
            if get_census_data(i.strip().split(',')) is not None
        ]
    with open(state_data_fp) as fobj:
        state_data = [
            get_state_data(i.strip().split(',')) for i in fobj.readlines()
        ]
    json.dump(
        aggregate(disease_data, census_data, state_data), open(output_fp, "w"))


if __name__ == '__main__':
    main()
