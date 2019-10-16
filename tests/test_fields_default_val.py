from .utils.fixtures import missing_user_validator_1


def test_fields_default_val(missing_user_validator_1):
    """
    Tests that fields default val
    """
    assert missing_user_validator_1.is_valid()

    assert "@" in missing_user_validator_1.email
    assert 10 < missing_user_validator_1.age < 100

    missing_user_validator_1.age = 88
    assert missing_user_validator_1.age == 88



