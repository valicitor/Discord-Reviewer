import re

class TrainingLogEvaluator:
    """
    Evaluates structured training log data for OC power level updates.
    More flexible than earlier versions — does not depend on strict headers like 'OC Training Log'.
    """

    def __init__(self):
        # Minimum number of key fields (name + gains + power level) for a post to be considered valid
        self.valid_threshold = 3

    # =========================
    # Main Evaluation Pipeline
    # =========================
    def evaluate(self, data):
        results = []
        total_entries = 0
        total_correct = 0
        bad_entries = []

        for post_id, post_content in data.items():
            parsed = self.parse_structured_post(post_id, post_content)
            if not parsed["is_training_update"]:
                continue

            total_entries += 1
            correct = self.validate_calculations(parsed)
            parsed["computed_correctly"] = correct

            if correct:
                total_correct += 1
            else:
                bad_entries.append(parsed)

            results.append(parsed)

        return {
            "total_correct": total_correct,
            "total_entries": total_entries,
            "bad_entries": bad_entries,
            "all_results": results,
        }

    # ==================================
    # Parsing Structured Discord Message
    # ==================================
    def parse_structured_post(self, post_id, sections):
        entry = {
            "post_id": post_id,
            "is_training_update": False,
            "name": None,
            "location": None,
            "old_power_level": None,
            "new_power_level": None,
            "training_gains": [],
            "calculation_headers": [],
        }

        # Search for structured subsections
        for section in sections:
            header = section.get("header", "").strip()
            subsections = section.get("subsections", [])
            content = section.get("content", [])

            # Detect probable math/calculation lines (e.g., "32,996 + 10k = 42996")
            if re.search(r"\d+.*[+\-%=]", header):
                entry["calculation_headers"].append(header)

            # Check subsections for known fields
            for sub in subsections:
                subheader = sub.get("subheader", "").strip().lower()
                subcontent = [c.strip() for c in sub.get("content", []) if c.strip()]

                if not subcontent:
                    continue
                val = " ".join(subcontent).replace(",", "")

                if "name" in subheader:
                    entry["name"] = val

                elif "location" in subheader:
                    entry["location"] = val

                elif "old power level" in subheader:
                    entry["old_power_level"] = self.parse_number(val)

                elif any(k in subheader for k in ["new power level", "total", "current power level"]):
                    entry["new_power_level"] = self.parse_number(val)

                elif "gain" in subheader:
                    # Append each gain line as a separate gain component
                    for g in subcontent:
                        g = g.replace(",", "").strip()
                        if g:
                            entry["training_gains"].append(g)

        # Post-classification
        confidence_score = sum([
            bool(entry["name"]),
            bool(entry["training_gains"]),
            bool(entry["old_power_level"] or entry["new_power_level"])
        ])

        entry["confidence_score"] = confidence_score
        entry["is_training_update"] = confidence_score >= self.valid_threshold

        return entry

    # =========================================
    # Validates the numeric consistency of logs
    # =========================================
    def validate_calculations(self, entry):
        old_pl = entry.get("old_power_level")
        new_pl = entry.get("new_power_level")

        # If no old power level, cannot compute
        if old_pl is None:
            return False

        total_gain = 0
        multiplier = 1.0

        for g in entry.get("training_gains", []):
            # Each gain line can be a percent, flat value, or a mix
            gain_val = self.parse_number(g, base_value=old_pl)
            # If it's a percent-only gain, parse_number already handles it
            # Some gains can be "10% to gains" -> apply to multiplier
            if "to gain" in g.lower() or "to gains" in g.lower():
                percent_match = re.search(r"([\d.]+)\s*%", g)
                if percent_match:
                    bonus = float(percent_match.group(1)) / 100
                    multiplier += bonus
            else:
                total_gain += gain_val

        # Compute expected new power level
        expected_new = int((old_pl + total_gain) * multiplier)
        entry["expected_new_power_level"] = expected_new

        if new_pl is None:
            entry["computed_only"] = True
            return True  # can't compare but computation succeeded

        return abs(expected_new - new_pl) <= 2  # tolerate small rounding differences

    # ========================
    # Number Parsing Utilities
    # ========================
    def parse_number(self, value_str, base_value=None):
        """Parse strings like '10k', '25%', or raw numbers."""
        if not value_str:
            return 0

        # Remove URLs and formatting
        value_str = re.sub(r"https?://\S+", "", value_str)
        value_str = value_str.replace(",", "").strip().lower()

        # Handle percentage gain
        percent_match = re.search(r"([\d.]+)\s*%", value_str)
        if percent_match and base_value is not None:
            percent = float(percent_match.group(1))
            return int(base_value * (percent / 100))

        # Handle flat numeric with k/m suffix
        multiplier_match = re.search(r"(\d+(?:\.\d+)?)\s*([km]?)", value_str)
        if multiplier_match:
            num = float(multiplier_match.group(1))
            suffix = multiplier_match.group(2)
            multiplier = 1
            if suffix == "k":
                multiplier = 1_000
            elif suffix == "m":
                multiplier = 1_000_000
            return int(num * multiplier)

        return 0
