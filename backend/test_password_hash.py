"""
Test password hashing to debug the bcrypt 72-byte limit issue
"""
from auth import get_password_hash

# Test with various password lengths
test_passwords = [
    "short",
    "normalpassword123",
    "a" * 50,  # 50 characters
    "a" * 72,  # 72 characters (should be exactly 72 bytes if ASCII)
    "a" * 100,  # 100 characters (should be truncated)
    "test@example.com_password123",  # Normal password
]

print("Testing password hashing...")
for i, pwd in enumerate(test_passwords):
    try:
        pwd_bytes = pwd.encode('utf-8')
        print(f"\nTest {i+1}: Password length = {len(pwd)} chars, {len(pwd_bytes)} bytes")
        hash_result = get_password_hash(pwd)
        print(f"✅ Success: Hash length = {len(hash_result)}")
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n✅ All tests completed!")

