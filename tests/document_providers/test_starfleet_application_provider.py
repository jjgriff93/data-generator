from typing import Dict
import uuid
from mimesis.schema import Field
from document_providers import StarfleetApplication


def test_starfleet_application_template_correctly_populated():

    generated_schema: Dict
    field = Field("en-GB")
    generated_schema = StarfleetApplication().create_schema(field)

    # assert the top level keys are as expected
    assert set(generated_schema.keys()) == set(
        [
            "id",
            "accountId",
            "completed",
            "details",
            "record"
        ]
    )

    # assert that keys under "details" are as expected...
    assert set(generated_schema["details"].keys()) == set(
        [
            "surname",
            "forename",
            "title",
            "faction",
            "communicator",
            "space_address",
            "federation_citizen_id"
        ]
    )

    # ... and none of them have a value of None
    assert None not in generated_schema["details"].values()


def test_starfleet_application_document_generates_output():

    generated_document = StarfleetApplication().generate()

    # If the document was generated correctly, random valid UUID should have been generated
    # for the "accountId" field
    assert uuid.UUID(generated_document["accountId"]).hex
