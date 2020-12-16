from io import UnsupportedOperation

from journey_providers.journey_provider import JourneyProvider
from .starfleet import StarfleetJourney


journey_provider_mapping = {"starfleet": StarfleetJourney}


def select_journey_provider(provider_name: str, output_path: str) -> JourneyProvider:
    """ Returns an instance of a user journey provider, given the provider_name """

    try:
        journey_type = journey_provider_mapping[provider_name.casefold()]
        return journey_type(output_path)
    except KeyError:
        raise UnsupportedOperation(
            f"Unsupported generator_type specified: {provider_name}"
        )
