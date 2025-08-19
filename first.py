import json
import os
from time import sleep

def load_questions(filename):

    try:
        with open(filename, 'r') as file:
            questions = json.load(file)
        return questions
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file '{filename}' contains invalid JSON.")
        return None

def display_question(question, question_number, total_questions):

    print(f"\nQuestion {question_number}/{total_questions}")
    print("=" * 30)
    print(question["question"])
    print("-" * 30)
    
    for option, text in question["options"].items():
        print(f"{option}. {text}")

def get_user_answer():
    
    while True:
        answer = input("\nYour answer (A/B/C/D) or Q to quit: ").upper()
        if answer in ['A', 'B', 'C', 'D', 'Q']:
            return answer
        print("Invalid input. Please enter A, B, C, D, or Q to quit.")

def run_quiz(questions):

    score = 0
    total_questions = len(questions)
    
    print("\n-----Welcome to the Quiz App!------\n")
    print(f"There are {total_questions} questions in this quiz.")
    print("Press Enter to begin...", end="")
    input()
    
    for i, question in enumerate(questions, 1):
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear screen
        display_question(question, i, total_questions)
        user_answer = get_user_answer()
        
        if user_answer == 'Q':
            print("\nQuiz aborted.")
            return
        
        if user_answer == question["answer"]:
            print("\n✅ Correct!")
            score += 1
        else:
            print(f"\n❌ Incorrect! The correct answer is {question['answer']}.")
        
        print(f"Explanation: {question.get('explanation', 'No explanation provided.')}")
        sleep(3)  
    
   
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\nQuiz Completed!")
    print("=" * 30)
    print(f"Your final score: {score}/{total_questions}")
    print(f"Percentage: {(score/total_questions)*100:.1f}%")
    
    if score == total_questions:
        print("Perfect score! 🎉")
    elif score/total_questions >= 0.7:
        print("Well done! 👍")
    elif score/total_questions >= 0.5:
        print("Not bad! 😊")
    else:
        print("Keep practicing! 📚")

def main():

    filename = "quizzes.json"
    questions = load_questions(filename)
    
    if questions:
        run_quiz(questions)
    
    print("\nThank you for particiating!")

main()