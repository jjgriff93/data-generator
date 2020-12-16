SHELL := /bin/bash

build: lint	test

pip-install:
	pip install -r requirements.txt

ci-build: pip-install build
	
lint:
	flake8 .
	
test:
	pytest tests/**

black:
	black .

application_10000:
	time python generate.py document --provider starfleet_application --quantity 10000

account_10000:
	time python generate.py document --document_provider starfleet_account --quantity 10000

starfleet_journey_1000:
	time python generate.py journey --journey_provider starfleet --quantity 1000

azcopy_documents:
	time azcopy copy './output/documents' '${BLOB_CONTAINER_URL}/${BLOB_SAS_TOKEN}' --recursive

azcopy_journeys:
	time azcopy copy './output/journeys' '${BLOB_CONTAINER_URL}/${BLOB_SAS_TOKEN}' --recursive

cleanup:
	rm -rf ./output/*/*.json
	rm -rf ./output/*/*.zip
