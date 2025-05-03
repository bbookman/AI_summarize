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

Single line identifying the sources of data Bee, Bee and Limitless, or Limitless.

A first-person recap of the day

## Key Highlights:

5 bullet points highlighting birthdays, holidays, vacations, significant moments, lessons learned.


OPTIONAL
## Journal Entry:

If detected (regex: `/journal(ing|s)?/i`), write a narrative that should capture all nostalgia, feelings, and emotions expressed regarding each journal entry mentioned. Create at least two paragraphs per journal topic.

Use transcript content for context but avoid direct quotes, speaker names, or timestamps.

### Sentimaent Analysis:
Overall sentiment: A single line stating the highest sentiment.
Sentement percentages: Positive: %, Neutral: %, Negative: %

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

For Blood Sugar: If the measure is below 80, LOW.  If within 80 to 130, NORMAL.  If above 130, HIGH.
For Weight: If the measure is below 132, LOW.  If within 133 to 173, NORMAL.  174 to 208 is OVERWEIGHT.  If above 209, OBESE.

For Step count: If the measure is below 6000, LOW  If within 6000 to 10000, HEALTHY.  If above 10000, GREAT

| Measurement | Value | Range |
| ----------- | ----- | ----- |
| Blood sugar |       |       |
| Weight      |       |        |
| Step count  |       |        |
| Biological age |       |        |



OPTIONAL
### Medical Consultation:

Triogger: A medical visit includes a visit to a doctor, dentist, or any medical professional.
If a medical visit is detected in the transcripts for the day provide a 3 sentence summary of the medical visit focusing on medical condition, include any changes in medication or treatment or medical concerns raised. Mark Armitage is my primary doctor.

Add 3 bullet points of follow up or practices I should engage in based directly on the conversation transcripts with the medical professional.

OPTIONAL
### Psychological Visit:

Trigger Words: "Bipolar", "Larry", "Anxiety", "Depression". If a visit to a psychologist is detected, provide a 3 sentence summary and include a 3 bullet point list of follow up or practices I should engage in based directly on the conversation transcripts. Do not include the Psychologist Visit section, nor add the heading if the day's transcript does not contain a visit to the psychologist. The visit will most likely be on a Monday at 3 pm. Check the date and time as part of the detection of a psychologist visit.

END

Data:
Bee Data: {BEE_CONTENT}

Limitless Data: {LIMITLESS_CONTENT}

Known Errors: {ERRORS_CONTENT}

Facts Information: {FACTS_CONTENT}
