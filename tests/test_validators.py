from app.validation.validation_utils import validate_uuid
import pytest
import uuid


def test_uuid_validator():
    with pytest.raises(ValueError):
        validate_uuid("1")
    with pytest.raises(ValueError):
        validate_uuid(1)
    uuid_str = str(uuid.uuid4())
    assert validate_uuid(uuid_str) == uuid_str
