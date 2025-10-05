import re

class AdminAbilityInsights:

    def __init__(self):
        pass

    def generate(self, results) -> tuple[bool, list[str]]:
        requires_review = False
        insights = []

        # Summary
        summary = results.get("summary", "").strip()
        if not summary:
            insights.append("- Missing summary")
            requires_review = True
        else:
            # Heuristic: warn if summary is very short
            if len(summary) < 100:  # fewer than 100 characters
                insights.append("- Summary is very short; may lack detail")
                requires_review = True
            # Optional: warn if fewer than 4 sentences
            elif summary.count('.') < 4:
                insights.append(
                    "- Summary may be too brief or not descriptive")
                requires_review = True

        # Power score analysis
        power_scores = results.get("power_scores", [])
        if power_scores:
            scores = [s for _, s in power_scores]

            high_threshold = 8  # example threshold for “very high”
            low_threshold = 2  # example threshold for “very low”

            high_count = sum(1 for s in scores if s >= high_threshold)
            low_count = sum(1 for s in scores if s <= low_threshold)

            if high_count >= len(scores) - 1:  # all or almost all high
                insights.append(
                    "- Power distribution is extremely high across all axes; may be overpowered"
                )
                requires_review = True
            elif low_count >= len(scores) - 1:  # all or almost all low
                insights.append(
                    "- Power distribution is extremely low across all axes; may be underpowered"
                )
                requires_review = True
        else:
            insights.append("- No power scores available")
            requires_review = True

        # Multiplier check
        multipliers = results.get("multiplier", [])
        multiplier_value = None
        if multipliers:
            if len(multipliers) > 1:
                insights.append(f"- Multiple multipliers found: {multipliers}")
                requires_review = True

            # Just evaluate the first multiplier
            first = str(multipliers[0]).strip()
            match = re.search(r"\d+(\.\d+)?", first.replace(",", "."))
            if match:
                multiplier_value = float(match.group(0))
            else:
                insights.append(f"- Multiplier value may be invalid: {first}")
                requires_review = True

        if multiplier_value and multiplier_value > 5:
            insights.append(
                f"- High multiplier ({multiplier_value}) may be unbalanced")
            requires_review = True

        # Cooldown check
        cooldowns = results.get("cooldown", [])
        cooldown_value = None
        if cooldowns:
            if len(cooldowns) > 1:
                insights.append(f"- Multiple cooldowns found: {cooldowns}")
                requires_review = True

            first = str(cooldowns[0]).strip()
            match = re.search(r"\d+", first)
            if match:
                cooldown_value = float(match.group(0))
            else:
                insights.append(f"- Cooldown value may be invalid: {first}")
                requires_review = True

        if cooldown_value and cooldown_value < 2:
            insights.append(
                f"- Very short cooldown ({cooldown_value}) may be unbalanced")
            requires_review = True

        # --- New: check top_categories against expected rank ---
        ranks = results.get("rank", [])
        if ranks:
            if len(ranks) > 1:
                insights.append(f"- Multiple ranks found: {ranks}")
                requires_review = True

            first = str(ranks[0]).strip()
            top_categories: list[tuple[str, float]] = results.get("top_categories", [])

            # --- New: check confidence scores ---
            confidences = [conf for _, conf in top_categories]
            if all(conf < 10.0 for conf in confidences):  # 10% threshold
                insights.append("- Poor alignment with category criteria")
                requires_review = True

            categories = [category for category, _ in top_categories]
            if not self.compare_categories(categories, first):
                insights.append(
                    f"- Top predicted categories do not match expected rank ({first})"
                )
                requires_review = True

        return requires_review, insights

    def compare_categories(self, top_categories: list[str], expected_rank: str) -> bool:
        expected_rank_norm = self.normalize_rank_text(expected_rank)
        return any(
            expected_rank_norm ==
            self.normalize_rank_text(category)
            for category in top_categories)

    def normalize_rank_text(self, text: str) -> str:
        # Remove decorative symbols
        text = re.sub(r'[☆★<>\[\]]', '', text).strip()

        # Find all alphanumeric tokens (+/- allowed)
        tokens = re.findall(r'[A-Za-z0-9]+[+-]?', text)

        if not tokens:
            return text.upper()

        # Filter out common descriptor words
        blacklist = {"RANK", "TIER", "GRADE", "RARITY", "CLASSIFICATION", "ABILITY"}
        candidates = [t for t in tokens if t.upper() not in blacklist]

        if candidates:
            return candidates[0].upper()
        else:
            # if everything was blacklisted, just take the last token
            return tokens[-1].upper()
