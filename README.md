# Data Generator

The Data Generator is a Python CLI app made up of two commands/capabilities:

- Document Generator: generates data files using a "Document Provider", a schema that outlines the structure of a given document, as well as what fields to fake and how to fake them.
- User Journey Generator: generates a user journey using a "Journey Provider", a series of steps that instruct types of documents to generate to simulate a user interacting with a system and generating a number of documents in the database as a result.

To view overall usage:

``` bash
$ python generate.py --help

Usage: generate.py [OPTIONS] COMMAND [ARGS]...

Commands:
  document     Generates data based upon a specified document provider schema...
  journey      Generates documents in a pattern to simulate a user journey
```


## Installation & Developing

A DevContainer configuration is already set up for you. Simply clone this repository in VS Code and it will prompt you to re-open in a DevContainer, which will installed all the required dependencies and tools for you in a Docker image. More info on them [here](https://code.visualstudio.com/docs/remote/containers)

If you fancy doing it the old-fashioned way (heaven-forbid) then simply open in your IDE of choice with a Python environment set up, then run:

``` bash
pip install -r requirements.txt
```
Then you're ready to engage (sorry in advance for all of the shameless Star Trek references).

## Building and Testing

The `Makefile` defines the following rules for building and testing this codebase:

rule | description | example
--|--|--
'lint' | Runs `flake8` against the code | `make lint`
'black' | Runs `black` against the code, which will format the .py files so that they pass linting | `make black`
'test' | Runs `pytest` and reports test results | `make test`
'build' | Runs the lint and test rules. This is the default rule. | `make build` or just `make`


## Document Generator

### Usage

To view usage for the `document` command:
```bash
python generate.py document --help

Usage: generate.py document [OPTIONS]

  Generates data based upon a specified document provider schema

  Generated data files are saved to the path specified in --output_path 
  (if unspecified this defaults to ./output/documents)

  The --provider option is used to define a document provider to use for
  generating data

  The --quantity option specifies how many of the document files are to be
  generated

  For example:

  python generate.py document --output_path ./output/documents --provider
  starfleet_application  --quantity 10

Options:
  -o, --output_path PATH          Path to output the generated files to
  -p, --provider [starfleet_application | starfleet_account]
                                  document provider to use  [required]
  -q, --quantity INTEGER          Number of files to create
  --help                          Show this message and exit.
```


#### Generate 1 fake document on the local file system

``` bash
$ python generate.py document --provider starfleet_application
```

#### Generate 10 files on the local file system to a non-default directory

``` bash
$ python generate.py document --output_path ./my_custom_directory/output --document_provider starfleet_application --quantity 10
```


### Document Providers and Extending This Codebase

This utility works by using Document Providers that we define, which are built on top of [Mimesis Schemas](https://mimesis.readthedocs.io/api.html#schema) to describe what a document's structure should look like as well as the strategies to fake the fields within it.

Within the repo, the folder `./document_providers/` contains Python files (i.e `starfleet_application.py`, `starfleet_account.py`) which use the `DocumentProvider` base class and define the structure and content of a document. 


``` python
from mimesis.schema import Field
from document_providers.document_provider import DocumentProvider


class StarfleetAccount(DocumentProvider):

    name = "starfleet_account"

    def create_schema(self, _: Field) -> dict:

        starfleet_account_schema = {
            "id": _("cryptographic.uuid"),
            "stardate_of_birth": str(_("datetime.date", end=current_year - 18)),
```

It then returns this 'description' which is then passed into `document_provider.generate()`, which takes the Mimesis Schema and asks Mimesis to use it to generate a fake document (outputted as a dictionary).

This is then saved to the specified `output_path` as JSON.


### Understanding DocumentProviders

As these are built on top of Mimesis Schemas & Fields, it's a good idea to first understand how these work by [visiting their docs](https://mimesis.readthedocs.io/getting_started.html#schema-and-fields). 

Now let's take the `starfleet_account.py` provider as an example:

```python
class StarfleetAccount(DocumentProvider):

    name = "starfleet_account"

    def create_schema(self, _: Field) -> dict:

        starfleet_account_schema = {
            "id": _("cryptographic.uuid"),
            "stardate_of_birth": str(_("datetime.date", end=current_year - 18)),
            "subspace_address": _("person.email"),
            "communicator": _("person.telephone", mask="07#########"),
            "surname": _("person.last_name"),
            "forename": _("person.first_name"),
            "title": _("person.title"),
            "auth": {
                "logins": []
            },
            "federation_citizen_id": _("person.identifier", mask="@@###@@@#@###@")
        }

        # Return Mimesis schema description of the document
        return starfleet_account_schema
```

Here you can see we first pass in a Mimesis Field object (`_`). This is what Mimesis uses to interpret which Data Providers (providers of fake data in different categories such as `person` and `text`) we want to use, as well as additional arguments to further customise their usage. You can see this in us on many of the lines above including this one:

```python
"communicator": _("person.telephone", mask="07#########"),
```

This is simply passing in the provider `person.telephone`, which creates a random telephone number, as well as the optional `mask` argument to scope what pattern the number should follow ()in our case a mobile number, which would obviously still be useful in the 23rd century...). The output when processed by the `generator` will look something like this:

```python
"communicator": "07123456789"
```

So, using the Field creator `_` followed by `("data_provider_name.provider_method")` allows us to fill in that placeholder with generated fake data.

For the full range of Data Providers you can call with Mimesis, view their [API formation](https://mimesis.readthedocs.io/api.html).


### Adding a New Document Provider

The following is a TODO list for anyone adding a new document provider:

1. Implement a new subclass of `DocumentProvider` within the `./document_providers/` folder. Use `./document_provider/starfleet_account.py` as a simple example or `./document_provider/starfleet_application.py` if you're looking to do something more complex
2. Modify `./document_providers/__init__.py` to add your new provider to the `document_type_mapping` and pass it the `.name` property of your new class as the key
3. (Optional but encouraged) Create some `pytest` tests in the `./tests/document_providers` to validate that your provider is producing the desired document structure/content correctly

That's it. All you need to do then is construct how your document should look and how the data should be faked in the provider file you've created. You can use the [Mimesis docs](https://mimesis.readthedocs.io/api.html) to help you find the right fake data providers to use.


## Journey Generator

### Usage

To view usage for the `journey` command:
```bash
python generate.py journey --help

Usage: generate.py journey [OPTIONS]

  Generates documents in a pattern to simulate a user journey

  Generated data files are saved to the path specified in --output_path
  (if unspecified this defaults to ./output/journeys)

  The --provider option is used to specify the name of the
  journey provider to use that describes the pattern of documents to generate

  For example:

  python generate.py journey --output_path ./output/journeys
  --provider starfleet

Options:
  -o, --output_path PATH         Path to output the generated files to
  -p, --provider [starfleet]  Path to user journey template to use
                                 [required]

  -q, --quantity INTEGER         Number of journeys to create
  --help                         Show this message and exit.
```


#### Generate 1 fake journey

``` bash
$ python generate.py journey --provider starfleet
```

#### Generate 10 fake journeys to a non-default directory

``` bash
$ python generate.py journey --output_path ./my_new_directory/output --journey_provider starfleet --quantity 10
```


### Journey Providers and Extending This Codebase

Similar to the Document Generator, the Journey Generator creates a series of documents by using Journey Providers that we define. These are Python "templates" which inherit the base class `JourneyProvider` and implement the `create_journey()` method.

The folder `./journey_providers/` contains a Python file called `starfleet.py` which creates a Starfleet application journey and gives a good example of what a JourneyProvider should look like. It implements a series of steps by calling `self.add_step()` and passing a document, as well as some optional parameters.

Here is a snippet from the starfleet provider:

``` python
from document_providers.starfleet_account import StarfleetAccount
from journey_providers.journey_provider import JourneyProvider


class StarfleetJourney(JourneyProvider):

    name = "starfleet"

    def create_journey(self):

        # 1. User creates an account
        # Generate a random account document
        account_document = StarfleetAccount().generate()

        # Set the users account id as the user_id uuid we generated so we correlate the documents
        account_document["id"] = str(self.user_id)

        # Add the generated document as a new step
        self.add_step(StarfleetAccount, account_document)
```

Above you can see some key concepts which we'll now go through.

#### Provider construction
Our new class `StarfleetJourney` inherits the base class `JourneyProvider`. We specify a friendly "name" for the JourneyProvider which is used when exporting files to make the directory/filenames more descriptive. We then implement the `create_journey(self)` method.

#### Creating documents
We use a DocumentProvider (in this case `StarfleetAccount`) to generate a fake document by calling `generate()` on its instance, which we can then modify (i.e. replacing a field). This is useful for correlating all of the documents to a single user id for example as we do here. We can call as many DocumentProviders as we like for a variety of fake documents in the journey.

We also use the property `self.user_id` as the user's UUID - this is generated in the JourneyProvider's `__init__` function and will always be unique for each journey generated. It's used to name the journey and exported files, and can also be used to substitute in for a user identifier in the documents (in this case `id`).

#### Adding a journey step
We call the `self.add_step()` method, which takes a `DocumentProvider` and a `document` (dict) as input. The DocumentProvider is the provider that was used to construct the document we're passing in so it can derive the name of the document type for the output filename.

#### Delays & journey metadata
When we add the claim step, we also use the optional arguments `delay` and `delay_from_step_index` (if left unspecified they default to `0` & `None`). As well as generating a series of documents, a JourneyProvider keeps a metadata record (`self.journey_metadata`) of the steps (files) generated during journey creation. This includes the filename, and the delay value (in seconds) associated with it. 

This value is intended for a publishing tool to understand which documents it needs to copy into a destination container first, and the delay (number of seconds) to wait before publishing the next document and so on.
- `delay` accepts an array of two `int` values, the lowest possible delay to add and the highest in seconds - the step contructor will then generate a random delay within that range
- `delay_from_step_index` accepts an `int` which refers to the index of a step within the metadata's step array, and tells the constructor that we want our new step's delay value to be added to the specified step (in this example we specify the first log-in attempt step, the second step with an index of `1`, so we make sure the claim step happens after it)


### Understanding JourneyProvider output

In `generate.py`, when `journey_provider.generate()` completes, it then calls `journey_provider.publish_journey(output_path)`. This tells the JourneyGenerator that we'd like it to export the completed journey, which takes the outputted document JSONs from the file system and zips them into the `output_path`. It also exports the `journey_metadata` dict as JSON into the same `output_path`, which can then be used by a publishing tool to "replay" the documents within the zip.


### Adding a New Journey Provider

The following is a TODO list for anyone adding a new journey provider:

1. Implement a new subclass of `JourneyProvider` within the `./journey_providers/` folder. Use a copy of `./journey_provider/starfleet.py` as a starting point. Give it a unique `name` value
2. Modify `./journey_providers/__init__.py` to add your new provider to the `journey_provider_mapping` and pop the `.name` property in there (which will be used in the CLI to call that journey provider)
3. Add some new steps to the journey (importing whichever DocumentProviders you wish to use)
3. (Optional but encouraged) Create some `pytest` tests in the `./tests/journey_providers` to validate your journey is outputting as expected

Make it so.


## Uploading fake data to Azure Storage

For the copying of local generated data to Azure storage, you can use the `azcopy` utility which is already included in the DevContainer set-up.

To use `azcopy` to transfer data that you've generated to Azure, follow the below steps (these assume that you have already opened the data-generator DevContainer in VSCode and have generated some fake data into `./output`):

1. In the Azure portal, navigate to the Azure storage account you'd like upload data to
2. Click on 'Containers' and create a container where you'd like to upload the files (if it doesn't exist already)
3. In that container, click on 'Properties' in the side menu and copy the container URL
3. Back in VSCode, in the DevContainer Bash shell, create an environment variable for the container name like so:
  ```bash
  export BLOB_CONTAINER_URL="~insert container URL here~"
  ```
4. Back to the portal, click on 'Shared Access Signature' in the left-hand menu of the Storage Account pane
5. Generate a SAS token (restrict it to only blob access and make sure containers and objects are checked)
6. Copy the SAS token (the string starting with `?sv=`) and save it as another environment variable:
  ```bash
  export BLOB_SAS_TOKEN="~insert SAS token here~"
  ```
7. Now you can run the command `make azcopy_output` to copy all the data from `./output` to your container in Azure

If you want to run other commands with `azcopy`, it's pre-installed in the DevContainer image, so you can use any of the commands outlined in the docs [here](https://docs.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-blobs?toc=/azure/storage/blobs/toc.json).

> Make sure that with every copy operation to and from Azure, you pass the SAS token you generated as a suffix to your blob URL. Alternatively, you can run `azcopy login` to authenticate via AAD and circumvent the need to pass a SAS token each time. All the different authentication methods are outlined [here](https://docs.microsoft.com/en-us/azure/storage/common/storage-use-azcopy-v10?toc=/azure/storage/blobs/toc.json).
