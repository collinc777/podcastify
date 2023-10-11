from typing import Union, Literal
from pydantic import BaseModel

from fastapi import FastAPI

from backend.settings import init_settings

init_settings()
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
async def generate_script(html: str):
    from trafilatura import extract
    import instructor
    import openai

    instructor.patch()
    article_text = extract(html)

    script: Script = await openai.ChatCompletion.acreate(
        model="gpt-4",
        response_model=Script,
        messages=[
            {
                "role": "human",
                "content": f"You are a podcast writer. Convert blog posts into NPR-style podcast transcripts with 2 speakers: Rachel and Jack. YOU ONLY OUTPUT VALID JSON. Use the given format to extract information from the following input: {article_text}",
            }
        ],
    )
    return script
