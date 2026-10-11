# AI-Powered Subtitle Generation

Generate subtitle files (`.srt`) from audio and video using Groq's
hosted Whisper API. The script can process a local media file, a folder
of media files, or a Google Drive file/folder link.

## Features

-   Transcribes audio using Groq's hosted Whisper API.
-   Supports automatic audio-language detection or a selected language.
-   Supports caption output in English, Hindi, Urdu, Kannada, Malayalam,
    Hinglish, or automatic English-letter output where supported by the
    script.
-   Accepts a local audio/video file, a local folder, a Google Drive
    file link/ID, or a Google Drive folder link/ID.
-   Uses FFmpeg and FFprobe to support media processing.
-   Saves generated subtitle files in the project's `output_captions/`
    folder when configured to do so.

## Requirements

-   Python 3.10 or newer is recommended.
-   A Groq API key.
-   FFmpeg and FFprobe installed and accessible on your system.
-   Internet access for API requests.
-   Access to the Google Drive file/folder if processing Drive links.

## Project structure

A typical project layout:

``` text
Subtitle_generation_using__AI/
├── auto_caption_generator.py
├── .env
├── requirements.txt
└── output_captions/
```

Your project may contain additional files. The script's startup output
displays the detected FFmpeg/FFprobe paths and output directory.

## Setup

### 1. Open the project folder

Open a terminal in the folder containing `auto_caption_generator.py`.

### 2. Create and activate a virtual environment (recommended)

**Windows PowerShell**

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the script using the
virtual environment's Python directly:

``` powershell
.\.venv\Scripts\python.exe auto_caption_generator.py
```

### 3. Install dependencies

If the project includes `requirements.txt`:

``` powershell
python -m pip install -r requirements.txt
```

If `requirements.txt` is not present, install the dependencies specified
by the project source. The script also suggests `requests-toolbelt` for
an optional live upload progress bar:

``` powershell
python -m pip install requests-toolbelt
```

`requests-toolbelt` is optional; uploads can still work without it.

### 4. Install FFmpeg

Install FFmpeg for your operating system and ensure both `ffmpeg` and
`ffprobe` are available in your system `PATH`.

Verify in PowerShell:

``` powershell
ffmpeg -version
ffprobe -version
```

If the script already prints valid full paths for FFmpeg and FFprobe at
startup, it has detected them.

### 5. Configure environment variables

Create a `.env` file in the project folder if the script uses
`python-dotenv` to load environment variables. Keep each setting on its
own line:

``` dotenv
GROQ_API_KEY=your_groq_api_key_here
GROQ_LLM_MODEL=openai/gpt-oss-120b
SOURCE_LANG=auto
TARGET_LANG=en
```

Use your actual Groq API key for `GROQ_API_KEY`. Never commit your
`.env` file or publish your API key.

The script's defaults may be used if optional language/model variables
are omitted. In the version described here, the default source language
is `auto`, and the default caption language is `hing` unless overridden
by environment variables. The startup output shows the configured model
names.

## Run the application

From the project folder:

``` powershell
python auto_caption_generator.py
```

Follow the prompts.

### Prompt guide

1.  **Audio language (what is spoken)** --- choose `auto`, `en`, `hi`,
    `ur`, `kn`, or `ml`, or press Enter to use the configured default.
2.  **Caption language (what the .srt should contain)** --- choose from
    the options displayed by the script, such as `en`, `hi`, `ur`, `kn`,
    `ml`, `hing`, or `auto`.
3.  **Custom prompt about the audio** --- optionally enter context such
    as names, technical terms, or mixed-language details. Press Enter if
    you do not need a custom prompt.
4.  **Input** --- provide a local media file, a folder, or a supported
    Google Drive file/folder link or ID when requested by the script.

Example language selections:

``` text
Audio language (what is spoken) [auto/en/hi/ur/kn/ml] (Enter = auto): auto
Caption language (what the .srt should contain) [en/hi/ur/kn/ml/hing/auto] (Enter = en): en
Custom prompt about the audio (Enter = none): 
```

The exact prompts and available options depend on the current script
configuration.

## Output

Generated subtitle files use the SubRip format (`.srt`). The intended
output folder is:

``` text
output_captions/
```

Check the script's `process_video()` function if outputs are being saved
beside local media files instead. To always save captions in
`output_captions/`, set the output directory for the SRT file to the
configured `OUTPUT_DIR` for every input source.

## Language codes

  -----------------------------------------------------------------------
  Code                                Meaning
  ----------------------------------- -----------------------------------
  `auto`                              Automatically detect the spoken
                                      language, or use the script's
                                      automatic caption mode where
                                      offered

  `en`                                English

  `hi`                                Hindi

  `ur`                                Urdu

  `kn`                                Kannada (`ka` may also be accepted
                                      as an alias)

  `ml`                                Malayalam (`ma` may also be
                                      accepted as an alias)

  `hing`                              Hinglish
  -----------------------------------------------------------------------

The script prints the supported options when it starts. Use those
displayed options if they differ from this table.

## Troubleshooting

### `ffmpeg` or `ffprobe` not found

Install FFmpeg and add its `bin` directory to `PATH`, then open a new
terminal and check:

``` powershell
ffmpeg -version
ffprobe -version
```

### Groq authentication or API errors

-   Confirm `GROQ_API_KEY` is set correctly.
-   Check that your API key is active and has access to the requested
    model/API.
-   Avoid sharing your key in screenshots, logs, GitHub, or chat
    messages.

### The language prompt shows unexpected text

Check the `.env` file for malformed or merged values. For example, keep
these on separate lines:

``` dotenv
SOURCE_LANG=auto
GROQ_LLM_MODEL=openai/gpt-oss-120b
```

Do not combine the language value and model name on the same line.

### No subtitle file appears

-   Check the terminal for transcription or processing errors.
-   Confirm the input file is supported and readable.
-   Check the output directory printed when the script starts.
-   Confirm the output folder is writable.
-   If needed, inspect the output path assignment in `process_video()`.

### Google Drive input fails

-   Verify the link or ID is correct.
-   Ensure the file/folder is accessible to the account or method used
    by the script.
-   Check whether the script expects a share link, file ID, or folder
    ID.

## Security notes

-   Keep API keys in `.env` or another secure environment-variable
    mechanism.
-   Add `.env` and `.venv/` to `.gitignore`.
-   Do not upload private audio/video or generated transcripts to public
    repositories without permission.
-   Review generated captions before publishing; automatic transcription
    can make mistakes.

Suggested `.gitignore` entries:

``` gitignore
.env
.venv/
__pycache__/
output_captions/
```

## Limitations

-   Transcription requires API connectivity and may be subject to model
    availability, request limits, file-size limits, and usage costs.
-   Accuracy depends on audio quality, accents, background noise, and
    language mixing.
-   The exact supported formats, model options, and Google Drive
    behavior depend on the implementation in
    `auto_caption_generator.py`.

## License

Add the license applicable to your project before distributing it
publicly.
