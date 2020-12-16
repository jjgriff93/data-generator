import json
import os
import random
import uuid
from zipfile import ZipFile
import shutil

from document_providers.document_provider import DocumentProvider


class JourneyProvider:
    """
    Base class for providing user journeys
    """

    name = None

    def __init__(self, output_path):
        # Generate a unique user_id for the journey
        self.user_id = uuid.uuid4()

        # Instantiate a step index to keep filenames unique
        self.step_index = 0

        # Create journey metadata to track data for 'replaying' the files during publishing
        self.journey_metadata = {
            "userId": str(self.user_id),
            "journeyName": self.name,
            "steps": [],
        }

        # Create a local output path for the documents if it doesn't already exist
        self.output_path = output_path + f"/{self.user_id}"
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def create_journey(self) -> dict:
        raise NotImplementedError()

    def add_step(
        self,
        document_type: DocumentProvider,
        document: dict,
        delay=[0, 0],
        delay_from_step_index=None,
    ):
        """
        Save a document file to the output folder and add file path and delay info to journey metadata

        document_type : DocumentProvider
            The DocumentProvider which was used to generate the document you're passing in
        document: dict
            The document to add as a step
        delay: [int, int]
            The range (in seconds) in which to randomise a delay for the step. The delay value is used for publishing
            purposes; it reflects how many seconds after the user journey has begun to wait before publishing the file
        delay_from_step: int
            (Optional) Adds the delay of a previous step (specified as the index number of the step within the journey
            metadata's steps array) to this step's delay value
        """
        # Randomly generate a delay within the range specified (in seconds)
        document_delay = random.randint(delay[0], delay[1])

        # If delay_from_step specifies a step index, add the delay from that step to this step's delay
        if delay_from_step_index:
            document_delay += self.journey_metadata["steps"][delay_from_step_index]["delay"]

        # Output file with naming convention
        file_name = (
            f"{document_delay}.{document_type.name}.{self.step_index}.{self.user_id}.json"
        )
        with open(self.output_path + "/" + file_name, "w") as fp:
            json.dump(document, fp)

        # Update journey metadata with saved document and any additional replay details
        self.journey_metadata["steps"].append(
            {"fileName": file_name, "delay": document_delay}
        )

        # Increment the step index for unique filenames and delay reference
        self.step_index += 1

        return self.step_index - 1

    def final_step(self):
        """
        Helper function that returns the step index containing the highest delay

        This is useful if you need to make sure the step you're contructing is the last step
        the user perdocuments (i.e. has a delay higher than the highest computed delay from a
        previous step)
        """
        steps = self.journey_metadata["steps"]
        return max(range(len(steps)), key=lambda index: steps[index]["delay"])

    def publish_journey(self, publish_path: str):
        """
        Exports the finalised metadata file for the user journey and zips files for publishing
        """
        # Zip the document files
        with ZipFile(f"{publish_path}/{self.name}.{self.user_id}.zip", "w") as zip:
            for dirname, subdirs, files in os.walk(self.output_path):
                for filename in files:
                    zip.write(os.path.join(dirname, filename), arcname=filename)

        # Delete the unzipped directory
        shutil.rmtree(self.output_path)

        # Output the metadata dict as JSON within journey zip
        file_name = f"{self.name}.{self.user_id}.metadata.json"
        with open(publish_path + "/" + file_name, "w") as fp:
            json.dump(self.journey_metadata, fp)
