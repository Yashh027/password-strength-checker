import hashlib
import requests
from pathlib import Path
import sys

# ============================================================
# LOAD COMMON PASSWORD DATABASE
# ============================================================

def load_common_passwords():

    if getattr(sys, "frozen", False):
        password_file = Path(sys._MEIPASS) / "common_passwords.txt"
    else:
        password_file = Path(__file__).parent / "common_passwords.txt"

    try:

        with password_file.open(
            "r",
            encoding="utf-8"
        ) as file:

            return {
                line.strip().lower()
                for line in file
                if line.strip()
            }

    except FileNotFoundError:

        return set()


# ============================================================
# PREDICTABLE MODIFICATION DETECTION
# ============================================================

def check_predictable_modification(
    user_pass,
    common_passwords
):

    normalized_pass = user_pass.lower()

    for common_password in common_passwords:

        if normalized_pass == common_password:
            continue

        # Common password followed by numbers/small modification
        if normalized_pass.startswith(common_password):

            remaining = normalized_pass[len(common_password):]

            if remaining.isdigit():
                return True

            if 0 < len(remaining) <= 3:
                return True

        # Numbers/small modification followed by common password
        if normalized_pass.endswith(common_password):

            remaining = normalized_pass[:-len(common_password)]

            if remaining.isdigit():
                return True

            if 0 < len(remaining) <= 3:
                return True

    return False


# ============================================================
# PASSWORD SECURITY ANALYSIS
# ============================================================

def check_password(user_pass):

    # ========================================================
    # BASIC CHARACTER CHECKS
    # ========================================================

    password_length = len(user_pass)

    has_upper = any(
        char.isupper()
        for char in user_pass
    )

    has_lower = any(
        char.islower()
        for char in user_pass
    )

    has_digit = any(
        char.isdigit()
        for char in user_pass
    )

    has_special = any(
        not char.isalnum() and not char.isspace()
        for char in user_pass
    )


    # ========================================================
    # REPEATED CHARACTER DETECTION
    # ========================================================

    has_repeated = False
    count = 1

    for i in range(1, len(user_pass)):

        if user_pass[i] == user_pass[i - 1]:

            count += 1

            if count >= 3:
                has_repeated = True
                break

        else:

            count = 1


    # ========================================================
    # SEQUENTIAL CHARACTER DETECTION
    # ========================================================

    has_sequence = False
    sequence_count = 1

    for i in range(1, len(user_pass)):

        current_char = user_pass[i]
        previous_char = user_pass[i - 1]

        difference = (
            ord(current_char)
            - ord(previous_char)
        )

        if difference == 1 or difference == -1:

            sequence_count += 1

            if sequence_count >= 3:
                has_sequence = True
                break

        else:

            sequence_count = 1


    # ========================================================
    # COMMON PASSWORD DETECTION
    # ========================================================

    common_passwords = load_common_passwords()

    normalized_pass = user_pass.strip().lower()

    has_weakpass = (
        normalized_pass in common_passwords
    )


    # ========================================================
    # PREDICTABLE MODIFICATION DETECTION
    # ========================================================

    has_predictable_modification = (
        check_predictable_modification(
            user_pass,
            common_passwords
        )
    )


    # ========================================================
    # KEYBOARD PATTERN DETECTION
    # ========================================================

    keyboard_patterns = [

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

    normalized_for_pattern = user_pass.lower()

    for pattern in keyboard_patterns:

        if pattern in normalized_for_pattern:

            has_keypattern = True
            break


    # ========================================================
    # HIBP PASSWORD BREACH CHECK
    # ========================================================

    is_compromised = False
    breach_count = 0
    hibp_available = False

    # SHA-1 is used because HIBP's range API requires it.
    # Only the first 5 characters of the hash are sent.

    password_hash = hashlib.sha1(
        user_pass.encode("utf-8")
    ).hexdigest().upper()

    hash_prefix = password_hash[:5]
    hash_suffix = password_hash[5:]

    try:

        url = (
            "https://api.pwnedpasswords.com/range/"
            + hash_prefix
        )

        response = requests.get(
            url,
            headers={
                "User-Agent": "Password-Security-Analyzer"
            },
            timeout=10
        )

        response.raise_for_status()

        hibp_available = True

        for line in response.text.splitlines():

            parts = line.split(":")

            if len(parts) != 2:
                continue

            returned_suffix = parts[0]
            count = parts[1]

            if returned_suffix == hash_suffix:

                is_compromised = True
                breach_count = int(count)

                break

    except (
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError,
        requests.exceptions.RequestException,
        ValueError
    ):

        hibp_available = False


    # ========================================================
    # COUNT SECURITY WEAKNESSES
    # ========================================================

    weaknesses = 0

    if not has_upper:
        weaknesses += 1

    if not has_lower:
        weaknesses += 1

    if not has_digit:
        weaknesses += 1

    if not has_special:
        weaknesses += 1

    if password_length < 12:
        weaknesses += 1

    if has_repeated:
        weaknesses += 1

    if has_sequence:
        weaknesses += 1

    if has_keypattern:
        weaknesses += 1

    if has_weakpass:
        weaknesses += 1

    if has_predictable_modification:
        weaknesses += 1


    # ========================================================
    # SECURITY RATING
    # ========================================================

    if has_weakpass:

        rating = "Very Weak"

    elif has_keypattern:

        rating = "Very Weak"

    elif is_compromised:

        rating = "Weak"

    elif weaknesses >= 4:

        rating = "Very Weak"

    elif weaknesses >= 2:

        rating = "Weak"

    elif weaknesses == 1:

        rating = "Moderate"

    else:

        rating = "Strong"


    # ========================================================
    # THREAT LEVEL
    # ========================================================

    if is_compromised:

        threat_level = "CRITICAL RISK"

    elif has_weakpass:

        threat_level = "HIGH RISK"

    elif has_keypattern:

        threat_level = "HIGH RISK"

    elif has_predictable_modification:

        threat_level = "HIGH RISK"

    elif weaknesses >= 4:

        threat_level = "HIGH RISK"

    elif weaknesses >= 2:

        threat_level = "MEDIUM RISK"

    elif weaknesses == 1:

        threat_level = "LOW RISK"

    else:

        threat_level = "MINIMAL RISK"


    # ========================================================
    # RETURN RESULTS
    # ========================================================

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

        "has_predictable_modification":
            has_predictable_modification,

        "rating": rating,

        "threat_level": threat_level,

        "is_compromised": is_compromised,

        "breach_count": breach_count,

        "hibp_available": hibp_available

    }


