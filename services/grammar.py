import language_tool_python

def correct_grammar(text):
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(text)
    corrections = [match.replacements for match in matches if match.replacements]
    return corrections
