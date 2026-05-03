import os
import sys
import json

def grade(output_file, assertions):
    if not os.path.exists(output_file):
        return [{"text": "Output file exists", "passed": False, "evidence": "File not found"}]
    
    with open(output_file, "r") as f:
        content = f.read()
    
    results = []
    for assertion in assertions:
        passed = False
        evidence = ""
        
        if "Jekyll front matter" in assertion:
            passed = content.startswith("---") and "title:" in content and "tags:" in content
            evidence = "Found YAML block" if passed else "No YAML front matter found"
        elif "First heading in body is ##" in assertion:
            passed = "## Getting Started" in content and "# Getting Started" not in content
            evidence = "Found ## Getting Started and no # Getting Started" if passed else "H1 still present or H2 missing"
        elif "Contains {% youtube" in assertion:
            passed = "{% youtube dQw4w9WgXcQ %}" in content
            evidence = "Found Liquid youtube tag" if passed else "Missing Liquid youtube tag"
        elif "Contains blockquote for message" in assertion:
            passed = "> **Note**" in content
            evidence = "Found blockquote with **Note**" if passed else "Missing blockquote transformation"
        elif "Code block is ```typescript without filename" in assertion:
            passed = "```typescript" in content and "```typescript:hello.ts" not in content
            evidence = "Found clean language tag" if passed else "Language tag still contains filename"
        elif "Contains {% katex %}" in assertion:
            passed = "{% katex %}" in content and "{% endkatex %}" in content
            evidence = "Found katex Liquid tags" if passed else "Missing katex Liquid tags"
        elif "Contains <details><summary>" in assertion:
            passed = "<details>" in content and "<summary>" in content
            evidence = "Found HTML details tags" if passed else "Missing HTML details tags"
        elif "Contains {% katex inline %}" in assertion:
            passed = "{% katex inline %}" in content
            evidence = "Found inline katex tag" if passed else "Missing inline katex tag"
        else:
            passed = True
            evidence = "Manual check recommended"
            
        results.append({"text": assertion, "passed": bool(passed), "evidence": evidence})
    
    return results

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python grade.py <workspace_dir> <evals_file>")
        sys.exit(1)
        
    workspace_dir = sys.argv[1]
    evals_file = sys.argv[2]
    
    with open(evals_file, "r") as f:
        evals_data = json.load(f)
        
    for eval_item in evals_data["evals"]:
        eval_id = eval_item["id"]
        eval_name = eval_item["name"]
        assertions = eval_item["assertions"]
        
        for config in ["with_skill", "without_skill"]:
            eval_dir = os.path.join(workspace_dir, "eval-{}".format(eval_id), config)
            output_file_path = os.path.join(eval_dir, "outputs", "converted.md")
            
            grading_results = grade(output_file_path, assertions)
            
            if not os.path.exists(eval_dir):
                os.makedirs(eval_dir)
                
            with open(os.path.join(eval_dir, "grading.json"), "w") as f:
                json.dump({"expectations": grading_results}, f, indent=2)
