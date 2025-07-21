import re

# Input and output file paths
input_file = "answers.txt"
output_file = "glm_answers.txt"

# Read the input file
with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract questions and answers using regex
questions = re.findall(r'问题:\s*(.+?)(?=\s*答案:|\Z)', content)
answers = re.findall(r'答案:\s*(.+?)(?=\s*问题:|\Z)', content)

# Write to output file
with open(output_file, 'w', encoding='utf-8') as f:
    for i in range(min(len(questions), len(answers))):
        f.write(f"{i+1}. {answers[i]}\n")

print(f"Output written to {output_file}")