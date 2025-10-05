import re
import aiohttp
import discord
from urllib.parse import urlparse

class DiscordExtractor:
    def __init__(self, bot):
        self.bot = bot

    def is_discord_link(self, url):
        try:
            parsed = urlparse(url)
            return 'discord.com' in parsed.netloc and '/channels/' in url
        except Exception as e:
            return False

    def extract_discord_ids(self, url):
        try:
            pattern = r'discord\.com/channels/(\d+)/(\d+)(?:/(\d+))?'
            match = re.search(pattern, url)
            if match:
                guild_id = int(match.group(1))
                channel_id = int(match.group(2))
                message_id = int(match.group(3)) if match.group(3) else None
                return guild_id, channel_id, message_id
            return None
        except Exception as e:
            return None

    async def fetch_discord_message(self, url) -> tuple[list[str]|None, str|None]:
        ids = self.extract_discord_ids(url)
        if not ids:
            return None, "Invalid Discord link format"

        guild_id, channel_id, message_id = ids
        guild = self.bot.get_guild(guild_id)
        if not guild:
            return None, "Guild not found or bot doesn't have access"

        channel = guild.get_channel(channel_id) or guild.get_channel_or_thread(channel_id)

        if not channel:
            return None, f"Channel {channel_id} not found or bot doesn't have access. "

        if not channel.permissions_for(guild.me).read_messages:
            return None, "Bot doesn't have permission to read this channel"

        # CASE 1: Single message link
        if message_id:
            try:
                message = await channel.fetch_message(message_id)
                content = await self._process_message(message)
                return [content], None
            except discord.NotFound:
                return None, "Message not found"
            except discord.Forbidden:
                return None, "Bot doesn't have permission to access this message"
            except Exception as e:
                return None, f"Error fetching message: {str(e)}"

        # CASE 2: Channel/forum link
        try:
            if isinstance(channel, discord.ForumChannel):
                results = []

                # Active threads (cached list)
                active_threads = list(channel.threads)

                # Archived threads (async iterator)
                archived_threads = []
                async for thread in channel.archived_threads(limit=5):  # small limit for debugging
                    archived_threads.append(thread)

                threads = active_threads + archived_threads

                for thread in threads:
                    async for msg in thread.history(limit=5):  # small limit for debugging
                        processed = await self._process_message(msg)
                        results.append(processed)

                return results, None

            else:
                results = []
                async for msg in channel.history(limit=10):  # small limit for debugging
                    processed = await self._process_message(msg)
                    results.append(processed)

                return results, None

        except Exception as e:
            return None, f"Error fetching channel/thread: {str(e)}"

    async def _process_message(self, message: discord.Message):
        content = message.content or ""

        # Attachments
        for attachment in message.attachments:
            if attachment.filename.endswith(('.txt', '.md')):
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(attachment.url) as resp:
                            if resp.status == 200:
                                attachment_content = await resp.text()
                                content += f"\n\n[Attachment: {attachment.filename}]\n{attachment_content}"
                except Exception as e:
                    pass

        # Embeds
        for embed in message.embeds:
            if embed.description:
                content += f"\n\n[Embed Description]\n{embed.description}"
            if embed.fields:
                for field in embed.fields:
                    content += f"\n\n[{field.name}]\n{field.value}"

        return content
