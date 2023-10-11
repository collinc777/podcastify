from functools import lru_cache
from typing import Annotated, Union, Literal
from pydantic import BaseModel

from fastapi import Depends, FastAPI

from backend.settings import Settings


@lru_cache()
def get_settings():
    return Settings()  # type: ignore


app = FastAPI()


class ScriptLine(BaseModel):
    speaker: Literal["Rachel", "John"]


class Script(BaseModel):
    script_lines: list[ScriptLine]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/generate_script")
async def generate_script(
    html: str, settings: Annotated[Settings, Depends(get_settings)]
):
    from trafilatura import extract
    import instructor
    import openai

    # get environment variable
    openai.api_key = settings.openai_api_key

    instructor.patch()
    article_text = extract(html)

    script: Script = await openai.ChatCompletion.acreate(
        model="gpt-4",
        response_model=Script,
        messages=[
            {
                "role": "user",
                "content": f"You are a podcast writer. Convert blog posts into NPR-style podcast transcripts with 2 speakers: Rachel and Jack. YOU ONLY OUTPUT VALID JSON. Use the given format to extract information from the following input: {article_text}",
            }
        ],
    )
    return script