# ============================================================
# TERMINAL TEST
# ============================================================

if __name__ == "__main__":

    user_pass = input(
        "Enter the Password: "
    )

    result = check_password(user_pass)

    print("\n==============================")
    print("PASSWORD SECURITY ANALYSIS")
    print("==============================")

    print(
        "Password Length:",
        result["length"]
    )

    print(
        "Uppercase:",
        "Yes" if result["has_upper"] else "No"
    )

    print(
        "Lowercase:",
        "Yes" if result["has_lower"] else "No"
    )

    print(
        "Number:",
        "Yes" if result["has_digit"] else "No"
    )

    print(
        "Special Character:",
        "Yes" if result["has_special"] else "No"
    )

    print(
        "Repeated Characters:",
        "Detected" if result["has_repeated"]
        else "Not Detected"
    )

    print(
        "Sequential Pattern:",
        "Detected" if result["has_sequence"]
        else "Not Detected"
    )

    print(
        "Common Password:",
        "Yes" if result["has_weakpass"]
        else "No"
    )

    print(
        "Keyboard Pattern:",
        "Detected" if result["has_keypattern"]
        else "Not Detected"
    )

    print(
        "Predictable Modification:",
        "Detected"
        if result["has_predictable_modification"]
        else "Not Detected"
    )

    print("\n==============================")
    print("SECURITY VERDICT")
    print("==============================")

    print(
        "Rating:",
        result["rating"]
    )

    print(
        "Threat Level:",
        result["threat_level"]
    )

    if not result["hibp_available"]:

        print(
            "Compromised Password: UNKNOWN"
        )

        print(
            "HIBP Status: Service unavailable"
        )

    elif result["is_compromised"]:

        print(
            "Compromised Password: YES"
        )

        print(
            "Times Seen in Breaches:",
            result["breach_count"]
        )

    else:

        print(
            "Compromised Password: NO"
        )