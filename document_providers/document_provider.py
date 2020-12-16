from generate_errors import DataGenerationError
from mimesis.schema import Field, Schema


class DocumentProvider:
    """
    Base class for providing document schemas to generate fake documents with
    """

    name = None

    def __init__(self, localisation="en-GB"):
        # Generate a localisation field object for the DocumentProvider
        self.field = Field(localisation)

    def create_schema(self) -> dict:
        raise NotImplementedError()

    def generate(self) -> dict:
        try:
            # Create Mimesis Field object for specified localisation
            document_schema = Schema(lambda: self.create_schema(self.field))

            # Because we want a variance in schemas we need to handle iterations ourselves
            fake_document = document_schema.create(iterations=1)[0]
            return fake_document

        except Exception as e:
            raise DataGenerationError(
                "Unable to generate data using the document provider"
            ) from e
