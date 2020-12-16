from journey_providers.starfleet import StarfleetJourney
from journey_providers import select_journey_provider


def test_starfleet_journey_provider_name_is_resolved_correctly(tmpdir):

    provider_name = "starfleet"

    provider = select_journey_provider(provider_name, tmpdir)

    assert type(provider) == StarfleetJourney
