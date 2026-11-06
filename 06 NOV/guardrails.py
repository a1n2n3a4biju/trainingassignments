import re

def validate_input(question):
    if not question or not question.strip():
        return False, "Please enter a question."

    if len(question) > 500:
        return False, "Your question is too long. Please keep it under 500 characters."

    return True, ""


def is_restaurant_related(question, has_history=False):

    question = question.lower().strip()

    keywords = [
        "restaurant", "food", "cuisine", "dining",
        "menu", "price", "cost", "guest", "people",
        "reservation", "seat", "available",
        "indian", "italian", "chinese", "mexican",
        "spice garden"
    ]

    if has_history:
        if question in ["yes", "no", "ok", "okay"]:
            return True

        if question.isdigit() or "people" in question or "guests" in question:
            return True

    for word in keywords:
        if word in question:
            return True

    return False

def contains_pii(text):
    email = r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b"
    phone = r"\b[6-9]\d{9}\b"

    return bool(
        re.search(email, text)
        or re.search(phone, text)
    )

def clean_output(answer):

    answer = re.sub(
        r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b",
        "[EMAIL REDACTED]",
        answer
    )

    answer = re.sub(
        r"\b[6-9]\d{9}\b",
        "[PHONE REDACTED]",
        answer
    )

    return answer
