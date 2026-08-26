import re
# Taking password input from the user
user_pass = input("Enter the Password : ")

# Checking and displaying the length of the password 
print("Password length:" + str(len(user_pass)))

# Checking for uppercase characters in password and displaying the Result
has_upper = False
for char in user_pass:
    if char.isupper():
        has_upper = True
        break
if has_upper:
    print("Contains Uppercase : Yes")
else:
    print("Contains Uppercase : No")
    
# Checking for lowercase characters in password and displaying the Result
has_lower = False
for char in user_pass:
    if char.islower():
        has_lower = True
        break
if has_lower:
    print("Contains Lowercase : Yes")
else:
    print("Contains Lowercase : No")
    
# Checking for digits in password and displaying the Result
has_digit = False
for char in user_pass:
    if char.isdigit():
        has_digit = True
        break
if has_digit:
    print("Contains Number : Yes")
else:
    print("Contains Number : No")
    
# Checking for special characters in password and displaying the Result
has_special = False
for char in user_pass:
    if char.isupper():
        has_special = False
    elif char.islower():
        has_special = False
    elif char.isdigit():
        has_special = False
    elif char == " ":
        has_special = False
    else:
        has_special = True
        break
    # if char == "!" or char == "@" or char == "#" or char == "$" or char == "%" or char == "^" or char == "&" or char == "*" or char == "(" or char == ")" or char == "-" or char == "_" or char == "=" or char == "+" or char == '"':
if has_special:
    print("Contains Special Character : Yes")
else:    
    print("Contains Special Character : No")

# Checking for repeated characters
has_repeated = False
count = 1  # Start at 1 because a single character is a streak of 1

# Start from the 2nd character (index 1)
for i in range(1, len(user_pass)):
    if user_pass[i] == user_pass[i - 1]:
        count += 1
        if count == 3:
            has_repeated = True
            break  # Exit immediately since we found a triple repeat
    else:
        count = 1  # Reset streak back to 1 if the characters don't match

if has_repeated:
    print("Repeated Characters : Suspicious")
else:
    print("Repeated Characters : Not Suspicious")

# Checking for sequential characters
has_sequence = False
sequence_count = 1

for i in range(1, len(user_pass)):
    current_char = user_pass[i]
    previous_char = user_pass[i - 1]

    diff = ord(current_char) - ord(previous_char)
    if diff == 1 or diff == -1:
        sequence_count += 1
        if sequence_count == 3:
            has_sequence = True
            break
    else:
        sequence_count = 1

if has_sequence:
    print("Sequential Characters : Suspicious")
else:
    print("Sequential Characters : Not Suspicious")

# Checking for weak passwords
weak_passwords = [
    "password",
    "123456",
    "qwerty",
    "admin",
    "welcome",
    "abc123"
]

normalized_pass = user_pass.lower()
normalized_pass = re.sub(r"[\d\W_]+$", "", normalized_pass)

has_weakpass = False
for i in weak_passwords:
    if normalized_pass == i:
        has_weakpass = True
        break
    else:
        continue
if has_weakpass:
    print("Weak Password : Yes")
else:
    print("Weak Password : No")

# Checking for Keyboard Pattern Detection 
keyboard_pattern = [
    "qwerty",
    "asdfgh",
    "zxcvbn",
    "123456",
    "1qaz2wsx",
    "qwertyuiop",
    "asdfghjkl",
    "zxcvbnm",
    "1234567890"
]

has_keypattern = False
for i in keyboard_pattern:
    if i in user_pass.lower():
        has_keypattern = True
        break

if has_keypattern:
    print("Keyboard Pattern : Yes")
else:
    print("Keyboard Pattern : No")

# ==========================================
# PASSWORD SECURITY SCORING
# ==========================================

score = 100

# ---------- PENALTIES ----------

# Very short password
if len(user_pass) < 8:
    score -= 20

# Common / weak password
if has_weakpass:
    score -= 40

# Sequential characters
if has_sequence:
    score -= 30

# Repeated characters
if has_repeated:
    score -= 20

# Keyboard pattern
if has_keypattern:
    score -= 30


# ---------- LENGTH BONUSES ----------

# Good password length
if len(user_pass) >= 12:
    score += 15

# Strong password length
if len(user_pass) >= 16:
    score += 20


# ---------- PREDICTABILITY BONUS ----------

# Give a small bonus only when none of our
# currently detected predictable patterns exist.
if not has_sequence and not has_repeated and not has_keypattern:
    score += 10


# ---------- SCORE LIMIT ----------

# Keep score between 0 and 100
score = max(0, min(score, 100))

# ==========================================
# SEVERITY CAPS
# ==========================================

# Extremely predictable passwords should never
# receive a high security rating.

if has_sequence and len(user_pass) < 12:
    score = min(score, 39)

if has_repeated and len(user_pass) < 12:
    score = min(score, 39)

if has_keypattern:
    score = min(score, 39)

if has_weakpass:
    score = min(score, 49)
    
# ---------- FINAL RATING ----------

if score >= 80:
    rating = "Strong"
elif score >= 60:
    rating = "Moderate"
elif score >= 40:
    rating = "Weak"
else:
    rating = "Very Weak"


print("\n==============================")
print("PASSWORD SECURITY ASSESSMENT")
print("==============================")
print("Security Score :", score, "/ 100")
print("Security Rating:", rating)