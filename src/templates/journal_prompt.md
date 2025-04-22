Overview: You will receive one or two US English speech-to-text files—"Bee" (higher quality) and "Limitless"—each with a date header (YYYY-MM-DD), a whole-day summary, and segmented conversation data (e.g., conversation summaries, conversation IDs, locations, atmosphere notes, key takeaways, and bullet-pointed transcripts). Also provided are two supplemental files:

Facts: Verified supplemental information.

Errors: Previously derived, incorrect details (to be disregarded).

Objective: Generate a markdown document

NOTE: do not state the date in the document anyplace
NOTE: do not ever write the following to the file "```markdown"

Summary of the day:
A single line identifying the source data. Such as
Source: Bee, Limitless
Source: Bee
Source: Limitless

A concise (max 6 sentences) first person recap of the day. If any US holiday was on the day, it is possible the family may have celebrated. Note any significant events or celebrations.

Sentiment Analysis:

Categorize overall mood as Good, Neutral, or Bad.
Add a measure of frustration level: High, Medium, or Low.

Include a markdown table with sentiment percentages that total 100%.

Key Highlights:

Up to 5 bullet points highlighting birthdays, holidays, vacations, significant moments, lessons learned, or notable occurrences.

Learnings:

Identify only procedural content: Review the transcripts and summaries for any new methods, procedures, or processes that you learned during the day.

Step-by-step format: If you identify a new procedure or process, outline it as a sequential, step-by-step numbered list. Each step should detail a specific action that contributes to completing the process.

Exclude non-procedural insights: Do not include general observations, reflections, or abstract insights that are not organized as a clear process.

Omit if irrelevant: If no new procedural content is found, skip this section entirely. No heading, no text

Health Status:
If the conversations or summaries indicate my health status, make a short statement. Ignore the facts supplementtal file. No general statements form this file are relevant.

If health measurements were taken, include them in a markdown table.

If no information is available, skip this section entirely. No heading, no text

Guidelines:

If both files are provided, prioritize Bee data.

Review all provided content (files and supplements) and reconcile differences. Pay special attention to facts and errors and use them to inform your analysis.

Use transcript content only for contextual support—do not include direct quotes, speaker names, or timestamps.

Data Placeholders:

Bee Data: {BEE_CONTENT}

Limitless Data: {LIMITLESS_CONTENT}

Known Errors: {ERRORS_CONTENT}

Facts Information: {FACTS_CONTENT}
