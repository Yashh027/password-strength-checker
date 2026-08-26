import tkinter as tk
from tkinter import messagebox

from password_checker import check_password


# ============================================================
# CYBERSECURITY THEME
# ============================================================

BG = "#0b0f14"
PANEL = "#111820"
PANEL_LIGHT = "#17212b"
BORDER = "#263442"

TEXT = "#e6edf3"
MUTED = "#8b9aaa"

GREEN = "#39ff88"
RED = "#ff4d6d"
ORANGE = "#ffb454"
CYAN = "#36d9ff"
WHITE = "#ffffff"


# ============================================================
# MAIN WINDOW
# ============================================================

window = tk.Tk()

window.title("Password Security Analyzer")

# Smaller main window
window.geometry("1000x700")
window.minsize(850, 600)

window.configure(bg=BG)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def create_panel(parent, **kwargs):
    return tk.Frame(
        parent,
        bg=PANEL,
        highlightbackground=BORDER,
        highlightthickness=1,
        **kwargs
    )


def create_label(
    parent,
    text,
    size=10,
    color=TEXT,
    bold=False,
    **kwargs
):
    weight = "bold" if bold else "normal"

    return tk.Label(
        parent,
        text=text,
        bg=parent.cget("bg"),
        fg=color,
        font=("Consolas", size, weight),
        **kwargs
    )


# ============================================================
# SCROLLABLE MAIN AREA
# ============================================================

main_container = tk.Frame(
    window,
    bg=BG
)

main_container.pack(
    fill="both",
    expand=True
)


# Canvas
canvas = tk.Canvas(
    main_container,
    bg=BG,
    highlightthickness=0,
    borderwidth=0
)

canvas.pack(
    side="left",
    fill="both",
    expand=True
)


# Scrollbar
scrollbar = tk.Scrollbar(
    main_container,
    orient="vertical",
    command=canvas.yview,
    bg=PANEL_LIGHT,
    troughcolor=BG,
    activebackground=CYAN
)

scrollbar.pack(
    side="right",
    fill="y"
)


canvas.configure(
    yscrollcommand=scrollbar.set
)


# Frame inside canvas
content_frame = tk.Frame(
    canvas,
    bg=BG
)

canvas_window = canvas.create_window(
    (0, 0),
    window=content_frame,
    anchor="nw"
)


# ============================================================
# SCROLL CONFIGURATION
# ============================================================

def update_scroll_region(event=None):

    canvas.configure(
        scrollregion=canvas.bbox("all")
    )


def resize_content(event):

    canvas.itemconfig(
        canvas_window,
        width=event.width
    )


content_frame.bind(
    "<Configure>",
    update_scroll_region
)

canvas.bind(
    "<Configure>",
    resize_content
)


# Mouse wheel scrolling
def mouse_wheel(event):

    canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


canvas.bind_all(
    "<MouseWheel>",
    mouse_wheel
)


# Linux mouse wheel support
canvas.bind_all(
    "<Button-4>",
    lambda event: canvas.yview_scroll(-1, "units")
)

canvas.bind_all(
    "<Button-5>",
    lambda event: canvas.yview_scroll(1, "units")
)


# ============================================================
# PASSWORD ANALYSIS
# ============================================================

