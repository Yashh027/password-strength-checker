import tkinter as tk
from tkinter import messagebox

from password_checker import check_password


# ==========================================
# CHECK PASSWORD
# ==========================================

def check_password_gui():

    password = password_entry.get()

    # Don't allow an empty password
    if not password:
        messagebox.showwarning(
            "Empty Password",
            "Please enter a password first."
        )
        return

    # Run our cybersecurity engine
    result = check_password(password)

    # --------------------------------------
    # Update score and rating
    # --------------------------------------

    score_label.config(
        text=f"{result['score']} / 100"
    )

    rating_label.config(
        text=result["rating"]
    )

    # --------------------------------------
    # Update security checks
    # --------------------------------------

    update_check(
        upper_label,
        result["has_upper"],
        "Uppercase"
    )

    update_check(
        lower_label,
        result["has_lower"],
        "Lowercase"
    )

    update_check(
        digit_label,
        result["has_digit"],
        "Number"
    )

    update_check(
        special_label,
        result["has_special"],
        "Special Character"
    )

    update_check(
        repeat_label,
        not result["has_repeated"],
        "No Repeated Characters"
    )

    update_check(
        sequence_label,
        not result["has_sequence"],
        "No Sequential Pattern"
    )

    update_check(
        weak_label,
        not result["has_weakpass"],
        "Not a Weak Password"
    )

    update_check(
        keyboard_label,
        not result["has_keypattern"],
        "No Keyboard Pattern"
    )

    # --------------------------------------
    # Password length
    # --------------------------------------

    length_label.config(
        text=f"Password Length: {result['length']}"
    )

    # --------------------------------------
    # HIBP result
    # --------------------------------------

    if not result["hibp_available"]:

        breach_label.config(
            text="● Breach Check: UNKNOWN\nHIBP service unavailable"
        )

    elif result["is_compromised"]:

        breach_label.config(
            text=(
                "● Breach Check: COMPROMISED\n"
                f"Seen {result['breach_count']:,} times in breaches"
            )
        )

    else:

        breach_label.config(
            text="● Breach Check: NOT FOUND\n"
                 "Password not found in known breach data"
        )


# ==========================================
# UPDATE CHECK LABEL
# ==========================================

def update_check(label, passed, text):

    if passed:

        label.config(
            text=f"✓ {text}"
        )

    else:

        label.config(
            text=f"✗ {text}"
        )


# ==========================================
# SHOW / HIDE PASSWORD
# ==========================================

def toggle_password():

    if password_entry.cget("show") == "*":

        password_entry.config(show="")

        show_button.config(text="Hide")

    else:

        password_entry.config(show="*")

        show_button.config(text="Show")


# ==========================================
# MAIN WINDOW
# ==========================================

window = tk.Tk()

window.title("Password Security Checker")

window.geometry("700x720")

window.resizable(False, False)


# ==========================================
# TITLE
# ==========================================

title_label = tk.Label(
    window,
    text="PASSWORD SECURITY CHECKER",
    font=("Arial", 22, "bold")
)

title_label.pack(pady=(25, 5))


subtitle_label = tk.Label(
    window,
    text="Analyze password strength and breach exposure",
    font=("Arial", 11)
)

subtitle_label.pack(pady=(0, 20))


# ==========================================
# PASSWORD INPUT
# ==========================================

input_frame = tk.Frame(window)

input_frame.pack(pady=5)


password_entry = tk.Entry(
    input_frame,
    width=45,
    font=("Arial", 14),
    show="*"
)

password_entry.grid(
    row=0,
    column=0,
    padx=5
)


show_button = tk.Button(
    input_frame,
    text="Show",
    width=7,
    command=toggle_password
)

show_button.grid(
    row=0,
    column=1,
    padx=5
)


# ==========================================
# CHECK BUTTON
# ==========================================

check_button = tk.Button(
    window,
    text="CHECK PASSWORD",
    font=("Arial", 12, "bold"),
    width=25,
    command=check_password_gui
)

check_button.pack(pady=20)


# ==========================================
# SCORE SECTION
# ==========================================

score_frame = tk.Frame(
    window,
    relief="groove",
    borderwidth=2,
    padx=30,
    pady=15
)

score_frame.pack(
    padx=30,
    pady=5,
    fill="x"
)


score_title = tk.Label(
    score_frame,
    text="SECURITY SCORE",
    font=("Arial", 11, "bold")
)

score_title.pack()


score_label = tk.Label(
    score_frame,
    text="-- / 100",
    font=("Arial", 28, "bold")
)

score_label.pack()


rating_label = tk.Label(
    score_frame,
    text="Enter a password",
    font=("Arial", 14, "bold")
)

rating_label.pack(
    pady=(0, 5)
)


# ==========================================
# PASSWORD LENGTH
# ==========================================

length_label = tk.Label(
    window,
    text="Password Length: --",
    font=("Arial", 11)
)

length_label.pack(
    pady=(15, 10)
)


# ==========================================
# SECURITY CHECKS
# ==========================================

checks_frame = tk.Frame(window)

checks_frame.pack(
    padx=50,
    pady=5
)


upper_label = tk.Label(
    checks_frame,
    text="○ Uppercase",
    font=("Arial", 11),
    anchor="w",
    width=28
)

upper_label.grid(
    row=0,
    column=0,
    pady=3
)


lower_label = tk.Label(
    checks_frame,
    text="○ Lowercase",
    font=("Arial", 11),
    anchor="w",
    width=28
)

lower_label.grid(
    row=0,
    column=1,
    pady=3
)


digit_label = tk.Label(
    checks_frame,
    text="○ Number",
    font=("Arial", 11),
    anchor="w",
    width=28
)

digit_label.grid(
    row=1,
    column=0,
    pady=3
)


special_label = tk.Label(
    checks_frame,
    text="○ Special Character",
    font=("Arial", 11),
    anchor="w",
    width=28
)

special_label.grid(
    row=1,
    column=1,
    pady=3
)


repeat_label = tk.Label(
    checks_frame,
    text="○ No Repeated Characters",
    font=("Arial", 11),
    anchor="w",
    width=28
)

repeat_label.grid(
    row=2,
    column=0,
    pady=3
)


sequence_label = tk.Label(
    checks_frame,
    text="○ No Sequential Pattern",
    font=("Arial", 11),
    anchor="w",
    width=28
)

sequence_label.grid(
    row=2,
    column=1,
    pady=3
)


weak_label = tk.Label(
    checks_frame,
    text="○ Not a Weak Password",
    font=("Arial", 11),
    anchor="w",
    width=28
)

weak_label.grid(
    row=3,
    column=0,
    pady=3
)


keyboard_label = tk.Label(
    checks_frame,
    text="○ No Keyboard Pattern",
    font=("Arial", 11),
    anchor="w",
    width=28
)

keyboard_label.grid(
    row=3,
    column=1,
    pady=3
)


# ==========================================
# BREACH INFORMATION
# ==========================================

breach_label = tk.Label(
    window,
    text="● Breach Check: --",
    font=("Arial", 11, "bold"),
    justify="center"
)

breach_label.pack(
    pady=20
)


# ==========================================
# START APPLICATION
# ==========================================

window.mainloop()