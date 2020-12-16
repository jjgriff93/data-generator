from document_providers import select_document_provider, StarfleetApplication, StarfleetAccount


def test_starfleet_application_provider_name_is_resolved_correctly():

    provider_name = "starfleet_application"

    provider = select_document_provider(provider_name)

    assert type(provider) == StarfleetApplication


def test_account_provider_name_is_resolved_correctly():

    provider_name = "starfleet_account"

    provider = select_document_provider(provider_name)

    assert type(provider) == StarfleetAccount
