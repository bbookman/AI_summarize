You will be given one or two text collections. One of these is known as "Bee" and the other as "Limitless". Your ultimate goal is to generate a third text document containing a "Best of Class" analysis and summaries derived from the source data. The source files contain US English AI-derived speech-to-text results from conversations, broken into segments. The two files differ in content and format.

You will be provided with two supplemental documents:

- A **Facts** file, with the heading "Facts", which contains verified, supplemental factual information to assist in deriving the best in class file.
- An **Errors** file, with the heading "Errors", detailing information previously derived by the AI that has been deemed incorrect. Use this document to identify and disregard erroneous details.

### Source File Formats

**Bee File Format:**

- **High-level summaries:** Denoted by `#` markdown for each conversation segment.
- **Conversation details:**
  - _Conversation ID:_ Prefixed with "Conversation ID:"
  - _Location:_ Prefixed with "Location:"
- **Within each segment:**
  - **Second-level summaries:** Denoted by `##` markdown.
  - **Atmosphere:** A description of the conversation tone, denoted by the word "Atmosphere:" followed by descriptive text
  - **Key Takeaways:** Denoted by `"Key Takeaways" with each takeaway bullet-pointed.
  - **Transcripts:** Bullet-pointed (-) sentences that capture the spoken dialogue. These include a speaker tag and the spoken words. Examples:
  - Speaker 2: I would make myself a perfect.
  - Speaker 1: Open, I'm hearing all right.
  - **Facts:** Bullet-pointed (-) sentences that capture factual information.

**Limitless File Format:**

- **File heading:** YYYY-MM-DD
- **High-level summaries:** Denoted by `#` markdown for each conversation segment.
- **Within each segment:**
  - **Second-level summaries:** Denoted by `##` markdown.
  - **Transcripts:** Bullet-pointed (-) sentences that capture the spoken dialogue. These include a speaker tag, a time, and the spoken words. Examples:
    - \_Speaker 1 (3/2/25 8:46 AM): The what?
    - \_You (3/2/25 8:46 AM): Sorry.

### Analysis Guidelines

- **Data Quality Priority:** The Bee data is considered higher quality and should have a higher influence on the analysis.
- **Overall Objective:**
  - **Factual Recap:** Reconstruct conversational intent and flow by delivering a factual, objective narrative of what happened during the day.
  - **Emotional Tone:** Separately, analyze the tone and mood to capture how the events felt.
  - Emphasize actionable insights and conclusions, strictly summarizing the data without offering suggestions.
- **Presentation Style:**
  - Prioritize clarity and conciseness.
  - The **Full Day Summary** should provide a factual, comprehensive recap of key events and overarching themes, focusing on what happened\_ during the day. Keep this section concise—limit it to no more than 4 sentences.
  - The **Atmosphere** section should capture the emotional tone and mood (focusing on how the day felt\_) using interpretive insights. Also limit this section to no more than 4 sentences
  - The **Key Takeaways** section must be clearly actionable. It will contain no more than 7 bullet points. Each point will contain no more than 10 words.
- **Transcript Handling:**
  - Use transcripts from the data as supporting context for analysis
  - Consider speaker interactions and dialogue when analyzing tone and atmosphere
  - Do NOT include any direct transcript quotes in the final output
  - Do NOT include speaker names or timestamps in the output
  - Use transcript content only to inform the overall analysis and mood interpretation

### Steps for Analysis

1. **Review Data:**

   - Examine the entire contents of each provided file.
   - If only one file is available, conduct the analysis solely based on that file.

2. **Review Supplemental Information:**

   - **Facts Information:**
     {FACTS_CONTENT}
   - **Known Errors:**
     {ERRORS_CONTENT}
   - Apply factual information to enhance analysis accuracy.
   - Use error list to avoid known incorrect interpretations.

3. **Full Day Summary:**

   - Create a unique summary for the full day that emphasizes overarching themes, key events, and actions—detailing what happened. Keep it brief (no more than 4 sentences).

4. **Reconciliation of Data:**

   - When both files are provided, fully reconcile and integrate the high-level conversation summaries and the second-level segment summaries for each segment.
   - Use transcript data as needed to support the reconciliation.

5. **Atmosphere Analysis:**

   - Use the provided Bee Atmosphere data if available.
   - Additionally, independently analyze the tone and emotional context from the combined data to include interpretive insights—focusing on _how the day felt_. Keep this section concise (limit to 4 sentences)
   - If no Atmosphere data is available, derive the analysis solely from the combined data.

6. **Key Takeaways:**

   - Summarize actions or decisions—even if they need to be inferred from the data.
   - Derive potential implications and recommendations based on the provided context.
   - Determine the number of key takeaways solely from the data (it may have between 0 and 7 points).
   - If there are no key takeaways derived from the data, omit this section entirely.

7. **Unique Sections:**
   Identify unique subsections from each set of data (Bee and Limitless)

### Source Data for Analysis

**Bee Data:**
{BEE_CONTENT}

**Limitless Data:**
{LIMITLESS_CONTENT}

### Output Format

- **High-Level Day Summary:**
  - Denoted by `#` markdown.
  - Provide a factual, objective narrative that recaps the day's key events, overarching themes, and actions—focusing on what happened. \*Be concise and keep it to a maximum of 4 sentences
- **Atmosphere:**
  - Denoted by `## Atmosphere`.
  - Provide a description of the tone and mood with interpretive, conversational insights—focusing on
    how the day felt. Keep this description brief (up to 4 sentences).
- **Key Takeaways:**

  - Denoted by `## Key Takeaways`.
  - Use bullet points (`*`) for each takeaway, ensuring each point is clearly actionable.
  - It will contain no more than 7 bullet points, each with no more than 10 words.
  - Only include this section if there is at least one key takeaway.

- **Unique Sections:**
  If both Bee and Limitless data are provided, include the following. Otherwise, omit this section.
  - Denoted by `## Unique Section`.
  - Heading "#### Bee Unique Sections"
    - Bullet point list of section titles unique to bee
  - Heading "#### Limitless Unique Sections"
    - Bullet point list of section titles unique to limitless

### Final Note

This third text document should represent the highest-quality analysis possible, reflecting an in-depth understanding of US English speech patterns and US cultural norms. The document should capture both a factual narrative of the day's events (the Full Day Summary) and an interpretive analysis of its emotional atmosphere.
