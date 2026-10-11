
import contextlib
import io
import re
import tempfile
from pathlib import Path

import streamlit as st

import auto_caption_generator as captioner


st.set_page_config(
    page_title="AI Subtitle Generator",
    page_icon="🎬",
    layout="centered",
)

st.title("🎬 AI Subtitle Generator")
st.write(
    "Upload an audio or video file, generate subtitles, "
    "and download your SRT file."
)

st.divider()

# Check API configuration
if not captioner.GROQ_API_KEY:
    st.error(
        "Groq API key not found. Add GROQ_API_KEY to your .env file."
    )
    st.stop()

if not captioner.shutil.which(captioner.FFMPEG):
    st.error("FFmpeg was not found. Install FFmpeg and add it to PATH.")
    st.stop()

if not captioner.shutil.which(captioner.FFPROBE):
    st.error("FFprobe was not found. Install FFmpeg and add it to PATH.")
    st.stop()


# Upload audio or video
supported_extensions = sorted(
    ext.lstrip(".") for ext in captioner.MEDIA_EXTENSIONS
)

uploaded_file = st.file_uploader(
    "Upload your audio or video file",
    type=supported_extensions,
)

# Language settings
language_names = captioner.LANGUAGE_NAMES

source_options = captioner.SOURCE_OPTIONS
target_options = captioner.TARGET_OPTIONS

source_lang = st.selectbox(
    "Spoken language",
    options=source_options,
    format_func=lambda code: language_names.get(code, code),
    index=source_options.index(captioner.DEFAULT_SOURCE_LANG)
    if captioner.DEFAULT_SOURCE_LANG in source_options
    else 0,
)

target_lang = st.selectbox(
    "Subtitle language",
    options=target_options,
    format_func=lambda code: language_names.get(code, code),
    index=target_options.index(captioner.DEFAULT_TARGET_LANG)
    if captioner.DEFAULT_TARGET_LANG in target_options
    else 0,
)

custom_prompt = st.text_area(
    "Optional instructions",
    placeholder="Example: Pay attention to names and mixed languages.",
)

st.caption(
    "Subtitles are generated using your existing Groq-hosted "
    "Whisper and language-processing pipeline."
)

if st.button("Generate subtitles", type="primary", use_container_width=True):
    if uploaded_file is None:
        st.warning("Please upload an audio or video file first.")
        st.stop()

    captioner.CUSTOM_PROMPT = (
        custom_prompt.strip()
        or captioner.os.getenv("CUSTOM_PROMPT", "")
    )

    progress_log = io.StringIO()

    try:
        with st.spinner("Generating subtitles... This may take a while."):
            with tempfile.TemporaryDirectory(
                prefix="subtitle_generator_"
            ) as temp_folder:

                temp_dir = Path(temp_folder)
                input_path = temp_dir / Path(uploaded_file.name).name

                input_path.write_bytes(uploaded_file.getvalue())

                # Reuse the existing transcription pipeline.
                with contextlib.redirect_stdout(progress_log):
                    captioner.process_video(
                        input_path,
                        downloaded_from_drive=False,
                        source_lang=source_lang,
                        target_lang=target_lang,
                    )

                logs = progress_log.getvalue()

                # The existing function prints the paths of generated SRTs.
                output_paths = re.findall(
                    r"Subtitle file\s*:\s*(.+?\.srt)",
                    logs,
                )

                if not output_paths:
                    raise RuntimeError(
                        "No subtitle file was generated. "
                        "Check the processing logs below."
                    )

                # The last path is the final output, after any conversion.
                subtitle_path = Path(output_paths[-1].strip())

                if not subtitle_path.is_file():
                    raise RuntimeError(
                        "The generated subtitle file could not be found."
                    )

                subtitle_bytes = subtitle_path.read_bytes()
                subtitle_name = subtitle_path.name

        st.success("Subtitles generated successfully!")

        st.download_button(
            label="⬇️ Download subtitles (.srt)",
            data=subtitle_bytes,
            file_name=subtitle_name,
            mime="application/x-subrip",
            use_container_width=True,
        )

        with st.expander("Preview subtitles"):
            st.code(
                subtitle_bytes.decode("utf-8-sig"),
                language="text",
            )

        with st.expander("Processing logs"):
            st.text(logs[-10000:] or "No logs available.")

    except Exception as error:
        st.error(f"Subtitle generation failed: {error}")

        with st.expander("Error details"):
            st.text(progress_log.getvalue()[-10000:])
