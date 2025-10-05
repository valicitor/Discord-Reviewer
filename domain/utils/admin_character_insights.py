import re

class AdminCharacterInsights:
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
              insights.append("- Summary may be too brief or not descriptive")
              requires_review = True

        # Race Type check
        race_types = results.get("race_type", [])
        if race_types:
            if len(race_types) > 1:
                insights.append(f"- Multiple race types found: {race_types}")
                requires_review = True
            elif race_types:
                insights.append(f"- Possible limited race type found: {race_types}")
                requires_review = True

        
        # Starting PL check
        starting_pls = results.get("startingpl", [])
        if starting_pls:
            if len(starting_pls) > 1:
                insights.append(f"- Multiple starting PLs found: {starting_pls}")
                requires_review = True
            
            first = str(starting_pls[0]).strip()
            match = re.search(r"\d+", first)
            if not match:
                insights.append(f"- Starting PL value may be invalid: {first}")
                requires_review = True
        else:
            insights.append(f"- No Starting PL found")

        return requires_review, insights