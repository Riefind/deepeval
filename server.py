from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from deepeval.metrics import GEval, AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

app = FastAPI()

class TestCase(BaseModel):
    input: str
    expected_output: str
    actual_output: str


class EvalRequest(BaseModel):
    metric: str = "correctness"
    tests: List[TestCase]

@app.post("/api/evaluate")
def evaluate(req: EvalRequest):
    results = []
    for test in req.tests:
        if req.metric == "answer_relevancy":
            metric = AnswerRelevancyMetric()
        else:
            metric = GEval(
                name="Correctness",
                criteria="Determine if the 'actual_output' is correct based on the 'expected_output'.",
                evaluation_params=[
                    LLMTestCaseParams.ACTUAL_OUTPUT,
                    LLMTestCaseParams.EXPECTED_OUTPUT,
                ],
            )
        test_case = LLMTestCase(
            input=test.input,
            actual_output=test.actual_output,
            expected_output=test.expected_output,
        )
        metric.measure(test_case)
        results.append({
            "score": metric.score,
            "success": metric.success,
            "reason": metric.reason,
        })
    return {"results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
