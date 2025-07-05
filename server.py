from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import re

from deepeval.metrics import GEval, AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

app = FastAPI()


def sensitive_data_guardrail(text: str) -> bool:
    """Check for phone numbers or the word 'password' in the output."""
    phone_regex = re.compile(r"\b(?:\d{3}[- ]?){2}\d{4}\b")
    if phone_regex.search(text):
        return True
    if "password" in text.lower():
        return True
    return False

class TestCase(BaseModel):
    input: str
    expected_output: str
    actual_output: str


class EvalRequest(BaseModel):
    metric: str = "correctness"
    guardrails: bool = False
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
        guardrail_triggered = False
        if req.guardrails:
            guardrail_triggered = sensitive_data_guardrail(test.actual_output)
        results.append({
            "score": metric.score,
            "success": metric.success,
            "reason": metric.reason,
            "guardrail_triggered": guardrail_triggered,
        })
    return {"results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
