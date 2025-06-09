# Login Support Utility Documentation

This module (`login_support.py`) provides helper functions for managing login attempts and extracting client IP addresses, mainly for security and rate-limiting purposes.

## Main Class: `Login_Support`

### Purpose

- **Track Login Attempts:**  
  Helps keep track of how many login attempts a user (or IP address) has left before being throttled (blocked for a while).
- **Extract Client IP Address:**  
  Retrieves the user's IP address (IPv4 or IPv6) from the request, which is important for rate-limiting and security checks.

### Key Methods

#### 1. `get_client_ipv6(request)`

- **What it does:**  
  Tries to extract the client's IPv6 address from the request. If not found, falls back to IPv4 or returns "Unknown".
- **How it works:**  
  - Checks HTTP headers like `HTTP_X_FORWARDED_FOR` and `HTTP_X_REAL_IPV6`.
  - If none found, uses `REMOTE_ADDR`.
- **Why:**  
  Useful for identifying users uniquely, especially when rate-limiting by IP.

#### 2. `get_attempts_left(request)`

- **What it does:**  
  Returns the number of login attempts left for the current IP address before throttling kicks in.
- **How it works:**  
  - Uses the IP address (from `get_client_ipv6`) to build a cache key.
  - Looks up this key in Django's cache (usually backed by Redis).
- **Why:**  
  Helps prevent brute-force attacks by limiting repeated login attempts.

### Example Usage

```python
support = Login_Support()
ip = support.get_client_ipv6(request)
attempts_left = support.get_attempts_left(request)
```

### Notes

- This utility is typically used in login APIs to enforce security and rate limits.
- The cache key format is: `login_attempt_{ip_address}_attempt_left`
- Works with both IPv4 and IPv6 addresses.

---
