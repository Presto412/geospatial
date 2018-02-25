"""Module to clean data
"""
import os
import json


def data_unclean(county):
    """Checks for missing and unneccessary values

    Arguments:
        county {[dictionary]} -- [county details]

    Returns:
        [boolean] -- [true if data is unclean]
    """
    return any(elem == -1.00
               for elem in county.values())


def clean(counties):
    """Returns cleaned county data

    Arguments:
        details {list} -- [list of counties of a state]
    """

    return [county for county in counties if not data_unclean(county)]


def main():
    """Opens and writes cleaned data to json
    """

    with open(os.path.join("output", "organized_data.json"), "r") as fobj:
        data = json.load(fobj)
    final_dict = {
        state: {
            "Counties": clean(details["Counties"]),
            "Bordering States": details["Bordering States"]
        }
        for state, details in data.items()
    }
    json.dump(final_dict, open(
        os.path.join("output", "cleaned_data.json"), "w"))


if __name__ == "__main__":
    main()
