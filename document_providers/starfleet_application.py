import random

# from mimesis import Datetime
from mimesis.schema import Field
from document_providers.document_provider import DocumentProvider


# Static data (document options) for random population into relevant document sections
professions = [
    "Security Officer",
    "Botanist",
    "Ship's Councillor",
    "Engineer",
    "Science Officer"
]
factions = [
    "Terran",
    "Ferengi",
    "Klingon",
    "Romulan",
    "Vulcan"
]
ranks = [
    "Ensign",
    "Lieutenant JG",
    "Lieutenant",
    "Lieutenant Commander",
    "Commander",
    "Captain",
    "Admiral"
]
assignments = [
    "NCC-1701"
    "NCC-1701-A",
    "NCC-26517",
    "NCC-10532",
    "NCC-2893",
    "NX-74205",
    "NCC-42296",
    "NCC-71807",
    "NCC-1701-D",
    "NCC-1701-E",
    "NCC-74656",
    "NCC-1864"
]
performance = ["highest honours", "exemplary", "adequate", "poor", "discommendation"]
current_year = 2293  # Datetime.CURRENT_YEAR


class StarfleetApplication(DocumentProvider):

    name = "starfleet_application"

    def create_schema(self, _: Field) -> dict:

        starfleet_application_schema = {
            "id": _("cryptographic.uuid"),
            "accountId": _("cryptographic.uuid"),
            "completed": str(_("datetime.date", start=current_year - 1, end=current_year)),
            "details": {
                "surname": _("person.last_name"),
                "forename": _("person.first_name"),
                "title": _("person.title"),
                "faction": random.choice(factions),
                "communicator": _("person.telephone"),
                "space_address": {
                    "address_line": [_("address.street_name"), _("address.city")],
                    "postcode": _("address.postal_code"),
                },
                "federation_citizen_id": _("person.identifier", mask="@@###@@@#@###@")
            },
            "record": []  # <-- Populated by for-loop for variance
        }

        # Generate random number of entries into record
        for record_index in range(random.randint(1, 10)):
            starfleet_application_schema["record"].append(
                {
                    "assignment": random.choice(assignments),
                    "rank": random.choice(ranks),
                    "profession": random.choice(professions),
                    "served_from_month": _("numbers.integer_number", start=1, end=12),
                    "served_from_year": str(
                        _(
                            "datetime.year",
                            minimum=current_year - 20,
                            maximum=current_year,
                        )
                    ),
                    "comments": []
                }
            )

            # Generate random number of comments in record entry
            for comment_index in range(random.randint(1, 10)):
                starfleet_application_schema["record"][record_index]["comments"].append(
                    _("text.sentence")
                )

        # Return Mimesis schema description of the document
        return starfleet_application_schema
