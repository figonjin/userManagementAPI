def validate_fields(data, fields):
    missing_fields = []
    for field in fields:
        if field not in data or not data[field] or data[field] is None:
            missing_fields.append(field)
    return missing_fields


def validate_input(original_value, user_input):
    return user_input if user_input is not None and user_input != "" else original_value

