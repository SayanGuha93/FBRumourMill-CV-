import os
from dotenv import load_dotenv
from groq import Groq
import json

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def extract_transfer_info(article):
    prompt = f"""
You are a highly accurate football transfer news analyst.

Analyze ONLY the information contained in this article.

Title:
{article["title"]}

Description:
{article["description"]}

Determine whether the article itself reports a genuine player transfer
rumour or transfer development.

IMPORTANT RULES:

1. Return true ONLY when the article explicitly discusses a player
   potentially moving from one club to another.

2. Do NOT classify an article as a transfer rumour merely because:
   - it mentions a transfer window
   - it mentions a player's previous transfer
   - it mentions a player who was previously linked with a club
   - it discusses contracts without a transfer
   - it mentions the word "transfer" in passing
   - it is a general football news article.

3. Do NOT infer missing information.

4. If you cannot confidently identify BOTH the player and destination
   club, return is_transfer_rumour as false.

5. The transfer_stage must be based only on explicit information
   in the article.

6. confidence represents your confidence that this is genuinely a
   transfer report AND that the extracted information is correct.

7. Only use confidence >= 60 when the article provides reasonably
   clear evidence.

8. Return ONLY valid JSON.

Return exactly:

{{
    "is_transfer_rumour": false,
    "player_name": null,
    "current_club": null,
    "destination_club": null,
    "transfer_stage": null,
    "confidence": 0,
    "evidence": null
}}

If it IS a genuine transfer report, return:

{{
    "is_transfer_rumour": true,
    "player_name": "Player name",
    "current_club": "Current club",
    "destination_club": "Destination club",
    "transfer_stage": "linked",
    "confidence": 85,
    "evidence": "Short sentence from the article describing the transfer situation."
}}

Allowed transfer stages:
- linked
- interested
- in talks
- negotiation
- bid
- offer
- agreement
- medical
- completed
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0,
    )

    result = response.choices[0].message.content.strip()

    try:
        return json.loads(result)
    except json.JSONDecodeError:
        return {
            "is_transfer_rumour": False,
            "player_name": None,
            "current_club": None,
            "destination_club": None,
            "transfer_stage": None,
            "confidence": 0,
            "evidence": None,
        }