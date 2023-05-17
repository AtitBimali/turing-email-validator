from typing import Tuple, Dict
import re

def validate_email_addr(email_addr: str) -> bool:
    """
    Returns True if the email_addr is valid per specification. Otherwise, return False.
    """
    # Total length of email too long.
    if len(email_addr) > 254:
        return False

    # No domain!
    if email_addr.count('@') != 1:
        return False
    split_email = email_addr.split("@")
    first_part = split_email[0]
    last_part = split_email[1]
    if len(first_part) > 64:
        return False
    if len(last_part) > 251:
        return False
    if first_part.startswith(".") or first_part.endswith(".") or first_part.startswith("-") or first_part.endswith("-"):
            raise ValueError("Email address local part cannot start or end with a dot or hyphen.")

    if "." in last_part[:-4] or last_part.endswith(".") or last_part.startswith("."):
            raise ValueError("Email address domain part contains invalid dot placement.")

    if not last_part.lower().endswith((".com", ".net", ".org")):
            raise ValueError("Email address must end with '.com', '.net', or '.org'.")

    for c in email_addr:
        if not c in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@.':
            return False

    return True


def validate_email_payload(sender_name: str, sender_addr: str, receiver_name: str, receiver_addr: str, html: str,
                           replacements: Dict) -> bool:
    """
    Returns True if the payload is validated and is safe to send out. Otherwise, return False.
    """
    if len(sender_name) > 30 or len(sender_name) < 5:
        return False

    if len(receiver_name) > 30 or len(receiver_name) < 5:
        return False

    if not validate_email_addr(sender_addr):
        return False

    if not validate_email_addr(receiver_addr):
        return False
    tags = re.findall(r'\{(\w+)\}', html)
    replacements_keys = set(replacements.keys())

    if len(replacements_keys - set(tags)) > 0:
        return False
    if set(tags) - replacements_keys:
        return False
    for key, value in replacements.items():
        if not value:
            return False
    return True


# Function Test
sender_name = "John Doe"
sender_addr = "john.doe@example.com"
receiver_name = "Jane Smith"
receiver_addr = "jane.smith@example.com"
html = "Hello {name}! Thank you for subscribing to our newsletter."
replacements = {'name': 'Jane'}

try:
    validate_email_addr(sender_addr)
    print("Email address is valid.")
except ValueError as e:
    print("Email address failed:", str(e))

try:
    validate_email_payload(sender_name, sender_addr, receiver_name, receiver_addr, html, replacements)
    print("Email payload is valid.")
except ValueError as e:
    print("Email payload validation failed:", str(e))