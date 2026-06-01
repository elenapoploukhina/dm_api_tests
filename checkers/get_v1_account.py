from datetime import datetime

from hamcrest import (
    assert_that,
    has_property,
    all_of,
    equal_to,
    has_properties,
    starts_with,
    contains_inanyorder,
    instance_of,
)

from data.constants import LOGIN_START_PART
from dm_api_account.models.user_details_envelope import (
    UserDetailsEnvelope,
    ColorSchema,
)
from dm_api_account.models.user_envelope import UserRole


class GetV1Account:
    @classmethod
    def check_response_values(
            cls,
            response: UserDetailsEnvelope
    ):
        assert_that(
            response, has_property(
                "resource", all_of(
                    has_property("info", equal_to("")),
                    has_property(
                        "settings", all_of(
                            has_property("color_schema", equal_to(ColorSchema.MODERN)),
                            has_property(
                                "paging", has_properties(
                                    {
                                        "posts_per_page": equal_to(10),
                                        "comments_per_page": equal_to(10),
                                        "topics_per_page": equal_to(10),
                                        "messages_per_page": equal_to(10),
                                        "entities_per_page": equal_to(10)
                                    }
                                )
                            )
                        )
                    ),
                    has_property("login", starts_with(LOGIN_START_PART)),
                    has_property("roles", contains_inanyorder(UserRole.GUEST, UserRole.PLAYER)),
                    has_property(
                        "rating", has_properties(
                            {
                                "enabled": equal_to(True),
                                "quality": equal_to(0),
                                "quantity": equal_to(0)
                            }
                        )
                    ),
                    has_property("online", instance_of(datetime)),
                    has_property("registration", instance_of(datetime))
                )
            )
        )
