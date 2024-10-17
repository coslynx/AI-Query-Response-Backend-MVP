# Specify version and import
from werkzeug.security import generate_password_hash, check_password_hash  # Version: 2.2.2

# Specify version and import
from typing import Optional  # Version: 2.9.2

# Specify version and import
import os  #  No specific version required

# Specify version and import
from ..config.settings import Settings  # Version: 2.9.2

def hash_password(password: str) -> str:
    """Hash a user password using a secure algorithm.

    Args:
        password (str): The user's plain password.

    Returns:
        str: The hashed password.
    """
    return generate_password_hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password.

    Args:
        plain_password (str): The user's plain password.
        hashed_password (str): The hashed password stored in the database.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return check_password_hash(hashed_password, plain_password)