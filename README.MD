# 🔐 Password Security Analyzer

A Python-based desktop cybersecurity tool that analyzes password security using multiple local security checks and breach-exposure intelligence.

The application provides a graphical interface built with Tkinter and evaluates passwords for common weaknesses such as predictable patterns, repeated characters, sequential characters, keyboard patterns, and common-password usage. It also checks whether a password has appeared in known data breaches using the Have I Been Pwned (HIBP) Pwned Passwords API.

---

## 📌 Overview

Weak and reused passwords are one of the most common causes of account compromise.

The **Password Security Analyzer** was developed as a cybersecurity-focused desktop application to demonstrate how password security can be evaluated through a combination of:

- Local password pattern analysis
- Password complexity checks
- Common-password detection
- Predictable modification detection
- Keyboard-pattern detection
- Sequential-character detection
- Repeated-character detection
- Password length analysis
- Known breach exposure checking

The application presents the results through a dark-themed graphical user interface designed to make security findings easy to understand.

---

## ✨ Features

### 🔍 Password Complexity Analysis

The application checks whether the password contains:

- Uppercase characters
- Lowercase characters
- Numbers
- Special characters
- A recommended minimum length of 12 characters

---

### 🔁 Repeated Character Detection

The analyzer detects repeated characters occurring consecutively.

For example:

