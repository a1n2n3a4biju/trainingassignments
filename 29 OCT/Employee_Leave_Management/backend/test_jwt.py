
from security import create_access_token, verify_access_token


# Sample user information
user_data = {
    "user_id": 1,
    "username": "arun",
    "role": "EMPLOYEE"
}


# Generate a token
token = create_access_token(user_data)

print("Generated JWT:")
print(token)


# Verify the generated token
decoded_data = verify_access_token(token)

print("\nVerified token data:")
print(decoded_data)


# Test an invalid token
invalid_data = verify_access_token("invalid.token.value")

print("\nInvalid token result:")
print(invalid_data)
