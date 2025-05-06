Overview:
You will receive one or two speech-to-text files—"Bee" and "Limitless"—each with a date header (YYYY-MM-DD), a whole-day summary, and segmented conversation data (e.g., conversation summaries, conversation IDs, locations, atmosphere notes, key takeaways, and bullet-pointed transcripts). Additionally, two supplemental files will be provided:

Facts: Verified supplemental information.

Errors: Previously derived, incorrect details (to be disregarded).

Objective:
Generate a markdown document that captures the day's events in a journal-like format. 
Review all provided content (files and supplements) and reconcile differences, carefully considering facts and errors to inform your analysis.

Guidelines:

Do not include the date anywhere in the document.

Never write the following in the file: ```markdown

If both Bee and Limitless files are provided, prioritize Bee data.


Markdown section generation instructions:

Journal Entry: Only include this section if the day's transcript contains the word "journal," "journaling," or "journals" (regex: `/journal(ing|s)?/i`). Do not write the header nor any text for this section if the day's transcript does not contain the word "journal," "journaling," or "journals."

Note the optional sections below.  They should not be included if the day's transcript does not contain the trigger words.

Markdown Document Structure
START

# Summary of <Day name .. example Monday, Tuesday>:

For the line identifying the data source(s), strictly follow this logic to produce a single line in the format "Source(s): [Derived Source Name]":
- If the {BEE_CONTENT} variable contains actual data (i.e., is not "No data available") AND the {LIMITLESS_CONTENT} variable is "No data available", then the line MUST be: **Source(s): Bee**
- If BOTH the {BEE_CONTENT} variable AND the {LIMITLESS_CONTENT} variable contain actual data (i.e., neither is "No data available"), then the line MUST be: **Source(s): Bee and Limitless**
- If the {LIMITLESS_CONTENT} variable contains actual data AND the {BEE_CONTENT} variable is "No data available", then the line MUST be: **Source(s): Limitless**

A first-person recap of the day

## Key Highlights:

5 bullet points highlighting birthdays, holidays, vacations, significant moments, lessons learned.


OPTIONAL
## Journal Entry:

**CRITICAL: Only include the "## Journal Entry:" header and the following content IF the day's transcript contains "journal," "journaling," or "journals" (regex: `/journal(ing|s)?/i`). If these words are NOT found, OMIT THIS ENTIRE "Journal Entry" SECTION, including its header AND the "Sentiment Analysis" subsection below.**

Use transcript content for context but avoid direct quotes, speaker names, or timestamps.

### Sentimaent Analysis:
Overall sentiment: A single line stating the highest sentiment.
Sentement percentages: Positive: %, Neutral: %, Negative: %

Sentiment Rationale: A single paragraph (3-4 sentences) explaining the basis for the sentiment analysis. This should briefly reference the source data, such as the number of positive, negative, or neutral summaries or transcript segments. For example: "The positive sentiment was derived from several joyful summaries and interactions noted in the Bee transcripts. Only one transcript segment indicated a negative tone, while the remaining data was largely neutral."

OPTIONAL
## Health, Wellness and Mood:
OPTIONAL
### General
Health Rating: A single line measure of health as Excellent, Good, Fair, or Poor. If no statements in the day related to the health of Bruce Bookman, mark as N/A.
Sleep Quality: A single line measure of sleep quality as Excellent, Good, Fair, or Poor. If no statements in the day related to the sleep quality of Bruce Bookman, mark as N/A.
Streess Level: A single line measure of stress level as High, Medium, Moderate or Low. If no statements in the day related to the stress level of Bruce Bookman, mark as N/A.
Frustration level: A single line measure of frustration level as High, Medium, Moderate or Low.
Allergy Level: A single line measure of allergy level as High, Medium, Moderate or Low. If no statements in the day related to the health of Bruce Bookman, mark as N/A.

OPTIONAL
### Health Data:
Trigger words: Only include this section if the day's transcript contains the words like "weight", "steps", "walked", "Blood sugar", "Blood Glucose", "Bilogical age", "Cardiovascular", "Renal", "Metabolic". These words will be followed by a measurement. Do not write the header nor any text for this section if the day's transcript does not contain the words like "weight", "steps", "walked" or "Blood sugar", "Blood Glucose".

In the Range column, provide the following:

For Blood Sugar:
- Below 80: LOW
- 80 to 130: NORMAL
- Above 130: HIGH

For Weight (lbs): **Adhere strictly to these ranges for the 'Range' column:**
- Below 132 lbs: LOW
- 133 lbs to 173 lbs: NORMAL
- 174 lbs to 208 lbs: OVERWEIGHT
- 209 lbs and above: OBESE

For Step count:
- Below 6000: LOW
- 6000 to 10000: HEALTHY
- Above 10000: GREAT

| Measurement | Value | Range |
| ----------- | ----- | ----- |
| Blood sugar |       |       |
| Weight      |       |        |
| Step count  |       |        |
| Biological age |       |        |



OPTIONAL
### Medical Consultation:

CRITICAL: Only include the "### Medical Consultation:" header and the following content IF a medical visit (doctor, dentist, or any medical professional) is detected in the day's transcript. If no medical visit is detected, OMIT THIS ENTIRE "Medical Consultation" SECTION, including its header

Trigger: A medical visit includes a visit to a doctor, dentist, or any medical professional.
If a medical visit is detected in the transcripts for the day provide a 3 sentence summary of the medical visit focusing on medical condition, include any changes in medication or treatment or medical concerns raised. Mark Armitage is my primary doctor.

Add 3 bullet points of follow up or practices I should engage in based directly on the conversation transcripts with the medical professional.

OPTIONAL
### Psychological Visit:

CRITICAL: Only include the "### Psychological Visit:" header and the following content IF a psychological visit (e.g., triggered by words like "Bipolar", "Larry", "Anxiety", "Depression", or a Monday 3 PM appointment) is detected in the day's transcript. If no such visit is detected, OMIT THIS ENTIRE "Psychological Visit" SECTION, including its header.

Trigger Words: "Bipolar", "Larry", "Anxiety", "Depression", "Manic", "Mania".  The visit will most likely be on a Monday or Tuesday at 3 pm. Check the date and time and trigger words as part of the detection of a psychologist visit.

If a visit to a psychologist is detected, provide a 3 sentence summary and include a 3 bullet point list of follow up or practices I should engage in based directly on the conversation transcripts.

### Psychiatrist Visit:
CRITICAL: Only include the "### Psychiatrist Visit:" header and the following content IF a visit to a psychiatrist is detected in the day's transcript. If no visit to a psychiatrist is detected, OMIT THIS ENTIRE "Psychiatrist Visit" SECTION, including its header

Trigger Words: "Dorinda", "Dorinda Dew", "Coastal Carolina Neuropsychiatric Center". If a visit to a psychiatrist is detected, provide a 3 sentence summary and include a 3 bullet point list of follow up or practices I should engage in based directly on the conversation transcripts. 

END

Data:
Bee Data: {BEE_CONTENT}

Limitless Data: {LIMITLESS_CONTENT}

Known Errors: {ERRORS_CONTENT}

Facts Information: {FACTS_CONTENT}