def check_password_gui():

    password = password_entry.get()

    if not password:

        messagebox.showwarning(
            "Input Required",
            "Please enter a password before running the security analysis."
        )

        return


    # Run cybersecurity engine
    result = check_password(password)


    # ========================================================
    # SECURITY SCORE
    # ========================================================

    score = result["score"]

    score_value.config(
        text=f"{score}/100"
    )


    # ========================================================
    # THREAT RATING
    # ========================================================

    rating = result["rating"]

    if rating == "Strong":

        rating_value.config(
            text="STRONG",
            fg=GREEN
        )

    elif rating == "Moderate":

        rating_value.config(
            text="MODERATE",
            fg=ORANGE
        )

    elif rating == "Weak":

        rating_value.config(
            text="WEAK",
            fg=ORANGE
        )

    else:

        rating_value.config(
            text="VERY WEAK",
            fg=RED
        )


    # ========================================================
    # SCORE BAR
    # ========================================================

    score_bar.delete("all")

    bar_width = 500
    bar_height = 18

    score_bar.create_rectangle(
        0,
        0,
        bar_width,
        bar_height,
        fill="#202b35",
        outline=""
    )

    fill_width = int(
        bar_width * score / 100
    )


    if score >= 80:

        bar_color = GREEN

    elif score >= 60:

        bar_color = ORANGE

    else:

        bar_color = RED


    score_bar.create_rectangle(
        0,
        0,
        fill_width,
        bar_height,
        fill=bar_color,
        outline=""
    )


    # ========================================================
    # PASSWORD LENGTH
    # ========================================================

    length_value.config(
        text=f"Length: {result['length']} characters"
    )


    # ========================================================
    # SECURITY CHECKS
    # ========================================================

    update_check(
        upper_status,
        result["has_upper"],
        "Uppercase Character",
        "Missing Uppercase Character"
    )

    update_check(
        lower_status,
        result["has_lower"],
        "Lowercase Character",
        "Missing Lowercase Character"
    )

    update_check(
        digit_status,
        result["has_digit"],
        "Number",
        "Missing Number"
    )

    update_check(
        special_status,
        result["has_special"],
        "Special Character",
        "Missing Special Character"
    )

    update_check(
        repeat_status,
        not result["has_repeated"],
        "No Repeated Characters",
        "Repeated Characters Detected"
    )

    update_check(
        sequence_status,
        not result["has_sequence"],
        "No Sequential Pattern",
        "Sequential Pattern Detected"
    )

    update_check(
        weak_status,
        not result["has_weakpass"],
        "Not a Common Password",
        "Common Password Detected"
    )

    update_check(
        keyboard_status,
        not result["has_keypattern"],
        "No Keyboard Pattern",
        "Keyboard Pattern Detected"
    )


    # ========================================================
    # BREACH INTELLIGENCE
    # ========================================================

    if not result["hibp_available"]:

        breach_status.config(
            text="● UNKNOWN",
            fg=ORANGE
        )

        breach_details.config(
            text="HIBP service unavailable."
        )

    elif result["is_compromised"]:

        breach_status.config(
            text="● COMPROMISED",
            fg=RED
        )

        breach_details.config(
            text=(
                f"Seen {result['breach_count']:,} times "
                "in known breach data."
            )
        )

    else:

        breach_status.config(
            text="● NOT FOUND",
            fg=GREEN
        )

        breach_details.config(
            text="No match found in known breach data."
        )


    # ========================================================
    # ANALYSIS SUMMARY
    # ========================================================

    reasons = []


    if result["length"] < 8:

        reasons.append(
            "Password is shorter than 8 characters."
        )


    if result["has_weakpass"]:

        reasons.append(
            "Password matches a common weak-password pattern."
        )


    if result["has_sequence"]:

        reasons.append(
            "Sequential characters were detected."
        )


    if result["has_repeated"]:

        reasons.append(
            "Repeated characters were detected."
        )


    if result["has_keypattern"]:

        reasons.append(
            "A keyboard pattern was detected."
        )


    if result["is_compromised"]:

        reasons.append(
            "This password has appeared in known data breaches."
        )


    if not reasons:

        summary_label.config(
            text=(
                "No major weaknesses detected by the "
                "current analysis rules."
            ),
            fg=GREEN
        )

    else:

        summary_label.config(
            text="\n".join(
                "• " + reason
                for reason in reasons
            ),
            fg=RED
        )


    # Automatically move to the result section
    canvas.update_idletasks()

    canvas.yview_moveto(0.15)


# ============================================================
# SECURITY CHECK LABEL UPDATE
# ============================================================

def update_check(
    label,
    passed,
    good_text,
    bad_text
):

    if passed:

        label.config(
            text=f"✓  {good_text}",
            fg=GREEN
        )

    else:

        label.config(
            text=f"✗  {bad_text}",
            fg=RED
        )


# ============================================================
# SHOW / HIDE PASSWORD
# ============================================================

def toggle_password():

    if password_entry.cget("show") == "*":

        password_entry.config(
            show=""
        )

        visibility_button.config(
            text="HIDE"
        )

    else:

        password_entry.config(
            show="*"
        )

        visibility_button.config(
            text="SHOW"
        )


# ============================================================
# CLEAR RESULTS
# ============================================================

def clear_results():

    password_entry.delete(
        0,
        tk.END
    )

    score_value.config(
        text="--/100"
    )

    rating_value.config(
        text="WAITING",
        fg=MUTED
    )

    length_value.config(
        text="Length: -- characters"
    )

    score_bar.delete(
        "all"
    )

    score_bar.create_rectangle(
        0,
        0,
        500,
        18,
        fill="#202b35",
        outline=""
    )


    for label, text in [

        (
            upper_status,
            "○  Uppercase Character"
        ),

        (
            lower_status,
            "○  Lowercase Character"
        ),

        (
            digit_status,
            "○  Number"
        ),

        (
            special_status,
            "○  Special Character"
        ),

        (
            repeat_status,
            "○  No Repeated Characters"
        ),

        (
            sequence_status,
            "○  No Sequential Pattern"
        ),

        (
            weak_status,
            "○  Not a Common Password"
        ),

        (
            keyboard_status,
            "○  No Keyboard Pattern"
        )

    ]:

        label.config(
            text=text,
            fg=MUTED
        )


    breach_status.config(
        text="● WAITING",
        fg=MUTED
    )

    breach_details.config(
        text="Run an analysis to check breach exposure."
    )


    summary_label.config(
        text="Enter a password and run the security analysis.",
        fg=MUTED
    )


    canvas.yview_moveto(0)


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(
    content_frame,
    bg=BG
)

