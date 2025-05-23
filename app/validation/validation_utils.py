from uuid import UUID


def validate_uuid(uuid_to_test) -> str:
    """
        Validates an uuid as string and returns it back
        will raise ValueError if there is a problem
    """
    try:
        return str(UUID(uuid_to_test))
    except Exception as e:
        # We just want ValueError out and do not care about the more detailed exceptions
        raise ValueError(e)
