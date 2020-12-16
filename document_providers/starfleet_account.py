# from mimesis.providers.date import Datetime

from mimesis.schema import Field
from document_providers.document_provider import DocumentProvider


current_year = 2293  # Datetime.CURRENT_YEAR


class StarfleetAccount(DocumentProvider):

    name = "starfleet_account"

    def create_schema(self, _: Field) -> dict:

        starfleet_account_schema = {
            "id": _("cryptographic.uuid"),
            "stardate_of_birth": str(_("datetime.date", end=current_year - 18)),
            "subspace_address": _("person.email"),
            "communicator": _("person.telephone", mask="07#########"),
            "surname": _("person.last_name"),
            "forename": _("person.first_name"),
            "title": _("person.title"),
            "auth": {
                "logins": []
            },
            "federation_citizen_id": _("person.identifier", mask="@@###@@@#@###@")
        }

        # Return Mimesis schema description of the document
        return starfleet_account_schema
