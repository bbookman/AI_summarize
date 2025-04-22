Overview:
You will receive one or two US English speech-to-text files—"Bee" (higher quality) and "Limitless"—each with a date header (YYYY-MM-DD), a whole-day summary, and segmented conversation data (e.g., conversation summaries, conversation IDs, locations, atmosphere notes, key takeaways, and bullet-pointed transcripts). Additionally, two supplemental files will be provided:

Facts: Verified supplemental information.

Errors: Previously derived, incorrect details (to be disregarded).

Objective:
Generate a markdown document.

Guidelines:

Do not include the date anywhere in the document.

Never write the following in the file: ```markdown

If both files are provided, prioritize Bee data.

Review all provided content (files and supplements) and reconcile differences, carefully considering facts and errors to inform your analysis.

Use transcript content only for contextual support—do not include direct quotes, speaker names, or timestamps.

Markdown Document Structure
Summary of the Day:
A single line identifying the source data. Example:

Source: Bee, Limitless

Source: Bee

Source: Limitless

A concise (maximum 6 sentences) first-person recap of the day. If any US holiday occurred, the family may have celebrated—note significant events or celebrations.

Sentiment Analysis:
Categorize overall mood as Good, Neutral, or Bad.

Measure frustration level as High, Medium, or Low.

Include a markdown table with sentiment percentages totaling 100%.

Key Highlights:
Up to 5 bullet points highlighting birthdays, holidays, vacations, significant moments, lessons learned, or notable occurrences.

Journal Entry:
If the transcript includes a mention of journaling, generate a narrative about the subject (person, place, or event).

If no mention of "journal" appears, omit this section entirely.

Learnings:
Identify only procedural content: Review transcripts and summaries for newly learned methods, procedures, or processes.

If identified, outline them in step-by-step numbered format, detailing specific actions.

Do not include general observations, reflections, or abstract insights.

If no procedural content is present, omit this section entirely—no heading, no text.

Health Status:
Only generate a statement about health if transcripts or summaries explicitly reference a health status (e.g., symptoms, test results, or conditions). Otherwise, do not generate a statement.

If health measurements were explicitly recorded, include them in a markdown table. Only list numerical values for:

Blood pressure

Heart rate

Blood sugar

Weight

Height

Step count

If no measurements are provided, omit the table entirely.

If a conversation with a medical professional is documented, provide a detailed summary strictly based on transcript content.

Include any changes in medication or treatment.

List future appointments or important follow-ups as bullet points.

If no relevant health information is available, omit this section entirely—no heading, no text.

Data Placeholders:
Bee Data: {BEE_CONTENT}

Limitless Data: {LIMITLESS_CONTENT}

Known Errors: {ERRORS_CONTENT}

Facts Information: {FACTS_CONTENT}
