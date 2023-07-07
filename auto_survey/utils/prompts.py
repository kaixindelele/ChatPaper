import logging
from langchain import PromptTemplate
import os, json
log = logging.getLogger(__name__)
keywords_system_prompt_str = """You are an assistant designed to provide accurate and informative keywords of searching academic papers. 
The user will input the title of a paper. You need to return three to five most related fields. \n
Instructions:\n
- Assign numbers to each field to present the importance. The larger, the more important. \n
- 10 is the most important and 1 is the least important. \n
- Your response should follow the following format: {"field 1": 5, "field 2": 7, "field 3": 8, "field 4": 5}\n 
- Ensure the response can be parsed by Python json.loads"""

preliminaries_system_prompt_str = '''You are an assistant designed to propose preliminary concepts for a paper given its title and contributions. Ensure follow the following instructions:
Instruction:
- Your response should follow the JSON format.
- Your response should have the following structure: {"name of the concept":  1, {"name of the concept":  2,  ...} 
- Smaller number means the concept is more fundamental and should be introduced earlier. '''

PRELIMINARIES = preliminaries_system_prompt_str
KEYWORDS = keywords_system_prompt_str
SYSTEM = {"keywords": KEYWORDS,   "preliminaries": PRELIMINARIES}


