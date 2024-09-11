import secrets

# Generate a secure random key (e.g., 32 bytes)
secret_key = secrets.token_hex(32)
print(f"Your secret key: {secret_key}")