from fastapi import FastAPI
from pydantic import BaseModel
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

app = FastAPI()

class EvalRequest(BaseModel):
    input: str
    expected_output: str
    actual_output: str

@app.post("/api/evaluate")
def evaluate(req: EvalRequest):
    metric = GEval(
        name="Correctness",
        criteria="Determine if the 'actual_output' is correct based on the 'expected_output'.",
        evaluation_params=[
            LLMTestCaseParams.ACTUAL_OUTPUT,
            LLMTestCaseParams.EXPECTED_OUTPUT,
        ],
    )
    test_case = LLMTestCase(
        input=req.input,
        actual_output=req.actual_output,
        expected_output=req.expected_output,
    )
    metric.measure(test_case)
    return {
        "score": metric.score,
        "success": metric.success,
        "reason": metric.reason,
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
