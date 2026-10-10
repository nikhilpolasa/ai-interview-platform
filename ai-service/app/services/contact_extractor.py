import re


EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

URL_PATTERN = re.compile(
    r"(?:https?://)?(?:www\.)?"
    r"(?:linkedin\.com/[^\s]+|github\.com/[^\s]+)"
)


def extract_contact_information(text: str) -> dict:
    email_match = EMAIL_PATTERN.search(text)

    urls = URL_PATTERN.findall(text)

    return {
        "email": email_match.group(0) if email_match else None,
        "links": urls
    }