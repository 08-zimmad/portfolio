from django.core.exceptions import ValidationError
from urllib.parse import urlparse

ALLOWED_DOMAINS = ["coursera.com", "udemy.com"]

def validate_safe_url(value):
    parsed = urlparse(value)

    # Only allow http/https
    if parsed.scheme not in ["http", "https"]:
        raise ValidationError("Only HTTP/HTTPS URLs are allowed.")

    # Check domain whitelist
    domain = parsed.netloc.lower()

    if not any(allowed in domain for allowed in ALLOWED_DOMAINS):
        raise ValidationError("This domain is not allowed.")

    # Block suspicious keywords
    suspicious_keywords = ["javascript:", "data:", "file:"]
    if any(keyword in value.lower() for keyword in suspicious_keywords):
        raise ValidationError("Suspicious URL detected.")