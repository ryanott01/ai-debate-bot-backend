from typing import Dict, List, Any, Optional

def validate_generate_request(data: Dict[str, Any]) -> List[str]:
    """Validate the generate request payload.

    Returns:
        List of error messages, empty if valid
    """
    errors = []

    # Check required fields
    if "provider" not in data:
        errors.append("Missing 'provider' field")
    elif not isinstance(data["provider"], str):
        errors.append("'provider' must be a string")

    if "model" not in data:
        errors.append("Missing 'model' field")
    elif not isinstance(data["model"], str):
        errors.append("'model' must be a string")

    if "messages" not in data:
        errors.append("Missing 'messages' field")
    elif not isinstance(data["messages"], list):
        errors.append("'messages' must be a list")
    else:
        # Validate message format
        for i, msg in enumerate(data["messages"]):
            msg_errors = validate_message(msg)
            for error in msg_errors:
                errors.append(f"Message {i}: {error}")

    return errors

def validate_message(message: Any) -> List[str]:
    """Validate a single message object."""
    errors = []

    if not isinstance(message, dict):
        return ["Message must be an object"]

    if "role" not in message:
        errors.append("Missing 'role' field")
    elif not isinstance(message["role"], str):
        errors.append("'role' must be a string")
    elif message["role"] not in ["system", "user", "assistant"]:
        errors.append("'role' must be one of: system, user, assistant")

    if "content" not in message:
        errors.append("Missing 'content' field")
    elif not isinstance(message["content"], str):
        errors.append("'content' must be a string")

    return errors
