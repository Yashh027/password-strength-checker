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