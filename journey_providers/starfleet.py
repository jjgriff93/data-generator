from journey_providers.helper_functions import days, minutes
import random
from mimesis.providers.date import Datetime
from mimesis.providers.generic import Generic

from document_providers.starfleet_account import StarfleetAccount
from document_providers.starfleet_application import StarfleetApplication
from journey_providers.journey_provider import JourneyProvider


fake = Generic("en-GB")


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

        # =====================================================================================
        # 2. User attempts log in varied no. of times during process, modifying account document
        updated_account_document = account_document
        updated_account_step = 0

        # Random number of attempts between 1 and 10
        for i in range(random.randint(1, 10)):
            updated_account_document["auth"]["logins"].append(
                {
                    "timestamp": str(
                            fake.datetime.date(
                                start=Datetime.CURRENT_YEAR - 1,
                                end=Datetime.CURRENT_YEAR,
                            )
                        )
                }
            )

            # Add the step with a delay + the delay from account step (as log-ins happen after that)
            updated_account_step = self.add_step(
                StarfleetAccount,
                updated_account_document,
                delay=[minutes(1), days(1)],
                delay_from_step_index=updated_account_step,
            )

        # ==========================================================================
        # 3. User then submits the completed claim which generates a starfleet_application document
        application_document = StarfleetApplication().generate()

        # Replace sumbission claimant details with generated ones
        application_document["accountId"] = str(self.user_id)

        # Replace account details with ones from account document
        application_document["details"]["forename"] = account_document["forename"]
        application_document["details"]["surname"] = account_document["surname"]
        application_document["details"]["title"] = account_document["title"]
        application_document["details"]["communicator"] = account_document["communicator"]
        application_document["details"]["federation_citizen_id"] = account_document["federation_citizen_id"]

        # starfleet_application will be final action, thus delay needs to be higher than the max
        # delay fom any step within the metadata - thus pass final_step() helper function
        self.add_step(
            StarfleetApplication,
            application_document,
            delay=[minutes(1), days(1)],
            delay_from_step_index=self.final_step(),
        )
