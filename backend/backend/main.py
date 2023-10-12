from functools import lru_cache
from pydub import AudioSegment
import io
from typing import Annotated, Union, Literal, Any
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, HttpUrl

from fastapi import Depends, FastAPI

from backend.settings import Settings


settings = Settings()  # type: ignore


app = FastAPI()


class ScriptLine(BaseModel):
    speaker: Literal["Rachel", "John"]
    content: str


class Script(BaseModel):
    script_lines: list[ScriptLine]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/api/generate_script")
async def generate_script(url: HttpUrl):
    print("do i get called")
    script = await _generate_script(url=url.unicode_string())
    audio = generate_audio_from_script(script=script)
    return StreamingResponse(
        audio,
        headers={"Content-Type": "audio/mpeg"},
        media_type="audio/mpeg",
    )


async def _generate_script(*, url: str):
    from trafilatura import bare_extraction, fetch_url
    import instructor
    import openai

    # get environment variable
    openai.api_key = settings.openai_api_key

    instructor.patch()
    downloaded = fetch_url(url)
    article = bare_extraction(downloaded, url=url)

    script: Script = await openai.ChatCompletion.acreate(
        model="gpt-4",
        response_model=Script,
        max_retries=2,
        messages=[
            {
                "role": "user",
                "content": f"You are a podcast writer. You convert blog posts into NPR-style podcast transcripts with 2 speakers: Rachel and Jack. Rachel and Jack have a great witty rapport. YOU ONLY OUTPUT VALID JSON. Use the given format to extract information from the following input: {article['text']}",
            }
        ],
    )
    return script


def generate_audio_from_script(
    *,
    script: Script,
):
    import boto3

    session = boto3.Session(
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        region_name="us-east-1",
    )
    client = session.client("polly")
    # silence bytes for .5 second
    for script_line in script.script_lines:
        match (script_line.speaker):
            case "Rachel":
                polly_speaker = "Joanna"
            case "John":
                polly_speaker = "Matthew"
            case _:
                raise ValueError(f"Unknown speaker: {script_line.speaker}")
        polly_result = generate_audio_bytes(
            client=client, text=script_line.content, speaker=polly_speaker
        )
        audio1 = AudioSegment.from_file(io.BytesIO(polly_result))
        silence = AudioSegment.silent(duration=500)
        final_audio: AudioSegment = audio1 + silence
        byte_io = io.BytesIO()
        final_audio.export(byte_io, format="mp3")
        yield byte_io.getvalue()


def generate_audio_bytes(*, client: Any, text: str, speaker: str) -> bytes:
    result = client.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId=speaker,
        TextType="text",
    )
    polly_result = result["AudioStream"].read()
    return polly_result
