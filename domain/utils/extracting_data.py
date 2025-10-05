import re
from domain.utils.discord_extractor import DiscordExtractor
from domain.utils.url_extractor import URLExtractor

class ExtractingData:
    def __init__(self, bot):
        self.bot = bot

    async def extract_content(self, input_text, ctx):
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, input_text)

        discordExtractor = DiscordExtractor(self.bot)
        urlExtractor = URLExtractor()

        # Case 1: input_text is exactly a URL
        if urls and input_text.strip() == urls[0]:
            url = urls[0]

            if discordExtractor.is_discord_link(url):
                content, error = await discordExtractor.fetch_discord_message(url)
                if content:
                    return content, 'discord_message', url, None
                else:
                    return None, 'error', url, error

            elif urlExtractor.is_supported_url(url):
                content, error = urlExtractor.extract_text_from_url(url)
                if content:
                    return content, 'url', url, None
                else:
                    return None, 'error', url, error or "Could not extract content"

            else:
                return None, 'error', url, f"Unsupported URL domain: {url}"

        # Case 2: input_text contains URL(s) but is mostly text
        elif urls:
            # You might choose to keep URLs in the text or remove them
            return [str(input_text)], 'text_with_url', str(input_text), None

        # Case 3: plain text without URLs
        return [str(input_text)], 'text', str(input_text), None