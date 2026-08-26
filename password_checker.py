import re
import hashlib
import requests


def check_password(user_pass):

    # ==========================================
    # BASIC PASSWORD CHARACTER CHECKS
    # ==========================================

    password_length = len(user_pass)

    # Checking for uppercase characters
    has_upper = False

    for char in user_pass:
        if char.isupper():
            has_upper = True
            break

    # Checking for lowercase characters
    has_lower = False

    for char in user_pass:
        if char.islower():
            has_lower = True
            break

    # Checking for digits
    has_digit = False

    for char in user_pass:
        if char.isdigit():
            has_digit = True
            break

    # Checking for special characters
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


    # ==========================================
    # REPEATED CHARACTER DETECTION
    # ==========================================

    has_repeated = False
    count = 1

    for i in range(1, len(user_pass)):

        if user_pass[i] == user_pass[i - 1]:

            count += 1

            if count == 3:
                has_repeated = True
                break

        else:
            count = 1


    # ==========================================
    # SEQUENTIAL CHARACTER DETECTION
    # ==========================================

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


    # ==========================================
    # WEAK PASSWORD DETECTION
    # ==========================================

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

    for weak_password in weak_passwords:

        if normalized_pass == weak_password:
            has_weakpass = True
            break


    # ==========================================
    # KEYBOARD PATTERN DETECTION
    # ==========================================

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

    for pattern in keyboard_pattern:

        if pattern in user_pass.lower():
            has_keypattern = True
            break


    # ==========================================
    # CREATING SHA-1 HASH LOCALLY
    # ==========================================

    password_hash = hashlib.sha1(
        user_pass.encode("utf-8")
    ).hexdigest().upper()

    hash_prefix = password_hash[:5]
    hash_suffix = password_hash[5:]


    # ==========================================
    # HIBP PASSWORD BREACH CHECK
    # ==========================================

    is_compromised = False
    breach_count = 0
    hibp_available = False

    try:

        url = f"https://api.pwnedpasswords.com/range/{hash_prefix}"

        response = requests.get(
            url,
            timeout=10
        )

        response.raise_for_status()

        hibp_available = True

        for line in response.text.splitlines():

            returned_suffix, count = line.split(":")

            if returned_suffix == hash_suffix:

                is_compromised = True
                breach_count = int(count)

                break

    except requests.exceptions.Timeout:

        pass

    except requests.exceptions.RequestException:

        pass


    # ==========================================
    # PASSWORD SECURITY SCORING
    # ==========================================

    score = 100


    # ---------- PENALTIES ----------

    if password_length < 8:
        score -= 20

    if has_weakpass:
        score -= 40

    if has_sequence:
        score -= 30

    if has_repeated:
        score -= 20

    if has_keypattern:
        score -= 30


    # ---------- LENGTH BONUSES ----------

    if password_length >= 12:
        score += 15

    if password_length >= 16:
        score += 20


    # ---------- PREDICTABILITY BONUS ----------

    if not has_sequence and not has_repeated and not has_keypattern:
        score += 10


    # ---------- HIBP COMPROMISE PENALTY ----------

    if is_compromised:

        if breach_count >= 1_000_000:
            score -= 50

        elif breach_count >= 10_000:
            score -= 40

        elif breach_count >= 100:
            score -= 30

        elif breach_count >= 10:
            score -= 20

        else:
            score -= 10


    # ---------- SEVERITY CAPS ----------

    if has_sequence and password_length < 12:
        score = min(score, 39)

    if has_repeated and password_length < 12:
        score = min(score, 39)

    if has_keypattern:
        score = min(score, 39)

    if has_weakpass:
        score = min(score, 49)

    if is_compromised:
        score = min(score, 49)


    # ---------- SCORE LIMIT ----------

    score = max(0, min(score, 100))


    # ==========================================
    # FINAL SECURITY RATING
    # ==========================================

    if score >= 80:
        rating = "Strong"

    elif score >= 60:
        rating = "Moderate"

    elif score >= 40:
        rating = "Weak"

    else:
        rating = "Very Weak"


    # ==========================================
    # RETURN RESULTS TO GUI
    # ==========================================

    return {
        "length": password_length,
        "has_upper": has_upper,
        "has_lower": has_lower,
        "has_digit": has_digit,
        "has_special": has_special,
        "has_repeated": has_repeated,
        "has_sequence": has_sequence,
        "has_weakpass": has_weakpass,
        "has_keypattern": has_keypattern,
        "score": score,
        "rating": rating,
        "is_compromised": is_compromised,
        "breach_count": breach_count,
        "hibp_available": hibp_available
    }


# ==========================================
# TERMINAL TEST
# ==========================================

if __name__ == "__main__":

    user_pass = input("Enter the Password : ")

    result = check_password(user_pass)

    print("\n==============================")
    print("PASSWORD SECURITY ASSESSMENT")
    print("==============================")

    print("Password length :", result["length"])

    print(
        "Contains Uppercase :",
        "Yes" if result["has_upper"] else "No"
    )

    print(
        "Contains Lowercase :",
        "Yes" if result["has_lower"] else "No"
    )

    print(
        "Contains Number :",
        "Yes" if result["has_digit"] else "No"
    )

    print(
        "Contains Special Character :",
        "Yes" if result["has_special"] else "No"
    )

    print(
        "Repeated Characters :",
        "Suspicious" if result["has_repeated"] else "Not Suspicious"
    )

    print(
        "Sequential Characters :",
        "Suspicious" if result["has_sequence"] else "Not Suspicious"
    )

    print(
        "Weak Password :",
        "Yes" if result["has_weakpass"] else "No"
    )

    print(
        "Keyboard Pattern :",
        "Yes" if result["has_keypattern"] else "No"
    )

    print("\n==============================")
    print("PASSWORD SECURITY ASSESSMENT")
    print("==============================")

    print("Security Score :", result["score"], "/ 100")
    print("Security Rating:", result["rating"])

    if not result["hibp_available"]:

        print("Compromised Password : UNKNOWN")
        print("HIBP Status : Service unavailable")

    elif result["is_compromised"]:

        print("Compromised Password : YES")
        print(
            "Times Seen in Breaches :",
            result["breach_count"]
        )

    else:

        print("Compromised Password : NO")