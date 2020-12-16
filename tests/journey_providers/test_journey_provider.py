from document_providers.document_provider import DocumentProvider
from journey_providers import JourneyProvider


class FakeJourneyProvider(JourneyProvider):
    name = "fake_journey_provider"


class FakeDocumentProvider(DocumentProvider):
    name = "fake_document_provider"


fake_document = {"id": "foo", "class": "bar"}


def test_journey_provider_adds_step(tmpdir):

    fake_journey = FakeJourneyProvider(tmpdir)
    fake_journey.add_step(
        FakeDocumentProvider,
        fake_document,
    )

    # If step is successfully added a metadata entry should be present
    assert (
        fake_journey.journey_metadata["steps"][0]["fileName"]
        == f"0.fake_document_provider.0.{fake_journey.user_id}.json"
    )


def test_journey_provider_final_step(tmpdir):

    fake_journey = FakeJourneyProvider(tmpdir)
    delays = [0, 60, 6000, 30]

    # Create four steps with varying delays
    for delay in delays:
        fake_journey.add_step(FakeDocumentProvider, fake_document, delay=[delay, delay])

    # Final step should be the one with the highest delay - step index 2 (6000s)
    assert fake_journey.final_step() == 2
