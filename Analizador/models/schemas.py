from pydantic import BaseModel

class CodeInput(BaseModel):
    code: str

class AnalysisResult(BaseModel):
    complexity: float
    maintainability: float
