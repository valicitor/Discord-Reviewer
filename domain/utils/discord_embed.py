import discord
from datetime import datetime
from config import BOT_VERSION
import math

class DiscordEmbed:
    @staticmethod
    def approved_embed(ctx) -> discord.Embed:
        embed = discord.Embed(
            title="✅ Stamp of Approval",
            description=f"### 🎉 You are officially **APPROVED**!\n\nYour submission has been reviewed and given the thumbs up by **{ctx.author.name}**.",
            color=0x32CD32  # bright green
        )
        embed.set_footer(text="Keep up the great work!")
        embed.timestamp = ctx.message.created_at

        return embed

    @staticmethod
    def denied_embed(ctx) -> discord.Embed:
        embed = discord.Embed(
            title="🚫 Stamp of Denial",
            description=(
                f"### 🚫 Unfortunately, your submission has been **DENIED**.\n\nReviewed and rejected by **{ctx.author.name}**."
            ),
            color=0xFF0000  # bright red
        )
        embed.set_footer(text="Better luck next time!")
        embed.timestamp = ctx.message.created_at
        return embed

    @staticmethod
    def real_teapot_embed(ctx) -> discord.Embed:
        embed = discord.Embed(
            title="🍵 Official British Stamp of Tea",
            description=(
                f"### 🫖 Certified by the **Royal Order of Teapots**\n\n"
                f"This submission has been steeped, brewed, and taste-tested by **{ctx.author.name}**.\n"
                f"☑️ Approved for maximum Britishness!"
            ),
            color=0x8B4513  # a nice tea-brown
        )
        embed.set_footer(text="Keep calm and sip on ☕")
        embed.timestamp = ctx.message.created_at
        return embed

    @staticmethod
    def fatherkoko_embed(ctx) -> discord.Embed:
        embed = discord.Embed(
            title="🕯️ The Seal of Father Koko",
            description=(
                f"### 🌑 From the shadows emerges a verdict...\n\n"
                f"With solemn artistry, **{ctx.author.name}** has cast their judgment.\n"
                f"⚖️ Your work now carries the weight of the midnight seal."
            ),
            color=0x2C003E  # deep violet-black for dramatic flair
        )
        embed.set_footer(text="The candle burns... but the night is eternal.")
        embed.timestamp = ctx.message.created_at
        return embed

    @staticmethod
    def starlight_embed(ctx) -> discord.Embed:
        embed = discord.Embed(
            title="🌟✨ Idol Seal of Starlight ✨🌟",
            description=(
                f"### 💖 Approved with Idol Energy!\n\n"
                f"Like a shining vtuber on stage, **{ctx.author.name}** "
                f"has bestowed their dazzling approval upon you!\n\n"
                f"🎤 May your journey be full of sparkle, hype, and critical hits!"
            ),
            color=0xFFD700  # golden idol glow
        )
        embed.set_footer(text="✨ Shine bright, like a starlight idol ✨")
        embed.timestamp = ctx.message.created_at
        return embed
    
    @staticmethod
    def prefix_changed_embed(ctx, new_prefix: str, admin: discord.Member) -> discord.Embed:
        return discord.Embed(
            title="🔧 Prefix Changed",
            description=f"The command prefix has been updated by **{ctx.author.name}**.",
            color=discord.Color.gold()
        ).add_field(
            name="New Prefix",
            value=f"`{new_prefix}`",
            inline=True
        )

    @staticmethod
    def submission_verified_embed(ctx, is_verified: bool) -> discord.Embed:
        if is_verified:
            return discord.Embed(
                title="✅ Submission Verified",
                description=f"{ctx.author.display_name} has verified the content of the submission.",
                color=discord.Color.green()
            )
        else:
            return discord.Embed(
                title="⚠️ Submission Changed",
                description=f"The verification token did not match, there are likely changes to submission.",
                color=discord.Color.orange()
            )
    
    @staticmethod
    def review_character_embed(ctx, source_type, results):
        embed = discord.Embed(
            title=f"📋 Character Review Summary",
            color=discord.Color.blue() if not results['requires_review'] else discord.Color.orange(),
            timestamp=datetime.now()
        )

        # Header information
        source_display = {
            'text': 'Direct Text',
            'url': 'External URL',
            'discord_message': 'Discord Message'
        }

        embed.add_field(
            name="🔗 Source", 
            value=source_display.get(source_type, 'Unknown'), 
            inline=True
        )

        embed.add_field(
            name="📝 Submitted by", 
            value=ctx.author.display_name, 
            inline=True
        )

        embed.add_field(
            name="🕒 Submitted on", 
            value=datetime.now().strftime("%Y-%m-%d"), 
            inline=True
        )

        character_name = results.get("character_name", [])
        if character_name:
            first_character_name = str(character_name[0]).strip()
            embed.add_field(
                name="⚡ Character Name",
                value=first_character_name,
                inline=True
            )
            
        race = results.get("race", [])
        if race:
            first_race = str(race[0]).strip()
            embed.add_field(
                name="⚡ Race",
                value=first_race,
                inline=True
            )

        race_type = results.get("race_type", [])
        if race_type:
            first_race_type = str(race_type[0]).strip()
            embed.add_field(
                name="⚡ Race Type",
                value=first_race_type,
                inline=True
            )

        age = results.get("age", [])
        if age:
            first_age = str(age[0]).strip()
            embed.add_field(
                name="⚡ Age",
                value=first_age,
                inline=True
            )

        gender = results.get("gender", [])
        if gender:
            first_gender = str(gender[0]).strip()
            embed.add_field(
                name="⚡ Gender",
                value=first_gender,
                inline=True
            )

        ki = results.get("ki", [])
        if ki:
            first_ki = str(ki[0]).strip()
            embed.add_field(
                name="⚡ Ki Type",
                value=first_ki,
                inline=True
            )

        startingpl = results.get("startingpl", [])
        if startingpl:
            first_startingpl = str(startingpl[0]).strip()
            embed.add_field(
                name="⚡ Starting PL",
                value=first_startingpl,
                inline=True
            )

        # Summary section
        if 'summary' in results and results['summary']:
            summary = results['summary']
            if len(summary) > 500:
                summary = summary[:497] + "..."
            embed.add_field(
                name="📝 Character Summary",
                value=summary,
                inline=False
            )
        
        # Physcial section
        if 'physcial' in results and results['physcial']:
            physcial = results['physcial']
            if len(physcial) > 500:
                physcial = physcial[:497] + "..."
            embed.add_field(
                name="📝 Physcial Description",
                value=physcial,
                inline=False
            )
        
        # Personality section
        if 'personality' in results and results['personality']:
            personality = results['personality']
            if len(personality) > 500:
                personality = personality[:497] + "..."
            embed.add_field(
                name="📝 Perceived Personality",
                value=personality,
                inline=False
            )
        
        # Backstory section
        if 'backstory' in results and results['backstory']:
            backstory = results['backstory']
            if len(backstory) > 500:
                backstory = backstory[:497] + "..."
            embed.add_field(
                name="📝 Backstory",
                value=backstory,
                inline=False
            )

        # Bullet points field
        if results.get('bullet_points'):
            bullets_text = "\n".join(f"• {bp}" for bp in results['bullet_points'])
            embed.add_field(
                name="📌 Characater Notes",
                value=bullets_text,
                inline=False
            )

        # Admin Insights section
        if results.get('admin_insights'):
            insights_text = "\n".join(results['admin_insights'])
            embed.add_field(
                name="⚠️ Requires Admin Review",
                value=f"{insights_text}",
                inline=False
            )
        else:
            embed.add_field(
                name="✅ No Immediate Concerns",
                value="This submission does not have any flagged issues.",
                inline=False
            )

        embed.set_footer(text=f"Verification Token: {results.get('verification_token', 'N/A')}")

        return embed

    @staticmethod
    def review_item_embed(ctx, source_type, results):
        embed = discord.Embed(
            title=f"📋 Item Review Summary",
            color=discord.Color.blue() if not results['requires_review'] else discord.Color.orange(),
            timestamp=datetime.now()
        )

        # Header information
        source_display = {
            'text': 'Direct Text',
            'url': 'External URL',
            'discord_message': 'Discord Message'
        }

        embed.add_field(
            name="🔗 Source", 
            value=source_display.get(source_type, 'Unknown'), 
            inline=True
        )

        embed.add_field(
            name="📝 Submitted by", 
            value=ctx.author.display_name, 
            inline=True
        )

        embed.add_field(
            name="🕒 Submitted on", 
            value=datetime.now().strftime("%Y-%m-%d"), 
            inline=True
        )

        item_name = results.get("item_name", [])
        if item_name:
            first_item_name = str(item_name[0]).strip()
            embed.add_field(
                name="⚡ Item Name",
                value=first_item_name,
                inline=True
            )

        type = results.get("type", [])
        if type:
            first_type = str(type[0]).strip()
            embed.add_field(
                name="⚡ Type",
                value=first_type,
                inline=True
            )

        rank = results.get("rank", [])
        if rank:
            first_rank = str(rank[0]).strip()
            embed.add_field(
                name="⚡ Rank",
                value=first_rank,
                inline=True
            )

        assistant = results.get("assistant", [])
        if assistant:
            first_assistant = str(assistant[0]).strip()
            embed.add_field(
                name="⚡ Assistant(s)",
                value=first_assistant,
                inline=True
            )

        cooldown = results.get("cooldown", [])
        if cooldown:
            first_cooldown = str(cooldown[0]).strip()
            embed.add_field(
                name="⚡ Cooldown",
                value=first_cooldown,
                inline=True
            )

        ki = results.get("ki", [])
        if ki:
            first_ki = str(ki[0]).strip()
            embed.add_field(
                name="⚡ Ki Type",
                value=first_ki,
                inline=True
            )

        artificialpl = results.get("artificialpl", [])
        if artificialpl:
            first_artificialpl = str(artificialpl[0]).strip()
            embed.add_field(
                name="⚡ Artificial PL",
                value=first_artificialpl,
                inline=True
            )

        # Summary section
        if 'summary' in results and results['summary']:
            summary = results['summary']
            if len(summary) > 500:
                summary = summary[:497] + "..."
            embed.add_field(
                name="📝 Item Summary",
                value=summary,
                inline=False
            )
        
        if 'effects' in results and results['effects']:
            effects = results['effects']
            if len(effects) > 500:
                effects = effects[:497] + "..."
            embed.add_field(
                name="📝 Item Effects",
                value=effects,
                inline=False
            )

        # Bullet points field
        if results.get('bullet_points'):
            bullets_text = "\n".join(f"• {bp}" for bp in results['bullet_points'])
            embed.add_field(
                name="📌 Item Notes",
                value=bullets_text,
                inline=False
            )

        # Admin Insights section
        if results.get('admin_insights'):
            insights_text = "\n".join(results['admin_insights'])
            embed.add_field(
                name="⚠️ Requires Admin Review",
                value=f"{insights_text}",
                inline=False
            )
        else:
            embed.add_field(
                name="✅ No Immediate Concerns",
                value="This submission does not have any flagged issues.",
                inline=False
            )

        embed.set_footer(text=f"Verification Token: {results.get('verification_token', 'N/A')}")
        
        return embed
        
    @staticmethod
    def review_ability_embed(ctx, source_type, author, results):
        embed = discord.Embed(
            title=f"📋 Ability Review Summary",
            color=discord.Color.blue() if not results['requires_review'] else discord.Color.orange(),
            timestamp=datetime.now()
        )

        # Header information
        source_display = {
            'text': 'Direct Text',
            'url': 'External URL',
            'discord_message': 'Discord Message'
        }

        embed.add_field(
            name="🔗 Source", 
            value=source_display.get(source_type, 'Unknown'), 
            inline=True
        )

        embed.add_field(
            name="📝 Submitted by", 
            value=author if author else "Unknown", 
            inline=True
        )

        embed.add_field(
            name="🕒 Submitted on", 
            value=datetime.now().strftime("%Y-%m-%d"), 
            inline=True
        )

        ability_name = results.get("ability_name", [])
        if ability_name:
            first_ability_name = str(ability_name[0]).strip()
            embed.add_field(
                name="⚡ Ability Name",
                value=first_ability_name,
                inline=True
            )

        ability_type = results.get("ability_type", [])
        if ability_type:
            first_ability_type = str(ability_type[0]).strip()
            embed.add_field(
                name="⚡ Ability Type",
                value=first_ability_type,
                inline=True
            )

        ability_rank = results.get("rank", [])
        if ability_rank:
            first_ability_rank = str(ability_rank[0]).strip()
            embed.add_field(
                name="⚡ Ability Rank",
                value=first_ability_rank,
                inline=True
            )

        ability_multiplier = results.get("multiplier", [])
        if ability_multiplier:
            first_ability_multiplier = str(ability_multiplier[0]).strip()
            embed.add_field(
                name="⚡ Multiplier",
                value=first_ability_multiplier,
                inline=True
            )

        ability_cooldown = results.get("cooldown", [])
        if ability_cooldown:
            first_ability_cooldown = str(ability_cooldown[0]).strip()
            embed.add_field(
                name="⚡ Cooldown",
                value=first_ability_cooldown,
                inline=True
            )

        if results.get('top_categories'):
            max_blocks = 10  # Maximum number of blocks for the bar
            top_score = max(score for _, score in results['top_categories'])

            category_lines = []
            for name, score in results['top_categories']:
                bar_length = int((score / top_score) * max_blocks) if top_score > 0 else 0
                bar = "▇" * bar_length
                percent = score
                category_lines.append(f"{name:12} {bar} ({percent:.1f}%)")

            # Wrap in triple backticks for monospace formatting
            category_text = "```\n" + "\n".join(category_lines) + "\n```"

            embed.add_field(
                name="⚡ Category Assignment",
                value=category_text,
                inline=False
            )

        # Summary section
        if 'summary' in results and results['summary']:
            summary = results['summary']
            if len(summary) > 500:
                summary = summary[:497] + "..."
            embed.add_field(
                name="📝 Ability Summary",
                value=summary,
                inline=False
            )

        # Bullet points field
        if results.get('bullet_points'):
            bullets_text = "\n".join(f"• {bp}" for bp in results['bullet_points'])
            embed.add_field(
                name="📌 Key Mechanics / Notes",
                value=bullets_text,
                inline=False
            )

        # Power Analysis section
        if results.get('power_scores'):
            max_blocks = 10  # Max bar length
            # power_scores is expected to be a list of tuples: (axis_name, score 0-10)
            power_lines = []
            for axis, score in results['power_scores']:
                bar_length = int((score / 10) * max_blocks)  # normalize 0-10 to bar
                bar = "▇" * bar_length
                percent = score * 10  # convert 0-10 scale to percentage
                power_lines.append(f"{axis:12} {bar:<10} ({percent:.0f}%)")

            power_text = "```\n" + "\n".join(power_lines) + "\n```"

            embed.add_field(
                name="⚡ Power Analysis",
                value=power_text,
                inline=False
            )

        # Admin Insights section
        if results.get('admin_insights'):
            insights_text = "\n".join(results['admin_insights'])
            embed.add_field(
                name="⚠️ Requires Admin Review",
                value=f"{insights_text}",
                inline=False
            )
        else:
            embed.add_field(
                name="✅ No Immediate Concerns",
                value="This submission does not have any flagged issues.",
                inline=False
            )

        embed.set_footer(text=f"Verification Token: {results.get('verification_token', 'N/A')}")
        
        return embed

    @staticmethod
    def review_training_log_embed(ctx, source_type, results):
        embed = discord.Embed(
            title="Training Log Review",
            color=discord.Color.red() if results['total_correct'] < results['total_entries'] else discord.Color.green()
        )

        total_correct = results.get("total_correct", 0)
        total_entries = results.get("total_entries", 0)
        bad_entries = results.get("bad_entries", [])

        # Overall correctness
        embed.add_field(
            name="Correctness",
            value=f"{total_correct}/{total_entries} entries correct",
            inline=False
        )

        if bad_entries:
            for e in bad_entries:
                old_val = e.get("old_power_level", "?") or "?"
                gain_val = e.get("training_gains", "?") or "?"
                new_val = e.get("new_power_level", "?") or "?"
                expected_val = e.get("expected_new_power_level", "?") or "?"
                disparity = abs(new_val - expected_val) if isinstance(new_val, int) and isinstance(expected_val, int) else "?"
                error_type = e.get("errortype") or "Unknown"
                unclassified = "; ".join(e.get("unclassified", []))

                # Build field for each incorrect entry
                field_name = f"❌ {error_type} - {e.get('charactername', 'Unknown')}"
                field_value = ""

                # If gains exist, add as a separate sub-field line
                if gain_val and gain_val != "?":
                    gain_snippet = gain_val
                    if len(gain_snippet) > 100:
                        gain_snippet = gain_snippet[:97] + "..."
                    field_value += f"Gains: {gain_snippet}"

                # Break out gains into its own line
                field_value += "```"
                field_value += f"{'Old PL':>8} {'Expected':>8} {'Actual':>8} {'Dis':>8}\n"
                field_value += "-" * 36 + "\n"
                field_value += f"{old_val:>8} {expected_val:>8} {new_val:>8} {disparity:>8}\n"
                field_value += "```"

                # Optional additional info
                if unclassified:
                    snippet = unclassified
                    if len(snippet) > 100:
                        snippet = snippet[:97] + "..."
                    field_value += f"\nAdditional info: {snippet}"
                    
                embed.add_field(name=field_name, value=field_value, inline=False)
        else:
            embed.add_field(name="Bad Entries", value="None 🎉", inline=False)

        return embed

    @staticmethod
    def create_category_embed(category: dict | None) -> discord.Embed:
        """Embed shown when a category is created"""
        if category is None:
            return discord.Embed(
                title="❌ Category Creation Failed",
                description="The category could not be created.",
                color=discord.Color.red()
            )

        embed = discord.Embed(
            title=f"✅ Category Created: {category['tier_name']}",
            color=discord.Color.blue()
        )
        embed.add_field(name="Priority", value=category['priority'], inline=True)
        embed.add_field(name="Prompt", value=category['prompt'], inline=False)
        return embed

    @staticmethod
    def delete_category_embed(category: dict | None) -> discord.Embed:
        """Embed shown when a single category is deleted"""
        if category is None:
            return discord.Embed(
                title="❌ Category Deletion Failed",
                description="The category could not be found.",
                color=discord.Color.red()
            )

        embed = discord.Embed(
            title=f"🗑️ Category Deleted: {category['tier_name']}",
            color=discord.Color.blue()
        )
        embed.add_field(name="Priority", value=category['priority'], inline=True)
        return embed

    @staticmethod
    def delete_all_categories_embed(deleted_count: int) -> discord.Embed:
        """Embed shown when all categories for a guild are deleted"""
        if deleted_count == 0:
            return discord.Embed(
                title="❌ No Categories Found",
                description=f"No categories were found.",
                color=discord.Color.red()
            )

        embed = discord.Embed(
            title=f"🗑️ All Categories Deleted",
            description=f"Deleted {deleted_count} categories.",
            color=discord.Color.blue()
        )
        return embed
        
    @staticmethod
    def view_category_embed(category: dict | None) -> discord.Embed:
        """Create an embed for a single category, or a message if category is None"""
        if category is None:
            return discord.Embed(
                title="❌ Category Not Found",
                description="The requested category does not exist.",
                color=discord.Color.red()
            )

        embed = discord.Embed(
            title=f"📊 Category: {category['tier_name']}",
            color=discord.Color.blue()
        )
        embed.add_field(name="Priority", value=category['priority'], inline=True)
        embed.add_field(name="Full Prompt", value=category['prompt'], inline=False)
        embed.add_field(
            name="💡 Usage",
            value="This prompt is used to evaluate abilities and assign them to this tier based on similarity scoring.",
            inline=False
        )
        return embed

    @staticmethod
    def view_all_categories_embed(categories: list[dict]) -> discord.Embed:
        embed = discord.Embed(
            title="📋 All Categories",
            description="Here are the currently defined categories:",
            color=discord.Color.blue()
        )

        if not categories:
            embed.description = "No categories available."
            return embed

        for category in categories:
            prompt_preview = category['prompt']
            if len(prompt_preview) > 100:
                prompt_preview = prompt_preview[:97] + "..."

            embed.add_field(
                name=f"📊 {category['tier_name']} (Priority: {category['priority']})",
                value=prompt_preview,
                inline=False
            )

        return embed

    @staticmethod
    def command_not_found(command_name: str) -> discord.Embed:
        return discord.Embed(
            title="❌ Command Not Found",
            description=f"Command `{command_name}` not found. Use `!help` to see all commands.",
            color=discord.Color.red()
        )

    @staticmethod
    def help_embed(prefix: str) -> discord.Embed:
        embed = discord.Embed(
            title=f"🤖 Review Bot v{BOT_VERSION} - Help Menu",
            description="Advanced submission review system with category-based evaluation",
            color=discord.Color.blue()
        )
    
        # Admin Commands
        embed.add_field(
            name="📝 Admin Commands",
            value=f"""`{prefix}set_prefix <new_prefix>` - Change the bot's current prefix
    `{prefix}verify_content <verification_token> <text_or_link>` - Verify the content of a submission
    `{prefix}approved` - Approve a submission with a stamp of approval
    `{prefix}denied` - Deny a submission with a stamp of denial
    `{prefix}real_teapot` - Approve a submission with the Official British Stamp of Tea
    `{prefix}father_koko` - Approve a submission with the Seal of Father Koko
    `{prefix}star_light` - Approve a submission with the Idol Seal of Starlight""",
            inline=False
        )

        # Review Commands
        embed.add_field(
            name="📝 Review Commands",
            value=f"""`{prefix}review_ability <text_or_link>` - Review an ability (with tier grading)
    `{prefix}review_item <text_or_link>` - Review an item (with rarity/power analysis)
    `{prefix}review_character <text_or_link>` - Review a character""",
            inline=False
        )
    
        # Tier Management Commands
        embed.add_field(
            name="📊 Category Management",
            value=f"""`{prefix}view_all_categories` - View all custom tiers
    `{prefix}view_category <name>` - View details of a specific tier
    `{prefix}create_category <name> <priority> <prompt>` - Create new tier
    `{prefix}delete_category <name>` - Delete a tier
    `{prefix}delete_all_categories` - Delete all custom tiers""",
            inline=False
        )
    
        embed.set_footer(text=f"Use {prefix}help <command> for detailed command information")
    
        return embed

    @staticmethod
    def command_help(command, prefix: str):
        embed = discord.Embed(
            title=f"ℹ️ Command: {prefix}{command.name}",
            description=command.help or "No description available",
            color=discord.Color.blue()
        )
    
        # Add aliases if they exist
        if command.aliases:
            embed.add_field(name="Aliases", value=", ".join([f"`!{alias}`" for alias in command.aliases]), inline=True)

        c_examples = {
            'set_prefix': f'`{prefix}set_prefix !`',
            'verify_content': f'`{prefix}verify_content "abc123" "A powerful fireball ability"`',
            'approved': f'`{prefix}approved`',
            'denied': f'`{prefix}denied`',
            'real_teapot': f'`{prefix}real_teapot`',
            'father_koko': f'`{prefix}father_koko`',
            'star_light': f'`{prefix}star_light`',
            'review_ability': f'`{prefix}review_ability A fireball that deals 2x damage and ignites enemies`\n`!review_ability https://pastebin.com/example`',
            'review_item': f'`{prefix}review_item Sword of Flames. Deals damage and has a chance to burn`\n`!review_item https://docs.google.com/document/example`',
            'review_character': f'`{prefix}review_character A rogue with stealth abilities and backstab damage`',
            'view_all_categories': f'`{prefix}view_all_categories`',
            'view_category': f'`{prefix}view_category S-Rank`\n`!view_tier Common`',
            'create_category': f'`{prefix}create_category "S-Rank" 10 "Abilities that can affect reality or have universal scale"`',
            'delete_category': f'`{prefix}delete_category Old-Tier`',
            'delete_all_categories': f'`{prefix}delete_all_categories`',
        }
    
        # Add usage examples based on command
        examples = c_examples.get(command.name, "No examples available")
        if examples:
            embed.add_field(name="Examples", value=examples, inline=False)
    
        # Add permissions info if applicable
        if any(hasattr(check, '__name__') and 'has_permissions' in check.__name__ for check in command.checks):
            embed.add_field(name="Permissions", value="Administrator only", inline=True)
    
        return embed

    @staticmethod
    def command_faq(prefix: str):
        embed = discord.Embed(
            title=f"🤖 Review Bot v{BOT_VERSION} - FAQs",
            description="Common questions about the bot",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="❓ How do I change the command prefix?",
            value=f"Use the `{prefix}set_prefix <new_prefix>` command. Example: `{prefix}set_prefix !`",
            inline=False
        )

        embed.add_field(
            name="❓ How do I verify a submission?",
            value=f"Use the `{prefix}verify_content <verification_token> <text_or_link>` command. Example: `{prefix}verify_content \"abc123\" \"A powerful fireball ability\"`",
            inline=False
        )

        embed.add_field(
            name="❓ How do I review an ability?",
            value=f"Use the `{prefix}review_ability <text_or_link>` command. Example: `{prefix}review_ability A fireball that deals 2x damage and ignites enemies` or `{prefix}review_ability https://pastebin.com/example`",
            inline=False
        )

        embed.add_field(
            name="❓ How do I create a new category?",
            value=f"Use the `{prefix}create_category <name> <priority> <prompt>` command. Example: `{prefix}create_category \"S-Rank\" 10 \"Abilities that can affect reality or have universal scale\"`",
            inline=False
        )

        embed.add_field(
            name="❓ What is priority in Category?",
            value=f"Priority determines the order in which categories are evaluated. Higher priority categories are checked first.",
            inline=False
        )

        embed.add_field(
            name="❓ How do I view all categories?",
            value=f"Use the `{prefix}view_all_categories` command.",
            inline=False
        )

        embed.set_footer(text=f"Use {prefix}help <command> for detailed command information")
    
        return embed