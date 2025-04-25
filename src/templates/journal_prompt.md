Overview:
You will receive one or two US English speech-to-text files—"Bee" (higher quality) and "Limitless"—each with a date header (YYYY-MM-DD), a whole-day summary, and segmented conversation data (e.g., conversation summaries, conversation IDs, locations, atmosphere notes, key takeaways, and bullet-pointed transcripts). Additionally, two supplemental files will be provided:

Facts: Verified supplemental information.

Errors: Previously derived, incorrect details (to be disregarded).

Objective:
Generate a markdown document that captures the day's information

Guidelines:

Do not include the date anywhere in the document.

Never write the following in the file: ```markdown

Do not generate the journal entry section if the day's transcript does not include a mention of journaling or the word journal.
There may be more than one journal subject discussed. Create a paragraph for each subject.

Review the day data. If a medical consultation is not encountered, do not include the Medical Consultation section.
Review the day data. If a psychological consultation is not encountered, do not include the Psychological Consultation section.

If both Bee and Limitless files are provided, prioritize Bee data.

Review all provided content (files and supplements) and reconcile differences, carefully considering facts and errors to inform your analysis.

Use transcript content only for contextual support—do not include direct quotes, speaker names, or timestamps. However, do note the word "journal" as this should trigger creating a journal section described below.

Markdown section generation instructions:

Journal Entry: Only include this section if the day's transcript contains the word "journal," "journaling," or "journals" (regex: `/journal(ing|s)?/i`). Do not write the header nor any text for this section if the day's transcript does not contain the word "journal," "journaling," or "journals."

Health Data: Only include this section if the day's transcript contains the words like "weight", "steps", "walked", "Blood sugar" or "Blood Glucose". These words will be followed by a measurement. Do not write the header nor any text for this section if the day's transcript does not contain the words like "weight", "steps", "walked" or "Blood sugar" or "Blood Glucose".

Psychologist Visit: The majority of visits to my psychologist occur on a Monday at 3 pm. These visits are usually 60 minutes long. Words such as "anxiety", "bipolar" or "mania" may indicate a visit has occurred. If no visit is encountered, do not include the Psychologist Visit section. o not write the header nor any text for this section if the day's transcript does not contain a visit to the psychologist. Bruce Bookman and Larry will be the only speakers, do not include the Psychologist Visit section if there are any other spearkers for the transcript sections relating to the psychologist visit.

Markdown Document Structure
START

# Summary of <Day name .. example Monday, Tuesday>:

Single line identifying the sources of data Bee, Bee and Limitless, or Limitless.

first-person recap of the day

## Sentiment Analysis:

Frustration level: A single line measure of frustration level as High, Medium, or Low.
Overall sentiment: A single line stating the highest sentiment.
Health Rating: A single line measure of health as Good, Fair, or Poor. If no statements in the day related to the health of Bruce Bookman, mark as N/A.

| Sentiment | % |

| --- | --- |
| Positive | percentage |
| Neutral | percentage |
| Negative | percentage |

## Key Highlights:

Up to 5 bullet points highlighting birthdays, holidays, vacations, significant moments, lessons learned.

## Journal Entry:

If detected as described above (regex: `/journal(ing|s)?/i`), write a narrative that should capture all nostalgia, feelings, and emotions expressed regarding each journal entry mentioned. Create at least two paragraphs per journal topic.

Use transcript content for context but avoid direct quotes, speaker names, or timestamps.

## Health Data:

Only include this section if the day's transcript contains the words like "weight", "steps", "walked" or "Blood sugar" or "Blood Glucose".

| Measurement | Value |
| ----------- | ----- |
| Blood sugar |       |
| Weight      |       |
| Step count  |       |

## Medical Consultation:

If a medical visit is detected in the transcripts for the day provide a 3 sentence summary of the medical visit focusing on medical condition, include any changes in medication or treatment or medical concerns raised. Mark Armitage is my primary doctor.

## Psychological Visit:

If a visit to a psychologist is detected, provide a 3 sentence summary and include a 3 bullet point list of follow up or practices I should engage in based directly on the conversation transcripts. Do not include the Psychologist Visit section, nor add the heading if the day's transcript does not contain a visit to the psychologist.

END

Data:
Bee Data: {BEE_CONTENT}

Limitless Data: {LIMITLESS_CONTENT}

Known Errors: {ERRORS_CONTENT}

Facts Information: {FACTS_CONTENT}
