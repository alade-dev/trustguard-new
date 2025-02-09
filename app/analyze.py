import os
import re
import json
from pydantic import BaseModel, Field
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser

# Define vulnerability patterns and fixes (unchanged)
VULNERABILITY_PATTERNS = {
    "Overflow": {
        "patterns": ["uint", "+", "-", "*", "/"],
        "fixes": [
            "Use SafeMath library for arithmetic operations",
            "Add require() statements to check bounds before operations",
            "Consider using OpenZeppelin's SafeMath implementation"
        ]
    },
    "Reentrancy": {
        "patterns": ["transfer", "send", "call.value"],
        "fixes": [
            "Implement checks-effects-interactions pattern",
            "Use ReentrancyGuard from OpenZeppelin",
            "Update state variables before external calls",
            "Consider using transfer() instead of call.value()"
        ]
    },
    "Frontrunning": {
        "patterns": ["block.timestamp", "now", "blockhash"],
        "fixes": [
            "Implement commit-reveal schemes",
            "Use block.number instead of block.timestamp where possible",
            "Add minimum and maximum bounds for timing-sensitive operations"
        ]
    },
    "Unauthorized Access": {
        "patterns": ["selfdestruct", "delegatecall", "public", "external"],
        "fixes": [
            "Implement proper access control using modifiers",
            "Use OpenZeppelin's Ownable contract",
            "Add explicit function visibility modifiers",
            "Implement multi-signature requirements for critical functions"
        ]
    },
    "Gas Efficiency": {
        "patterns": ["array", "mapping", "struct", "loop"],
        "fixes": [
            "Use fixed size arrays when possible",
            "Optimize storage usage by packing variables",
            "Avoid unnecessary loops and complex computations",
            "Consider using events instead of storage for historical data"
        ]
    },
    "Self-Destruct": {
        "patterns": ["selfdestruct", "suicide"],
        "fixes": [
            "Remove selfdestruct if not absolutely necessary",
            "Implement time-locks for destructible contracts",
            "Add multi-signature requirements for self-destruct",
            "Consider making contract non-destructible"
        ]
    }
}

# Prompt template for vulnerability analysis
template = """You are a professional smart contract reviewer. You are provided with a smart contract code below.
Identify the most critical vulnerability in the contract from the following categories:
Overflow, Reentrancy, Frontrunning, Unauthorized Access, Gas Efficiency, Self-Destruct.
For the identified vulnerability, provide a list of recommended fixes.
Return a JSON object that follows this format:
{format_instructions}

# Vulnerability patterns and fixes
VULNERABILITY_PATTERNS = {vulnerability_patterns}

<smart contract>
{smart_contract}
</smart contract>
"""

class SCParser(BaseModel):
    """
    Pydantic model for parsing smart contract vulnerability analysis results.
    """
    category: str = Field(
        ..., 
        description="The category the issue belongs to. One of: Overflow, Reentrancy, Frontrunning, Unauthorized Access, Gas Efficiency, Self-Destruct."
    )
    fixes: list = Field(
        ..., 
        description="List of suggested fixes for the identified vulnerability."
    )

def is_smart_contract(code: str) -> bool:
    """
    Validate if the uploaded file looks like a smart contract.
    """
    solidity_indicators = [
        r'\bcontract\b',
        r'\bfunction\b',
        r'\bpublic\b',
        r'\bprivate\b',
        r'\bview\b',
        r'\bpure\b',
        r'\breturns\b',
        r'\baddress\b',
        r'\buint\b',
        r'\bstruct\b',
        r'\bmodifier\b',
        r'\bevent\b'
    ]
    indicators_found = sum(1 for pattern in solidity_indicators if re.search(pattern, code))
    return indicators_found >= 3

def analyze_smart_contract(smart_contract_text: str) -> dict:
    """
    Analyzes a smart contract for vulnerabilities using the Google Generative AI model.
    """
    parser = PydanticOutputParser(pydantic_object=SCParser)
    llm = GoogleGenerativeAI(model="gemini-1.5-flash", api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))
    prompt = PromptTemplate(
        template=template,
        input_variables=["smart_contract", "vulnerability_patterns"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    chain = prompt | llm | parser
    output = chain.invoke({
        "smart_contract": smart_contract_text,
        "vulnerability_patterns": json.dumps(VULNERABILITY_PATTERNS, indent=2)
    })
    return output.model_dump()

def generate_fixed_contract(smart_contract_text: str, analysis_result: dict) -> str:
    """
    Generates a fixed version of the smart contract code based on the identified vulnerability.
    """
    category = analysis_result.get("category", "General")
    fixed_template = f"""You are a professional smart contract developer. A smart contract has been identified to have a vulnerability in the category "{category}". The original contract is provided below.

<smart contract>
{{smart_contract}}
</smart contract>

Please produce a corrected version of this smart contract that addresses the identified vulnerability using best practices for {category}. Output only the fixed contract code.
"""
    prompt = PromptTemplate(
         template=fixed_template,
         input_variables=["smart_contract"]
    )
    llm = GoogleGenerativeAI(model="gemini-1.5-flash", api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))
    chain = prompt | llm
    # Invoke the chain with the original contract text to get the fixed version.
    fixed_code = chain.invoke({"smart_contract": smart_contract_text})
    # Debug output: print the fixed code (or an error message if empty)
    if not fixed_code:
        fixed_code = "Error: No fixed code generated. Please check the prompt or the Gemini model."
    print("DEBUG: Fixed code:", fixed_code)
    return fixed_code

if __name__ == "__main__":
    # Example usage for testing
    smart_contract_text = "contract Example { uint public value; }"
    result = analyze_smart_contract(smart_contract_text)
    fixed = generate_fixed_contract(smart_contract_text, result)
    # print("Analysis result:", result)
    # print("Fixed contract:", fixed)
