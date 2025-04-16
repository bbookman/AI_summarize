# AI Summarize: Python Directory Reader

## Overviewgit

AI Summarize is a Python application that reads daily conversation data from two sources ("Bee" and "Limitless"), along with supplemental facts and error files, and generates a high-quality, markdown-formatted summary for each date using OpenAI. The app is highly configurable and designed for robust, automated summarization workflows.

## Features

- Reads daily data files from Bee and Limitless directories.
- Integrates supplemental facts and known errors into the analysis.
- Uses OpenAI to generate a "Best of Class" summary for each date.
- Outputs one markdown summary file per date, named as `YYYY-MM-DD.md`.
- Handles missing data gracefully (processes even if only one source is present).
- All directory paths and OpenAI settings are configurable via `config/config.json`.
- Modify analysis_prompt.md to customize the analysis prompt.

## Project Structure

```
python-directory-reader
├── src/
│   ├── main.py
│   ├── config.py
│   ├── directory_reader.py
│   ├── services/
│   │   └── summarizer.py
│   ├── templates/
│   │   └── analysis_prompt.md
│   └── utils/
│       ├── file_handler.py
│       └── openai_handler.py
├── config/
│   └── config.json
├── tests/
│   ├── test_directory_reader.py
│   └── test_file_handler.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Edit `config/config.json` to set your data directories and OpenAI API key.

## Usage

Run the summarizer with:

```
python src/main.py
```

Summaries will be saved in the directory specified by `OUTPUT_DIR` in your config.

Ensure that the `directories.json` file is properly configured with the correct paths for the directories you wish to read from.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License.
