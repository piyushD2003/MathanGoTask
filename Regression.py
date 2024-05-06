import re
import json

def extract_question_numbers(file_path):
    question= []
    with open(file_path, 'r') as file:
        solutions = []
        options = []
        answers = []

        data = file.read()

        num =1

        matches = re.findall(r'Question ID: (\d+)', data)

        pattern = r"Question ID: (\d+).*?\n(.*?)\n\n"
        matches1 = re.findall(pattern, data, re.DOTALL)

        pattern = r'Sol\. (.+?)(?=\n\n)'
        matches2 = re.findall(pattern, data, re.DOTALL)

        for match in matches2:
            solution_text = match.strip()
            solutions.append(solution_text)


        num_questions = len(re.findall(r'Question ID: (\d+)', data))
        if len(solutions) < num_questions:
            missing_solutions = num_questions - len(solutions)
            solutions.extend([""] * missing_solutions)


        answer_pattern = re.compile(r'Question ID: \d+.*?Answer \((.)\)', re.DOTALL)
        answers = answer_pattern.findall(data)
        print(answers)
        option_pattern = re.compile(r'\((.)\)\s(.+?)(?=\s\(|$)')


        lines = data.strip().split('\n')
        
        current_options = []
        option_counter = 0
        answers_counter = 0
        for line in lines:
            
            option_match = option_pattern.match(line)
            if option_match:
                print(answers[option_counter],option_match.group(1))
                current_options.append({"optionNumber":option_counter,"optionText":option_match.group(2),"Iscorrect":answers[answers_counter]==option_match.group(1)})
                option_counter +=1
                if len(current_options) == 4:
                    options.append(current_options)
                    option_counter = 0
                    answers_counter +=1
                    current_options = []
            
        for match,match1,solution_text,option in zip(matches,matches1,solutions,options):
            question_text = match1[1].strip()
            question_text = re.sub(r'\([A-D]\)', '', question_text)
            question.append({"questionNumber": num,"questionID": int(match), "questionText":question_text,"option":option, "solutionText":solution_text})
            num = num+1
    return question

def generate_json_file(question_numbers, output_file_path):
    with open(output_file_path, 'w') as output_file:
        json.dump(question_numbers, output_file, indent=2)

def main():
    input_file_path = 'task.txt'
    output_file_path = 'questions.json'
    question = extract_question_numbers(input_file_path)
    generate_json_file(question, output_file_path)
    print("JSON file generated successfully!")

if __name__ == "__main__":
    main()