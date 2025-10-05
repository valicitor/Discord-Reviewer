from domain import VerificationToken, ExtractingData
from config import VERIFICATION_SECRET


class VerifyContentQuery:

    def __init__(self, bot):
        self.bot = bot
        return

    async def execute(self, ctx, hash, submission) -> bool:
        # Extract content from the submission if it contains a URL
        extractor = ExtractingData(self.bot)
        list_content, source, url, error = await extractor.extract_content(
            submission, ctx)

        if error:
            return False

        content = ""
        if list_content:
            content = str(list_content[0] or "")

        return VerificationToken(VERIFICATION_SECRET).verify(content, hash)
