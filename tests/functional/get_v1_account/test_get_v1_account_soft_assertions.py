from datetime import datetime

from assertpy import (
    assert_that,
    soft_assertions,
)
from vyper import v

from dm_api_account.models.user_details_envelope import ColorSchema
from dm_api_account.models.user_envelope import UserRole


def test_get_v1_account_auth_soft_assertions(
        auth_account_helper
):
    response = auth_account_helper.get_user(validate_response=True)
    with soft_assertions():
        assert_that(response.resource.info).is_empty()
        assert_that(response.resource.settings.color_schema).is_equal_to(ColorSchema.MODERN)
        assert_that(response.resource.login).is_equal_to(v.get('user.login'))
        assert_that(response.resource.roles).contains_only(UserRole.GUEST, UserRole.PLAYER)
        assert_that(response.resource.rating.enabled).is_true()
        assert_that(response.resource.online).is_instance_of(datetime)
        # Проверка нескольких ошибок
        # assert_that(response.resource.info).is_not_empty()
        # assert_that(response.resource.settings.color_schema).is_equal_to(ColorSchema.CLASSIC)
        # assert_that(response.resource.login).is_equal_to(LOGIN_START_PART)
        # assert_that(response.resource.roles).contains_only(UserRole.GUEST, UserRole.NANNY_MODERATOR)
        # assert_that(response.resource.rating.enabled).is_false()
        # assert_that(response.resource.online).is_instance_of(str)
