
import os
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv
from pwdlib import PasswordHash


# Load environment variables from .env
load_dotenv()


# Password hashing configuration
password_hash = PasswordHash.recommended()


# JWT configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
)


# Check whether the JWT secret exists
if not JWT_SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY is missing from .env")


# 1. Hash a password
def hash_password(password: str) -> str:
    return password_hash.hash(password)


# 2. Verify a password
def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


# 3. Generate a JWT access token
def create_access_token(data: dict) -> str:

    # Create a copy of the user information
    to_encode = data.copy()

    # Calculate token expiration time
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # Add expiration time to the token data
    to_encode.update({"exp": expire})

    # Generate and return the JWT token
    encoded_jwt = jwt.encode(
        to_encode,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )

    return encoded_jwt


# 4. Verify a JWT access token
def verify_access_token(token: str):

    try:
        # Decode and verify the token
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )

        return payload

    except jwt.InvalidTokenError:
        return None
