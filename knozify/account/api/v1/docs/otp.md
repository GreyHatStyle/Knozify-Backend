# OTP Handler Documentation (AI Generated for now)

This module (`otp.py`) provides a class called `OTP_Handler` to manage One-Time Passwords (OTPs) for user authentication via phone numbers. It is designed to be used in Django projects and works with a Redis cache for storing OTPs.

## Features

- **OTP Generation:** Creates a random 6-digit OTP for a given phone number.
- **OTP Storage:** Stores the generated OTP in a Redis cache with an expiration time (default: 120 seconds + 10 seconds buffer).
- **OTP Sending:** Sends the OTP to the user's phone number using the TextBee API via a `curl` subprocess call (because for some reason `request` module didn't worked).
- **OTP Validation:** Verifies if the OTP provided by the user matches the one stored in the cache.
- **Expiration Handling:** Handles OTP expiration and provides a method to check the time left before expiration.

## How It Works

1. **Initialization:**  
   Create an instance of `OTP_Handler` with the user's phone number.
   ```python
   handler = OTP_Handler("+911234567890")
   ```

2. **Send OTP:**  
   Call `send_otp()` to generate and send an OTP to the user's phone. This also stores the OTP in the cache.
   ```python
   otp = handler.send_otp()
   ```

3. **Verify OTP:**  
   Use the static method `verify_otp(phone_no, otp)` to check if the user's input matches the stored OTP.
   ```python
   is_valid = OTP_Handler.verify_otp("+911234567890", "123456")
   ```

4. **Check Expiry:**  
   Use `time_left()` to get the number of seconds before the OTP expires.
   ```python
   seconds_left = handler.time_left()
   ```

## Notes

- The class uses Django's cache system (specifically the "otp" cache).
- The OTP is sent using the TextBee API. Make sure to set the `SMS_SENDER_API` and `TEXTBEE_API_KEY` environment variables.
- The OTP is valid for 120 seconds, with an additional 10-second buffer to account for network delays.

## Example Usage

```python
handler = OTP_Handler("+911234567890")
handler.send_otp()
# User receives OTP on their phone

# Later, to verify:
if OTP_Handler.verify_otp("+911234567890", user_input_otp):
    print("OTP is valid!")
else:
    print("Invalid OTP.")
```