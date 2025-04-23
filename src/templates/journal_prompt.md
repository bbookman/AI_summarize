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

If no blood sugar, weight or steps count are described, do not include the Health Data section.

Review the day data. If a medical consultation is not encountered, do not include the Medical Consultation section.
Review the day data. If a psychological consultation is not encountered, do not include the Psychological Consultation section.

If both Bee and Limitless files are provided, prioritize Bee data.

Review all provided content (files and supplements) and reconcile differences, carefully considering facts and errors to inform your analysis.

Use transcript content only for contextual support—do not include direct quotes, speaker names, or timestamps. However, do note the word "journal" as this should trigger creating a journal section described below.

Markdown Document Structure
START

# Summary of <Day name .. example Monday, Tuesday>:

Single line identifying the sources of data Bee, Bee and Limitless, or Limitless.

first-person recap of the day

## Sentiment Analysis:

A single line measure of frustration level as High, Medium, or Low.
A single line stating the highest sentiment. Example: Positive

| Sentiment | % |

| --- | --- |
| Positive | percentage |
| Neutral | percentage |
| Negative | percentage |

## Key Highlights:

Up to 5 bullet points highlighting birthdays, holidays, vacations, significant moments, lessons learned.

Do not include the section below if no journal entry is found.

## Journal Entry:

This narrative will be as lengthy as needed to capture the details provided by the transcript if the word "journal" is seen. It should capture all the nostalgia, the feelings and emotions exxpressed regarding each journal entry. There may be more than one journal entry topic. Create at least one paragraph for each journal topic. Include quotes that illustrate the feelings and emotions expressed or the facts stated.

Do not include the section below if no health data is found.

## Health Data:

| Measurement | Value |
| ----------- | ----- |
| Blood sugar |       |
| Weight      |       |
| Step count  |       |

Do not include the section below if no medical consultation is found.

## Medical Consultation:

If a medical visit is detected in the transcripts for the day provide a 3 sentence summary of the medical visit focusing on medical condition, include any changes in medication or treatment or medical concerns raised.

Do not include the section below if no psychological consultation is found.

## Psychological Visit:

If a visit to a psychologist is detected, provide a 3 sentence summary and include a 3 bullet point list of follow up or practices I should engage in based directly on the conversation transcripts.

END

Data:
Bee Data: {BEE_CONTENT}

Limitless Data: {LIMITLESS_CONTENT}

Known Errors: {ERRORS_CONTENT}

Facts Information: {FACTS_CONTENT}