header.pack(
    fill="x",
    padx=35,
    pady=(25, 10)
)


create_label(
    header,
    "◈  CYBERSECURITY TOOL",
    10,
    CYAN,
    True
).pack(
    anchor="w"
)


create_label(
    header,
    "PASSWORD SECURITY ANALYZER",
    24,
    WHITE,
    True
).pack(
    anchor="w",
    pady=(4, 0)
)


create_label(
    header,
    "Local password analysis  •  Pattern detection  •  Breach exposure",
    10,
    MUTED
).pack(
    anchor="w",
    pady=(4, 0)
)


# Developer credit
create_label(
    header,
    "Developed by Yash Pathak  •  Cybersecurity Project",
    9,
    CYAN
).pack(
    anchor="w",
    pady=(4, 0)
)


# ============================================================
# PASSWORD INPUT PANEL
# ============================================================

input_panel = create_panel(
    content_frame,
    padx=20,
    pady=12
)

input_panel.pack(
    fill="x",
    padx=35,
    pady=8
)


create_label(
    input_panel,
    "PASSWORD INPUT",
    10,
    CYAN,
    True
).pack(
    anchor="w"
)


input_row = tk.Frame(
    input_panel,
    bg=PANEL
)

input_row.pack(
    fill="x",
    pady=(10, 0)
)


password_entry = tk.Entry(
    input_row,
    bg="#0d141b",
    fg=WHITE,
    insertbackground=GREEN,
    relief="flat",
    font=("Consolas", 13),
    show="*"
)

password_entry.pack(
    side="left",
    fill="x",
    expand=True,
    ipady=10,
    padx=(0, 10)
)


visibility_button = tk.Button(
    input_row,
    text="SHOW",
    bg=PANEL_LIGHT,
    fg=CYAN,
    activebackground="#20303c",
    activeforeground=WHITE,
    relief="flat",
    font=("Consolas", 9, "bold"),
    width=8,
    command=toggle_password
)

visibility_button.pack(
    side="left",
    padx=(0, 8)
)


check_button = tk.Button(
    input_row,
    text="ANALYZE",
    bg="#12382a",
    fg=GREEN,
    activebackground="#19553d",
    activeforeground=WHITE,
    relief="flat",
    font=("Consolas", 10, "bold"),
    width=12,
    command=check_password_gui
)

check_button.pack(
    side="left"
)


clear_button = tk.Button(
    input_panel,
    text="CLEAR",
    bg=PANEL,
    fg=MUTED,
    activebackground=PANEL_LIGHT,
    activeforeground=WHITE,
    relief="flat",
    font=("Consolas", 8),
    command=clear_results
)

clear_button.pack(
    anchor="e",
    pady=(7, 0)
)


# ============================================================
# SECURITY SCORE PANEL
# ============================================================

score_panel = create_panel(
    content_frame,
    padx=20,
    pady=10
)

score_panel.pack(
    fill="x",
    padx=35,
    pady=8
)


score_top = tk.Frame(
    score_panel,
    bg=PANEL
)

score_top.pack(
    fill="x"
)


score_left = tk.Frame(
    score_top,
    bg=PANEL
)

score_left.pack(
    side="left"
)


create_label(
    score_left,
    "SECURITY SCORE",
    10,
    CYAN,
    True
).pack(
    anchor="w"
)


score_value = create_label(
    score_left,
    "--/100",
    28,
    WHITE,
    True
)

score_value.pack(
    anchor="w",
    pady=(3, 0)
)


score_right = tk.Frame(
    score_top,
    bg=PANEL
)

score_right.pack(
    side="right"
)


create_label(
    score_right,
    "THREAT RATING",
    9,
    MUTED,
    True
).pack(
    anchor="e"
)


rating_value = create_label(
    score_right,
    "WAITING",
    16,
    MUTED,
    True
)

rating_value.pack(
    anchor="e",
    pady=(5, 0)
)


score_bar = tk.Canvas(
    score_panel,
    width=500,
    height=18,
    bg=PANEL,
    highlightthickness=0
)

score_bar.pack(
    pady=(15, 5)
)


score_bar.create_rectangle(
    0,
    0,
    500,
    18,
    fill="#202b35",
    outline=""
)


length_value = create_label(
    score_panel,
    "Length: -- characters",
    9,
    MUTED
)

