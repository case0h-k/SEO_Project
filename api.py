from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from pipeline import run_analysis


# --------------------------------
# CREATE FASTAPI APPLICATION
# --------------------------------

app = FastAPI(
    title="Semantic Site Architecture API",
    description=(
        "API for semantic website analysis, "
        "topical clustering and internal-link analysis."
    ),
    version="1.0.0"
)


# --------------------------------
# CORS
# --------------------------------

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173"
    ],

    allow_credentials=True,

    allow_methods=[
        "*"
    ],

    allow_headers=[
        "*"
    ]
)


# --------------------------------
# REQUEST MODEL
# --------------------------------

class AnalyzeRequest(BaseModel):

    url: str = Field(
        ...,
        description="Website URL to analyze"
    )

    max_pages: int = Field(
        default=50,
        ge=1,
        le=200,
        description="Maximum number of pages to crawl"
    )


# --------------------------------
# HEALTH CHECK
# --------------------------------

@app.get(
    "/api/health"
)
def health_check():

    return {

        "status": "ok",

        "message": (
            "Semantic Site Architecture API "
            "is running."
        )

    }


# --------------------------------
# WEBSITE ANALYSIS
# --------------------------------

@app.post(
    "/api/analyze"
)
def analyze_website(
    request: AnalyzeRequest
):

    try:

        result = run_analysis(
            request.url,
            request.max_pages
        )

        return result


    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )