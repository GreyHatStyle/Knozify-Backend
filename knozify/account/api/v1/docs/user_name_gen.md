# Username Generator Utility Documentation (AI generated)

This module (`user_name_gen.py`) provides a class called `Generate_Username` that helps create unique and available usernames for new users, based on their first name, last name, and birth date.

## Main Class: `Generate_Username`

### Purpose

- **Suggest Unique Usernames:**  
  Automatically generates username suggestions that are not already taken in the database.
- **Flexible Patterns:**  
  Combines first name, last name, special characters, and birth date in different ways to maximize the chance of finding an available username.

### How It Works

1. **Initialization:**  
   When you create an instance, you provide the user's first name, last name, and birth date.
   ```python
   gen = Generate_Username("john", "doe", "2000-01-15")
   ```

2. **Username Patterns:**  
   The class tries several patterns to generate usernames:
   - `[FirstName][SpecialChar][LastName]`  
   - `[FirstName][SpecialChar][LastName][SpecialChar]`  
   - `[FirstName][SpecialChar][LastName][SpecialChar][BirthDay]`  
   - `[SpecialChar][FirstName][SpecialChar][LastName][SpecialChar][BirthDay]`  
   Special characters used: `_`, `.`, `-`, or nothing.

3. **Checking Availability:**  
   For each pattern, it checks if the username is already taken in the database. If it finds an available one, it returns it immediately.

4. **Batch Checking:**  
   For patterns that generate many combinations, it checks them in batches for efficiency.

5. **Fallback:**  
   If no available username is found, it returns `"can't suggest name for now"`.

### Example Usage

```python
gen = Generate_Username("alice", "smith", "1995-07-20")
suggested_username = gen.generate_unique_name()
print(suggested_username)  # e.g., "alice_smith" or "alice-smith20"
```

### Methods Overview

- `f_sp_l()`:  
  Tries `[FirstName][SpecialChar][LastName]` combinations.

- `f_sp_l_sp()`:  
  Tries `[FirstName][SpecialChar][LastName][SpecialChar]` combinations.

- `f_sp_l_sp_bd()`:  
  Tries `[FirstName][SpecialChar][LastName][SpecialChar][BirthDay]` combinations.

- `sp_f_sp_l_sp_bd()`:  
  Tries `[SpecialChar][FirstName][SpecialChar][LastName][SpecialChar][BirthDay]` combinations, in batches.

- `generate_unique_name()`:  
  Calls the above methods in order and returns the first available username.

### Notes

- The class uses Django's ORM to check for existing usernames.
- The birth date should be in `"YYYY-MM-DD"` format.
- This utility is used in the API to help users pick a username that is both unique and relevant to their name.

---
