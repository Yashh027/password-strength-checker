# Password Security Analyzer

A Python-based cybersecurity project that analyzes password security using multiple security checks and verifies whether a password has appeared in known data breaches.

## Developed By

**Yash Pathak**

Cybersecurity Project

---

## Project Overview

Password Security Analyzer is a desktop-based cybersecurity tool developed using Python and Tkinter.

The application evaluates a password using several security indicators and generates an overall security score from 0 to 100.

It also checks whether the password has been exposed in known data breaches using the Have I Been Pwned (HIBP) Pwned Passwords API.

The application is designed for educational and cybersecurity awareness purposes.

---

## Features

### Password Analysis

The application checks:

- Password length
- Uppercase characters
- Lowercase characters
- Numbers
- Special characters
- Repeated characters
- Sequential characters
- Common or weak passwords
- Keyboard patterns

### Security Scoring

The password receives a security score between:

**0 – 100**

The application assigns one of four security ratings:

| Score | Rating |
|------:|--------|
| 80–100 | Strong |
| 60–79 | Moderate |
| 40–59 | Weak |
| 0–39 | Very Weak |

The scoring system considers password complexity, predictability, password length, and breach exposure.

### Breach Detection

The application uses the Have I Been Pwned Pwned Passwords API to determine whether a password has appeared in known breaches.

The application uses the API's k-anonymity approach:

1. The password is hashed locally using SHA-1.
2. Only the first five characters of the hash are sent to the API.
3. The remaining hash suffix is compared locally.
4. The original password itself is never sent to the API.

If a match is found, the application displays the number of times the password has appeared in known breach data.

---

## Technologies Used

- Python
- Tkinter
- Regular Expressions
- SHA-1 Hashing
- Requests Library
- Have I Been Pwned Pwned Passwords API

---

## Project Structure

```text
password-strength-checker/
│
├── gui.py
│       Graphical user interface for the application.
│
├── password_checker.py
│       Password analysis, scoring and breach-checking logic.
│
├── README.md
│       Project documentation.
│
├── requirements.txt
│       Required Python packages.
│
├── .gitignore
│       Files excluded from version control.
│
└── LICENSE
        License and usage information.
Installation
1. Clone the Repository

Clone the project from GitHub:

git clone https://github.com/Yashh027/password-strength-checker.git


Move into the project directory:

cd password-strength-checker
2. Install Python

Make sure Python 3.10 or newer is installed on your system.

Check the installed Python version:

python --version
3. Install Required Dependencies

Install the required dependencies using:

pip install -r requirements.txt

The project uses the requests library for communicating with the Have I Been Pwned Pwned Passwords API.

Tkinter is used for the graphical interface and is included with most standard Python installations.

4. Run the Application

Start the graphical application using:

python gui.py

The Password Security Analyzer window should open.

How to Use
Launch the application using python gui.py.
Enter a password into the password input field.
Click ANALYZE.
The application evaluates the password using multiple security checks.
Review the generated security score and threat rating.
Review the individual security checks.
Check the Breach Intelligence section to determine whether the password has appeared in known breach data.
Use the SHOW/HIDE button to control password visibility.
Use CLEAR to remove the current password and reset the analysis.

Important: Do not enter passwords that you currently use for important personal accounts into testing tools unless you understand how the application handles the data.

Running the Project

The main files required to run the application are:

gui.py
password_checker.py

Run the application with:

python gui.py

No web server or database is required.

Privacy and Security

The password itself is not sent directly to the Have I Been Pwned API.

The application uses the Pwned Passwords API's k-anonymity model. The password is hashed locally, and only a partial hash prefix is used for the API request.

The application is intended for educational and cybersecurity awareness purposes.

Users should avoid entering real passwords that are actively used on sensitive accounts.

API Information

This project uses the Have I Been Pwned Pwned Passwords API for breach exposure checking.

API documentation:

https://haveibeenpwned.com/API/v3#PwnedPasswords

The API is used to determine whether a password hash appears in known compromised password datasets.

Limitations

The Password Security Analyzer is an educational security tool and should not be considered a complete password security solution.

The security score is an application-defined assessment based on the implemented checks. A high score does not guarantee that a password is impossible to guess or has never been compromised.

Breach information depends on the data available through the Have I Been Pwned service.

The application does not attempt to crack passwords or perform brute-force attacks.

Future Improvements

Possible future improvements include:

Password strength estimation using entropy calculations
More advanced password pattern detection
Expanded common-password dictionaries
Improved password recommendations
More detailed breach statistics
Password generation functionality
Exporting security analysis reports
Additional cybersecurity analysis features
Improved user interface and visualization
Educational Purpose

This project was developed as a cybersecurity learning project to demonstrate concepts including:

Password security
Pattern recognition
Secure password practices
Hashing
API communication
k-anonymity
Data breach awareness
Python GUI development
Author

Yash Pathak

Cybersecurity Project

License

This project is provided for educational and cybersecurity awareness purposes.

See the LICENSE file for the applicable license terms.