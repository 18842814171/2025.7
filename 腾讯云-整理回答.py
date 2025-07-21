import re

# Input and output file paths
input_file = "aliyun/ALIYUN7.18.txt"
output_file = "combined_answers.txt"

# Read the input file
with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract answers starting with "A:"
answers = re.findall(r'A:\s*(.+?)(?=\s*问题|\Z)', content)

# Write to output file
with open(output_file, 'w', encoding='utf-8') as f:
    for i, answer in enumerate(answers, 1):
        f.write(f"{i}. {answer}\n")

print(f"Output written to {output_file}")