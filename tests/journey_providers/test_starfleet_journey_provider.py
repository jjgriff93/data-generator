import json
import os
from journey_providers import StarfleetJourney


def test_starfleet_journey_generates_valid_jsons(tmpdir):

    # Generate a starfleet journey to the temporary test directory
    starfleet = StarfleetJourney(tmpdir)
    starfleet.create_journey()

    # Every file in the temporary directory
    for file in os.listdir(starfleet.output_path):
        with open(starfleet.output_path.join(file)) as json_file:

            # JSONs should contain the correct documents for starfleet
            assert json.load(json_file)
