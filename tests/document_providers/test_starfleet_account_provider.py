from typing import Dict
from mimesis.schema import Field
from document_providers import StarfleetAccount


def test_document_template_correctly_populated():

    generated_document: Dict
    field = Field("en-GB")
    generated_document = StarfleetAccount().create_schema(field)

    # assert the top level keys are as expected
    assert set(generated_document.keys()) == set(
        [
            "id",
            "stardate_of_birth",
            "subspace_address",
            "communicator",
            "surname",
            "forename",
            "title",
            "auth",
            "federation_citizen_id"
        ]
    )

    # ... and none of them have a value of None
    assert None not in generated_document.values()
