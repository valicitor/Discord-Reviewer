import re

class AdminItemInsights:

    def __init__(self):
        pass

    def generate(self, results):
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

        # Starting PL check
        artificialpls = results.get("artificialpl", [])
        if artificialpls:
            if len(artificialpls) > 1:
                insights.append(f"- Multiple starting PLs found: {artificialpls}")
                requires_review = True

            first = str(artificialpls[0]).strip()
            match = re.search(r"\d+", first)
            if not match:
                insights.append(f"- Starting PL value may be invalid: {first}")
                requires_review = True
        else:
            insights.append(f"- No Starting PL found")

        return requires_review, insights
