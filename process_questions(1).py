import re

def process_questions(input_file, output_file):
    try:
        # Read the input file
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()

        # Split the text into question blocks, keeping empty questions
        questions = re.split(r'\n\s*Q\s*\d+:\s*\n', text)
        #questions = re.split(r'\n\s*问题\s*\d+:\s*\n', text)
        questions = [q.strip() for q in questions if q.strip() or q == '']  # Keep empty questions

        # Initialize output lines
        output_lines = []

        # Process each question block
        for i, question_text in enumerate(questions, 1):
            # Handle empty question blocks
            if not question_text.strip():
                output_lines.append(f"问题{i}")
                #output_lines.append(f"Question {i}:")
                continue

            # Clean up the question text by removing extra newlines and spaces
            cleaned_text = ' '.join(question_text.split())
            
            # Skip problematic questions (e.g., Question 33 with error message)
            if "未能成功完成" in cleaned_text:
                output_lines.append(f"Question {i}: No valid answer available.")
                continue

            # Replace "需更多信息吗？" or similar phrases with a period for cleaner output
            cleaned_text = re.sub(r'需更多信息吗？|还有其他问题(想了解|吗)？', '.', cleaned_text)
            
            # Format the answer as a single line
            answer = f"{i} :{cleaned_text}"
            #answer = f"Question {i}: {cleaned_text}"
            output_lines.append(answer)

        # Write to output file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join(output_lines))
        
        print(f"Answers written to {output_file}")

    except FileNotFoundError:
        print(f"Error: Input file {input_file} not found")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

# Example usage
if __name__ == "__main__":
    input_file = "hunyuan/HUNYUAN7.18.txt"  # Replace with your input file path
    output_file = "combined_answers.txt"  # Replace with desired output file path
    process_questions(input_file, output_file)