import json
import os

def load_quizzes(filename):
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data['quizzes']
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: The file {filename} contains invalid JSON.")
        return []

def display_welcome():

    print("\n---Welcome to the Multiple \n\tChoice Quiz App!😘😘----\n")

    print("For each question, \nselect the correct answer by entering the corresponding letter.\n")
    input("\nAre you ready? Press Enter to begin...")
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console

def run_quiz(quizzes):
    """Run the quiz and return the score."""
    score = 0
    
    for i, quiz in enumerate(quizzes, 1):
        print(f"\nQuestion {i}: {quiz['question']}")
        
        # Display options with letters (A, B, C, D)
        options = quiz['options']
        letters = ['A', 'B', 'C', 'D']
        for letter, option in zip(letters, options):
            print(f"{letter}. {option}")
        
        # Get user answer
        while True:
            user_answer = input("\nYour answer (A/B/C/D): ").upper()
            if user_answer in letters:
                break
            print("Invalid input. Please enter A, B, C, or D.")
        
        # Check if answer is correct
        correct_answer = quiz['answer']
        selected_option = options[letters.index(user_answer)]
        
        if selected_option == correct_answer:
            print("Correct! 🎉")
            score += 1
        else:
            print(f"Wrong! The correct answer is: {correct_answer}")
    
    return score

def display_results(score, total):
    """Display the quiz results."""
    print("\nQuiz completed!")
    print(f"Your score: {score} out of {total}")
    percentage = (score / total) * 100
    print(f"That's {percentage:.1f}%")
    
    if percentage == 100:
        print("Perfect score! 🌟")
    elif percentage >= 70:
        print("Well done! 👍")
    elif percentage >= 50:
        print("Not bad! 😊")
    else:
        print("Keep practicing! 💪")

def main():
    # Load quizzes from JSON file
    quizzes = load_quizzes('quizzes.json')
    if not quizzes:
        return
    
    total_questions = len(quizzes)
    
    # Display welcome message
    display_welcome()
    
    # Run the quiz
    score = run_quiz(quizzes)
    
    # Display results
    display_results(score, total_questions)

main()