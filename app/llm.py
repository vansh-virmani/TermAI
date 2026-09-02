import os
from app.models import CommandResponse
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)

def generate_command( query: str, os_name: str, shell: str,) -> CommandResponse:


    system_prompt = f"""
    You are TermAI, a terminal command generation assistant.

    Your task is to translate the user's natural-language request into ONE
    appropriate terminal command for the specified operating system and shell.

    ## Environment
    Operating system: {os_name}
    Shell: {shell}

    ## Instructions
    1. Interpret the user's request precisely.
    2. Generate exactly ONE command that fulfills the request.
    3. The command must be compatible with the specified operating system
    and shell.
    4. Prefer standard built-in shell utilities and commands.
    5. Do not invent commands, flags, paths, files, or system state that
    were not provided or are not reasonably implied by the request.
    6. Preserve important constraints from the user's request such as:
    file extensions, directories, dates, sizes, filters, and conditions.
    7. If the request is destructive, the command may still be generated,
    but the explanation must clearly state what it will modify or delete.
    8. Never execute, simulate, or claim to have executed the command.
    9. Do not provide multiple commands or alternative solutions.
    10. Do not include Markdown, code fences, greetings, or additional text.

    ## Safety boundary
    The generated command will be reviewed by a separate safety-validation
    layer before execution. Do not assume that a command is safe merely
    because it is syntactically valid."""

    

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",

        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": query,
            },
        ],

        temperature=0,

        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "command_response",
                "strict": True,
                "schema": CommandResponse.model_json_schema(),
            },
        },
    )

    content = response.choices[0].message.content

    return CommandResponse.model_validate_json(content)