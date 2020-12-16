from io import UnsupportedOperation

from .document_provider import DocumentProvider
from .starfleet_application import StarfleetApplication
from .starfleet_account import StarfleetAccount


document_provider_mapping = {
    StarfleetApplication.name: StarfleetApplication,
    StarfleetAccount.name: StarfleetAccount
}


def select_document_provider(provider_name: str) -> DocumentProvider:
    """ returns an instance of a document schema provider, given the provider_name """

    try:
        document_provider = document_provider_mapping[provider_name.casefold()]
        return document_provider()
    except KeyError:
        raise UnsupportedOperation(
            f"Unsupported document_provider specified: {provider_name}"
        )