length_value.pack(
    anchor="w",
    pady=(5, 0)
)


# ============================================================
# SECURITY CHECKS PANEL
# ============================================================

checks_panel = create_panel(
    content_frame,
    padx=20,
    pady=10
)

checks_panel.pack(
    fill="x",
    padx=35,
    pady=8
)


create_label(
    checks_panel,
    "SECURITY CHECKS",
    10,
    CYAN,
    True
).pack(
    anchor="w",
    pady=(0, 10)
)


checks_grid = tk.Frame(
    checks_panel,
    bg=PANEL
)

checks_grid.pack(
    fill="x"
)


upper_status = create_label(
    checks_grid,
    "○  Uppercase Character",
    9,
    MUTED
)

upper_status.grid(
    row=0,
    column=0,
    sticky="w",
    padx=(0, 80),
    pady=3
)


lower_status = create_label(
    checks_grid,
    "○  Lowercase Character",
    9,
    MUTED
)

lower_status.grid(
    row=0,
    column=1,
    sticky="w",
    pady=3
)


digit_status = create_label(
    checks_grid,
    "○  Number",
    9,
    MUTED
)

digit_status.grid(
    row=1,
    column=0,
    sticky="w",
    padx=(0, 80),
    pady=3
)


special_status = create_label(
    checks_grid,
    "○  Special Character",
    9,
    MUTED
)

special_status.grid(
    row=1,
    column=1,
    sticky="w",
    pady=3
)


repeat_status = create_label(
    checks_grid,
    "○  No Repeated Characters",
    9,
    MUTED
)

repeat_status.grid(
    row=2,
    column=0,
    sticky="w",
    padx=(0, 80),
    pady=3
)


sequence_status = create_label(
    checks_grid,
    "○  No Sequential Pattern",
    9,
    MUTED
)

sequence_status.grid(
    row=2,
    column=1,
    sticky="w",
    pady=3
)


weak_status = create_label(
    checks_grid,
    "○  Not a Common Password",
    9,
    MUTED
)

weak_status.grid(
    row=3,
    column=0,
    sticky="w",
    padx=(0, 80),
    pady=3
)


keyboard_status = create_label(
    checks_grid,
    "○  No Keyboard Pattern",
    9,
    MUTED
)

keyboard_status.grid(
    row=3,
    column=1,
    sticky="w",
    pady=3
)


# ============================================================
# BREACH INTELLIGENCE PANEL
# ============================================================

breach_panel = create_panel(
    content_frame,
    padx=20,
    pady=12
)

breach_panel.pack(
    fill="x",
    padx=35,
    pady=8
)


create_label(
    breach_panel,
    "BREACH INTELLIGENCE",
    10,
    CYAN,
    True
).pack(
    anchor="w"
)


breach_status = create_label(
    breach_panel,
    "● WAITING",
    12,
    MUTED,
    True
)

breach_status.pack(
    anchor="w",
    pady=(8, 0)
)


breach_details = create_label(
    breach_panel,
    "Run an analysis to check breach exposure.",
    9,
    MUTED
)

breach_details.pack(
    anchor="w",
    pady=(3, 0)
)


# ============================================================
# ANALYSIS SUMMARY
# ============================================================

summary_panel = create_panel(
    content_frame,
    padx=20,
    pady=12
)

summary_panel.pack(
    fill="x",
    padx=35,
    pady=8
)


create_label(
    summary_panel,
    "ANALYSIS SUMMARY",
    10,
    CYAN,
    True
).pack(
    anchor="w"
)


summary_label = create_label(
    summary_panel,
    "Enter a password and run the security analysis.",
    9,
    MUTED,
    wraplength=800,
    justify="left"
)

summary_label.pack(
    anchor="w",
    pady=(8, 0)
)


# ============================================================
# PROJECT INFORMATION
# ============================================================

info_panel = create_panel(
    content_frame,
    padx=20,
    pady=12
)

info_panel.pack(
    fill="x",
    padx=35,
    pady=(8, 25)
)


create_label(
    info_panel,
    "PROJECT INFORMATION",
    10,
    CYAN,
    True
).pack(
    anchor="w"
)


create_label(
    info_panel,
    "Password Security Analyzer",
    10,
    WHITE,
    True
).pack(
    anchor="w",
    pady=(8, 0)
)


create_label(
    info_panel,
    "Developed by Yash Pathak",
    9,
    CYAN
).pack(
    anchor="w",
    pady=(3, 0)
)


create_label(
    info_panel,
    "Cybersecurity Project  •  Python  •  Tkinter  •  HIBP API",
    9,
    MUTED
).pack(
    anchor="w",
    pady=(3, 0)
)


# ============================================================
# START APPLICATION
# ============================================================

window.mainloop()