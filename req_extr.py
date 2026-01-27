import time, random
import re
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from utils import clean_and_split
import time

load_dotenv()

current_words = "\n".join(clean_and_split("Reconstruction_document.txt"))

prompt = """
[Role]
You are an expert in Model-based Systems Engineering (MBSE), aircraft assembly
process modeling, and natural language extraction. Your task is to read a free-
text engineering document describing assembly process updates and convert it 
into a clean, structured JSON summary.

[Context]
The input document may contain a description of an existing baseline process, 
OR it may contain specific instructions to ADD, MODIFY, or DELETE operations.
Your goal is to identify ONLY the delta (changes) to be applied to the model.

[Input]
You will receive a requirement document in free-text form:

------------------ BEGIN DOCUMENT ------------------
""" + current_words + """
------------------ END DOCUMENT ------------------

[Task]
Analyze the document and extract information **strictly based on the following logic**:

1. **Detection**: Scan for keywords indicating a process change, such as "New Operation", "Engineering Change Notice (ECN)", "Update", "Insert", "Modify", or "Delete".
2. **Extraction**: 
   - **IF AND ONLY IF** specific new or modified operations are explicitly defined (e.g., "A new task... is introduced"), extract their details.
   - **IF** the document only describes the existing/baseline process (e.g., "The assembly sequence commences with...", "Existing workflow..."), **DO NOT** extract these as new operations. In this case, the "operations" list must be empty.

3. **Field definitions (for extracted changes only)**:
   - operation_name: Keep exact name (e.g., "S40_02002 Cleanup").
   - duration: Integer minutes.
   - precedence: Immediate predecessor.
   - required_resources: { "Station": <int>, "Mechanical Operator": <int>, "Station platform": <int> } (or null).

4. **Optimization Goal**: Always extract the "Global Optimization Directive" or similar goal text if present, regardless of whether operations changed.

[Output format]
Return a JSON object using exactly the following structure.
**If no new/modified operations are found, the "operations" list must be empty `[]`.**

{
  "operations": [
    {
      "operation_name": "<text>",
      "duration": <int or null>,
      "Type": "<Manual/Auto>",
      "precedence": "<operation_name>" or null,
      "required_resources": {
        "Station": <int or null>,
        "Mechanical Operator": <int or null>,
        "Station platform": <int or null>
      } or null
    }
  ],
  "optimization_goal": "<text> or null"
}

[Important]
- Do NOT output chain-of-thought reasoning.
- Do NOT extract operations that are described as part of the existing/standard workflow.
- Only output the final JSON result.
"""



llm = ChatOpenAI(model="gpt-5", temperature=0) 
res = llm.invoke([HumanMessage(content=prompt)])

json_data = json.loads(res.content)
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=2, ensure_ascii=False)