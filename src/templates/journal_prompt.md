Overview: You will receive one or two US English speech-to-text files—"Bee" (higher quality) and "Limitless"—each with a date header (YYYY-MM-DD), a whole-day summary, and segmented conversation data (e.g., conversation IDs, locations, atmosphere notes, key takeaways, and bullet-pointed transcripts). Also provided are two supplemental files:

Facts: Verified supplemental information.

Errors: Previously derived, incorrect details (to be disregarded).

Objective: Generate a markdown document containing:

Summary of the day:

A concise (max 4 sentences) factual recap of key events.

Sentiment Analysis:

Categorize overall mood as Good, Neutral, or Bad.

Include a markdown table with sentiment percentages that total 100%.

Atmosphere:

A brief tone/mood analysis (up to 4 sentences), using Bee’s "Atmosphere" data when available, supplemented by Limitless data if needed.

Key Takeaways:

Up to 5 bullet points (each under 10 words) summarizing actionable insights.

Include this section only if at least one takeaway is present.

Guidelines:

If both files are provided, prioritize Bee data.

Review all provided content (files and supplements) and reconcile differences.

Use transcript content only for contextual support—do not include direct quotes, speaker names, or timestamps.

Data Placeholders:

Bee Data: {BEE_CONTENT}

Limitless Data: {LIMITLESS_CONTENT}

Known Errors: {ERRORS_CONTENT}

Facts Information: {FACTS_CONTENT}
