from datetime import datetime

from hamcrest import (
    assert_that,
    all_of,
    has_property,
    starts_with,
    instance_of,
    equal_to,
    has_properties,
)

from data.constants import LOGIN_START_PART
from dm_api_account.models.user_envelope import UserEnvelope


class PostV1Account:
    @classmethod
    def check_response_values(
            cls,
            response: UserEnvelope
    ):
        today = datetime.now().strftime("%Y-%m-%d")
        assert_that(str(response.resource.registration), starts_with(today))
        assert_that(
            response, all_of(
                has_property("resource", has_property("login", starts_with(LOGIN_START_PART))),
                has_property("resource", has_property("registration", instance_of(datetime))),
                has_property(
                    "resource", has_property(
                        "rating", has_properties(
                            {
                                "enabled": equal_to(True),
                                "quality": equal_to(0),
                                "quantity": equal_to(0)
                            }
                        )
                    )
                )
            )
        )
