from pydantic import BaseModel, Field,ConfigDict


class CommandResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )
    command: str = Field(
        description="The single terminal command to execute."
    )

    explanation: str = Field(
        description="A concise explanation of what the command does."
    )

class ExecutionResult(BaseModel):
    stdout: str
    stderr: str
    return_code: int