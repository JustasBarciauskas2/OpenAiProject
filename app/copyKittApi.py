from fastapi import FastAPI, HTTPException
from copyKitt import generateBrandingSnippet, generateKeywords
from mangum import Mangum

app = FastAPI()
handler = Mangum(app)

MAX_INPUT_LENGTH = 32


@app.get("/generate_snippet")
async def generateSnippetApi(prompt: str):
    validateInputLength(prompt)
    snippet = generateBrandingSnippet(prompt)
    return {"snippet": snippet, "keywords": []}


@app.get("/generate_keyword")
async def generateKeywordApi(prompt: str):
    validateInputLength(prompt)
    keywords = generateKeywords(prompt)
    return {"snippet": None, "keywords": keywords}


@app.get("/generate_snippet_and_keyword")
async def generateKeywordApi(prompt: str):
    validateInputLength(prompt)
    snippet = generateBrandingSnippet(prompt)
    keywords = generateKeywords(prompt)
    return {"snippet": snippet, "keywords": keywords}


def validateInputLength(prompt: str):
    if len(prompt) >= MAX_INPUT_LENGTH:
        raise HTTPException(
            status_code=404, detail=f"Input length is too long. Must be under {MAX_INPUT_LENGTH} characters.")
