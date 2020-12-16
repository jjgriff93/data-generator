import json
import os
import click
from dotenv import load_dotenv

from document_providers import select_document_provider, document_provider_mapping
from journey_providers import select_journey_provider, journey_provider_mapping
from generate_errors import DataOutputError, DataGenerationError


load_dotenv()


@click.group()
def cli():
    pass


@cli.command(name="document")
@click.option(
    "-o",
    "--output_path",
    default="./output/documents",
    type=click.Path(exists=True),
    help="Path to output the generated files to",
)
@click.option(
    "-p",
    "--provider",
    type=click.Choice(document_provider_mapping.keys()),
    required=True,
    help="document provider to use",
)
@click.option(
    "-q", "--quantity", type=click.INT, default=1, help="Number of files to create"
)
def generate_document(output_path, provider, quantity):
    """Generates data based upon a specified document provider schema

    Generated data files are saved to the path specified in --output_path
    (if unspecified this defaults to ./output/documents)

    The --provider option is used to define a document provider to use for generating data

    The --quantity option specifies how many of the document files are to be generated

    For example:

    python generate.py document --output_path ./output/documents --provider starfleet_application
     --quantity 10
    """
    # Get provider type from document_provider type map
    document_provider = select_document_provider(provider)

    # Export output to a provider folder within the specified output path
    provider_output_path = os.path.join(output_path, document_provider.name)
    # Create the folder if it doesn't already exist
    if not os.path.exists(provider_output_path):
        os.makedirs(provider_output_path)

    # Generate documents up to desired quantity
    for i in range(quantity):
        document = document_provider.generate()

        try:
            # Save the generated document as JSON in the specified output folder
            file_name = f"{document_provider.name}_{i}.json"
            file_path = os.path.join(provider_output_path, file_name)
            with open(file_path, "w") as fp:
                json.dump(document, fp)

            if i != 0:
                # Clear previous line
                print("\033[A\033[A")

            # Output status to the console
            print(f"Generated {i + 1} {document_provider.name} documents...")

        except Exception as e:
            raise DataOutputError(
                "Unable to output the generated documents to destination path"
            ) from e


@cli.command(name="journey")
@click.option(
    "-o",
    "--output_path",
    default="./output/journeys/",
    type=click.Path(exists=True),
    help="Path to output the generated files to",
)
@click.option(
    "-p",
    "--provider",
    type=click.Choice(journey_provider_mapping.keys()),
    required=True,
    help="User journey provider to use",
)
@click.option(
    "-q", "--quantity", type=click.INT, default=1, help="Number of journeys to create"
)
def generate_journey(output_path, provider, quantity):
    """Generates documents in a pattern to simulate a user journey

    Generated data files are saved to the path specified in --output_path (if unspecified this defaults to ./output/journeys)

    The --provider option is used to specify the name of the user journey template to use
    that describes the pattern of documents to generate

    For example:

    python generate.py journey --output_path ./output/journeys --provider starfleet
    """
    # Generate documents up to desired quantity
    for i in range(quantity):

        # Get provider type from journey_provider type map
        journey_provider = select_journey_provider(provider, output_path)

        # Construct the journey & output document files
        try:
            journey_provider.create_journey()
        except Exception as e:
            raise DataGenerationError("Unable to create user journey") from e

        # Finalise and export metadata for the journey
        try:
            journey_provider.publish_journey(output_path)

            if i != 0:
                # Clear previous line
                print("\033[A\033[A")

            # Output status to the console
            print(f"Generated {i + 1} {journey_provider.name} journeys...")

        except Exception as e:
            raise DataOutputError(
                "Unable to output the generated documents to destination path"
            ) from e


if __name__ == "__main__":
    cli()