```text
Passwordaaa123!

may be flagged because of the repeated a characters.

🔢 Sequential Character Detection

The application checks for sequential character patterns.

Examples include:

abc
123
321
xyz

Sequential patterns can make passwords easier to predict.

⌨️ Keyboard Pattern Detection

The analyzer checks for commonly used keyboard sequences such as:

qwerty
asdfgh
zxcvbn
123456
1qaz2wsx
qwertyuiop
asdfghjkl
zxcvbnm
1234567890

These patterns are frequently used in weak passwords and are therefore treated as security risks.

📚 Common Password Detection

The application uses a local common_passwords.txt dataset to determine whether the entered password directly matches a known common password.

The password list is loaded locally by the application.

🔄 Predictable Password Modification Detection

The analyzer also checks whether a password appears to be a predictable variation of a common password.

For example:

password
password123
password12
123password

A password does not become significantly safer simply because a few predictable numbers or characters are added to a common password.

🌐 Breach Exposure Detection

The application uses the Have I Been Pwned Pwned Passwords API to determine whether a password has appeared in known data breaches.

The application does not send the complete password to the API.

Instead, it:

Generates a SHA-1 hash of the password locally.
Sends only the first five characters of the hash to the API.
Receives a list of matching hash suffixes.
Performs the final comparison locally.
Reports whether the password was found and how many times it has appeared.

This approach follows the API's k-anonymity model and avoids sending the complete password to the breach-checking service.

🖥️ Graphical User Interface

The application includes a custom Tkinter interface featuring:

Cybersecurity-themed dark UI
Password input field
Show/Hide password functionality
Analyze button
Clear button
Security assessment section
Password length display
Individual security checks
Breach intelligence section
Analysis summary
Project information section
Scrollable interface
🛠️ Technologies Used
Technology	Purpose
Python	Core programming language
Tkinter	Graphical user interface
Requests	Communication with the HIBP API
hashlib	Local SHA-1 password hashing
Regular expressions	Password-analysis support
pathlib	Local password-list file handling
Have I Been Pwned API	Password breach exposure checking
📂 Project Structure
password-security-analyzer/
│
├── password_checker.py
├── password_security_analyzer.py
├── common_passwords.txt
├── requirements.txt
├── README.md
├── .gitignore
│
└── screenshots/
    ├── compromised-password.png
    ├── strong-password.png
    └── pattern-detection.png
File Description
password_checker.py

Contains the core password-security analysis engine.

It performs:

Password length analysis
Character-type checks
Repeated-character detection
Sequential-pattern detection
Common-password detection
Keyboard-pattern detection
Predictable modification detection
HIBP breach checking
Security verdict generation
password_security_analyzer.py

Contains the Tkinter graphical interface.

It connects the GUI with the password-analysis engine and displays the analysis results to the user.

common_passwords.txt

Contains the local list of common passwords used by the application for password-strength analysis.

requirements.txt

Contains the external Python dependency required by the project.

README.md

Project documentation and usage information.

⚙️ Requirements

Before running the project, make sure you have:

Python 3.x
Internet connection for breach checking
requests Python package

Tkinter is included with most standard Python installations on Windows.

🚀 Installation
1. Clone the repository
git clone https://github.com/Yashh027/password-strength-checker.git
2. Open the project directory
cd password-security-analyzer
3. Install the required dependency
pip install -r requirements.txt
4. Run the application
python password_security_analyzer.py

The Password Security Analyzer window should open.

🧪 How to Use
Step 1 — Enter a password

Enter a password into the password input field.

The password is initially hidden for privacy.

Step 2 — Run the analysis

Click:

ANALYZE

The application will perform the configured local security checks and attempt a breach-exposure check.

Step 3 — Review the security assessment

The application displays an overall assessment such as:

ACTION REQUIRED
HIGH RISK PATTERN
PREDICTABLE PASSWORD
NEEDS IMPROVEMENT
NO MAJOR ISSUES
Step 4 — Review individual security checks

The Security Checks section displays the results for:

Uppercase characters
Lowercase characters
Numbers
Special characters
Repeated characters
Sequential patterns
Common passwords
Keyboard patterns
Predictable modifications

A green check indicates that the corresponding check passed.

A red cross indicates that the corresponding issue was detected.

Step 5 — Review breach intelligence

The Breach Intelligence section reports whether the password was found in known breach data.

Possible states include:

COMPROMISED
NOT FOUND
UNKNOWN

If the password is found, the application also displays the number of times it has appeared in the breach dataset returned by HIBP.

🔐 Privacy and Security

Privacy was considered during the design of the breach-checking functionality.

The application does not send the user's complete password to the HIBP Pwned Passwords API.

Instead, the password is hashed locally using SHA-1:

Password
   ↓
SHA-1 Hash
   ↓
First 5 Hash Characters → HIBP API
   ↓
Matching Hash Suffixes
   ↓
Local Comparison

The complete password remains on the user's local machine during the breach-checking process.

Important Note

Although SHA-1 is not considered suitable for modern cryptographic security applications, it is used here because the HIBP Pwned Passwords API uses SHA-1 password hashes as part of its API design.

This project is intended for password-security analysis and educational/portfolio purposes.

⚠️ Limitations

This application should not be treated as a complete password-security solution.

1. Rule-Based Analysis

The local password analysis is based on predefined rules.

It does not represent every possible password-cracking technique.

2. Breach Database Dependency

Breach results depend on the availability and data coverage of the HIBP Pwned Passwords service.

If the service is unavailable, the application reports the breach status as:

UNKNOWN

rather than incorrectly assuming that the password is safe.

3. No Absolute Security Guarantee

A password that passes all checks cannot be guaranteed to be secure.

Security depends on many factors, including:

Password reuse
Account security
Multi-factor authentication
Credential theft
Phishing
Malware
Service-specific security controls
Future password-cracking techniques
4. Common Password Dataset

The quality of local common-password detection depends on the contents of:

common_passwords.txt

Updating this dataset can improve local detection coverage.

🧠 Security Logic

The application evaluates several independent characteristics rather than relying on password length alone.

The general analysis flow is:

                ┌─────────────────────┐
                │   Password Input    │
                └──────────┬──────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │ Local Password Analysis │
              └────────────┬────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
    Complexity        Pattern Checks   Common Password
      Checks              │                Check
          │               │                │
          └───────────────┼────────────────┘
                          │
                          ▼
                ┌─────────────────────┐
                │ SHA-1 Hash Locally  │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ HIBP K-Anonymity    │
                │    Password Check   │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │ Security Assessment │
                └──────────┬──────────┘
                           │
                           ▼
                ┌─────────────────────┐
                │     GUI Results     │
                └─────────────────────┘
📊 Example Analysis

A password such as:

password123!

may trigger several findings, including:

Missing uppercase character
Sequential characters
Predictable modification
Known breach exposure

The application can therefore classify the password as requiring immediate action.

A password that passes the configured checks and is not found in the breach dataset may receive:

NO MAJOR ISSUES

This does not mean the password is guaranteed to be secure.

🧪 Testing

The application was tested using different categories of passwords, including:

Common Password
password123!

Used to test:

Common-password detection
Predictable modification detection
Sequential-pattern detection
Breach detection
Keyboard Pattern
qwerty123

Used to test keyboard-pattern detection.

Sequential Pattern
Abcdef123!

Used to test sequential-character detection.

Repeated Characters
AAAAAAAA

Used to test repeated-character detection.

Stronger Example
StrongRandom!47xQ

Used to test a password with a combination of character types and less predictable structure.

Empty Input

The application prevents analysis when no password has been entered and displays an input warning.

🎯 Project Goals

The primary goals of this project were to:

Understand practical password-security concepts
Implement password-analysis logic in Python
Work with hashing concepts
Integrate an external cybersecurity API
Understand the HIBP k-anonymity approach
Build a functional cybersecurity desktop application
Practice GUI development using Tkinter
Apply secure handling principles to password-related data
Create a practical cybersecurity project suitable for a portfolio
🔮 Future Improvements

Possible future improvements include:

Password entropy estimation
More advanced password-strength analysis
Expanded pattern detection
Larger and regularly updated password datasets
Additional keyboard-layout detection
Improved reporting and export functionality
Unit-test coverage
More detailed security recommendations
Standalone executable distribution
Improved accessibility and UI customization
📸 Screenshots
Main Interface

Add a screenshot of the application's main interface here.

screenshots/Password Security.png

🧑‍💻 Author

Yash Pathak

Cybersecurity Project
Built with:

Python
Tkinter
Requests
HIBP Pwned Passwords API
📄 License

This project is intended for educational, learning, and portfolio purposes.

You are free to study and modify the source code for your own learning and development.

⚠️ Disclaimer

This project is designed for defensive cybersecurity education and password-security awareness.

Do not use it to process passwords belonging to other people without their permission.

Never enter passwords that you actively use for important accounts into third-party password-analysis tools unless you understand how the tool handles the data.

For real-world account security, use a reputable password manager, unique passwords, and multi-factor authentication whenever available.

⭐ Project Summary

Password Security Analyzer is a Python/Tkinter cybersecurity application that combines local password analysis with privacy-conscious breach exposure checking.

The project demonstrates practical implementation of:

Python
│
├── Password Security Analysis
├── Pattern Detection
├── SHA-1 Hashing
├── HIBP API Integration
├── K-Anonymity Concept
├── GUI Development
├── Input Validation
└── Security-Oriented Programming

The goal is not simply to determine whether a password is "strong" or "weak", but to provide users with a clearer understanding of the specific characteristics that may make a password vulnerable.


### `requirements.txt`

Create a file named **exactly**:

```text
requirements.txt

and put only this inside:

requests