import hashlib

class VerificationToken:
    def __init__(self, secret: str|None = None):
        """
        secret: optional, used like HMAC so tokens can't be forged.
        """
        self.secret = secret

    def _normalize(self, text: str) -> str:
        """
        Normalize submission text to ensure stable tokens.
        - Strip leading/trailing whitespace
        - Normalize newlines
        """
        return "\n".join(line.rstrip() for line in text.strip().splitlines())

    def generate(self, submission_text: str) -> str:
        """
        Generate a verification token from raw submission text.
        """
        normalized = self._normalize(submission_text)

        if self.secret:
            normalized = self.secret + normalized

        token = hashlib.sha256(normalized.encode()).hexdigest()
        return token[:12]  # shorten for readability

    def verify(self, submission_text: str, token: str) -> bool:
        """
        Verify raw submission text against a known token.
        """
        expected = self.generate(submission_text)
        return expected == token
