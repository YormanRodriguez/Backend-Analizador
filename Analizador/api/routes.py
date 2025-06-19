from fastapi import APIRouter
from Analizador.models.schemas import CodeInput, AnalysisResult
from Analizador.services.analyzer import analyze_code

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResult)
def analyze(input: CodeInput):
    return analyze_code(input.code)
