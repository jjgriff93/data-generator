import json
import os
from click.testing import CliRunner
import pytest
from generate import cli


runner = CliRunner()


@pytest.fixture
def three_submission_documents(tmpdir):
    """
    Generates three starfleet_application documents
    """
    runner.invoke(
        cli,
        [
            "document",
            "--output_path",
            str(tmpdir),
            "--provider",
            "starfleet_application",
            "--quantity",
            3,
        ],
    )

    directory = tmpdir.join("starfleet_application")

    return directory


def test_generate_document_exits_0(tmpdir):
    response = runner.invoke(
        cli,
        ["document", "--output_path", str(tmpdir), "--provider", "starfleet_application"],
    )
    # Should run without failure
    assert response.exit_code == 0


def test_generate_document_produces_valid_files(three_submission_documents):

    # Every file in the temporary directory
    for file in os.listdir(three_submission_documents):
        with open(three_submission_documents.join(file)) as json_file:

            # Should be valid JSON
            assert json.load(json_file)


def test_generate_document_outputs_desired_quantity(three_submission_documents):

    num_of_files = len([file for file in os.listdir(three_submission_documents)])

    # Should have three files in the temp output directory
    assert num_of_files == 3


def test_generate_document_rejects_invalid_document(tmpdir):
    response = runner.invoke(
        cli, ["document", "--output_path", str(tmpdir), "--provider", "vogon_poetry"]
    )
    # Should return a usage error
    assert response.exit_code == 2


def test_generate_journey(tmpdir):
    response = runner.invoke(
        cli, ["journey", "--output_path", str(tmpdir), "--provider", "starfleet"]
    )
    # Should run without failure
    assert response.exit_code == 0


def test_generate_journey_rejects_invalid_journey(tmpdir):
    response = runner.invoke(
        cli,
        [
            "journey",
            "--output_path",
            str(tmpdir),
            "--provider",
            "an_unexpected_journey",
        ],
    )
    # Should return a usage error
    assert response.exit_code == 2
