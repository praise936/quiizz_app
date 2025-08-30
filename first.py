import json
import os
import time

def delete_quiz():
    department = select_dep()
    filename = f'{department}.json'
    try:
        with open(filename,'r') as file:
            results = json.load(file)
        
        for i,quiz in enumerate(results['quizzes'],1):
            print(f"{i}: {quiz['title']}")
            print("\n")
            del_list = [i for i in range(1,len(results['quizzes'])+1)]
            
            while True:
                to_delete = int(input("which quiz do you want to delete? (1,2 or 3): "))
                if to_delete in del_list:
                    del results['quizzes'][to_delete-1]
                    break
        os.remove(filename)
        with open(filename,'w') as file:
            json.dump(results,file,indent=4)
    except FileNotFoundError:
        return 'no such file exist'     
                
        
def view_result():
    with open('results.json', "r") as file:
        results = json.load(file)
    for i,result in enumerate(results['details'],1):
        print(f"name---->{result['name']}\nscore---->{result['score']}\nadmission---->{result['registration']}\n")
def create_results_file():
    results = {'details':[]}
    with open ('results.json','w') as file:
        json.dump(results,file,indent=4)
        
def store_results(score,name,adm):
    
    with open("results.json","r") as file:
        results = json.load(file)
    os.remove('results.json')
    info = {}

    info['name'] = name
    
        
    info['score'] = score
    info['registration'] = adm
    results['details'].append(info)
    with open("results.json","w") as file:
        json.dump(results,file,indent=4)
    
def select_dep():
    departments = ['CPE','MPE','CSC','TLE']
    for i, dep in enumerate(departments, 1):
        print(f"{i}:{dep}")
    dept_num = ['1','2','3','4']
    while True:
        dept = input("select 1,2,3 or 4: ")
        if dept in dept_num:
            break
        print("invalid department entered kindly selct between 1-4: ")
        
    selected_dept = departments[dept_num.index(dept)]
        
            
    return selected_dept
def load_quizzes(filename):

    try:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        print(f"Error: The file {filename} contains invalid JSON.")
        return {"quizzes": []}

def save_quizzes(filename, data):
    """Save quizzes to a JSON file."""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def display_welcome():
    """Display welcome message."""
    print("Welcome to the Multiple Choice Quiz App!")
    print("=" * 50)

def menu():
    """Ask user to select between taking or creating a quiz."""
    print("\nWhat would you like to do?")
    print("1. Take a quiz")
    print("2. Create a new quiz")
    print("3. view results")
    print("4. delete some quiz")
    print("5. exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ")
        if choice in ['1', '2', '3','4']:
            return choice
        print("Invalid input. Please enter 1, 2, or 3.")

def select_quiz(quizzes):
    """Allow user to select a quiz to take."""
    if quizzes == None:
        print("No quizzes available.\n")
        return None
    
    print("\nAvailable Quizzes:")
    for i, quiz in enumerate(quizzes, 1):
        print(f"{i}. {quiz['title']} ({len(quiz['questions'])} questions)")
    
    while True:
        try:
            choice = int(input(f"\nSelect a quiz (1-{len(quizzes)}): "))
            if 1 <= choice <= len(quizzes):
                return quizzes[choice - 1]
            print(f"Please enter a number between 1 and {len(quizzes)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def run_quiz(quiz):
    """Run the selected quiz and return the score."""
    score = 0
    questions = quiz['questions']
    
    print(f"\nStarting quiz: {quiz['title']}")
    print(f"Number of questions: {len(questions)}")
    input("Press Enter to begin...")
    os.system('cls' if os.name == 'nt' else 'clear')
    
    for i, question in enumerate(questions, 1):
        print(f"\nQuestion {i}: {question['question']}")
        
        # Display options with letters (A, B, C, D)
        options = question['options']
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
        correct_answer = question['answer']
        selected_option = options[letters.index(user_answer)]
        
        if selected_option == correct_answer:
            print("Correct! 🎉")
            score += 1
        else:
            print(f"Wrong! The correct answer is: {correct_answer}")
    
    return score, len(questions)

def create_quiz(selected_dept):
    
    filename = f'{selected_dept}.json'
    
    # Load existing quizzes or create new structure
    try:
        with open(filename, 'r') as file:
            department_quiz = json.load(file)
    except FileNotFoundError:
        department_quiz = {"quizzes": []}
        
    print("\nLet's create a new quiz!")
    
    # Get quiz title
    while True:
        title = input("Enter quiz title: ").strip()
        if title:
            break
        print("Title cannot be empty.")
    
    # Check if title already exists
    for quiz in department_quiz['quizzes']:
        if quiz['title'].lower() == title.lower():
            print("A quiz with this title already exists.")
            return selected_dept
    
    # Initialize questions list
    questions = []
    
    # Add questions
    print("\nNow let's add questions to your quiz.")
    while True:
        question = {}
        
        # Get question text
        while True:
            question_text = input("\nEnter question: ").strip()
            if question_text:
                question['question'] = question_text
                break
            print("Question cannot be empty.")
        
        # Get options
        options = []
        letters = ['A', 'B', 'C', 'D']
        for letter in letters:
            while True:
                option = input(f"Enter option {letter}: ").strip()
                if option:
                    options.append(option)
                    break
                print("Option cannot be empty.")
        
        question['options'] = options
        
        # Get correct answer
        while True:
            correct_answer = input("Enter the correct answer (A/B/C/D): ").upper()
            if correct_answer in letters:
                question['answer'] = options[letters.index(correct_answer)]
                break
            print("Invalid input. Please enter A, B, C, or D.")
        
        # Add question to questions list
        questions.append(question)
        
        # Ask if user wants to add another question
        while True:
            another = input("\nAdd another question? (y/n): ").lower()
            if another in ['y', 'n']:
                break
            print("Please enter 'y' or 'n'.")
        
        if another == 'n':
            break
    
    # Create the quiz object
    new_quiz = {
        "title": title,
        "questions": questions
    }
    
    # Add to data
    department_quiz['quizzes'].append(new_quiz)
    
    print(f"\nQuiz '{title}' created successfully with {len(questions)} questions!")
    return department_quiz

def display_results(score, total):
    """Display the quiz results."""
    print("\n" + "=" * 50)
    print("Quiz completed!")
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
    print("=" * 50)
    return percentage
def validate():
    while True:
        name = input("Enter your name...")
        if name:
            break
        print("invalid name enter kindly enter your name...\n")
    while True:
        adm = input("Enter your reg no...")
        if adm:
            break
        print("invalid registration number entered\n")
    return name,adm
def nextStep():
    print("select the department you want it's quiz"+ "-"*40)
    depart = select_dep()
    filename = f"{depart}.json"
    
    try:
        data = load_quizzes(filename)
        
        quiz = select_quiz(data['quizzes'])
        
    except TypeError:
        return None
    return quiz
def already_did(adm):
    try:
        with open('results.json','r') as file:
            results = json.load(file)
        if results['details']:
            for i,detail in enumerate(results['details'],1):
                if detail['registration'] == adm:
                    return 'done'
                else:
                    return 'good'
        return 'first'
    except FileNotFoundError:
        return 'error'

    
def sub_main():
    while True:
        
        while True:
            print("\nThere are two personel here\n1. lecturer\n2. student")
            position = input("\nyou are entering as...").strip()
            if position == "1" or position == "2":
                break
            print("please select 1 or 2")
        mode = menu()
        if (position == '1' and mode == '1' ):
            while True:
                name = input("Enter the name...").strip()
                if name:
                    break
                print("name cannot be empty\n")
            adm = 'lecturer'
            try:
                with open('results.json','r') as file:
                    result = json.load(file)
            except FileNotFoundError:
                create_results_file()
            quiz = nextStep()
            if quiz == None:
                print("wait for lecturer to add a quiz\n")
            else:    
                score, total = run_quiz(quiz)
                score = display_results(score, total)
                store_results(score,name,adm)
        
        elif(position == '2' and mode == '1'):  # Take a quiz
            name,adm = validate()
            
            status = already_did(adm)
            if status == 'error':
                create_results_file()
                quiz = nextStep()
                
                if quiz == None:
                    print("wait for lecturer to add a quiz\n")
                else:    
                    score, total = run_quiz(quiz)
                    score = display_results(score, total)
                    store_results(score,name,adm)
                
            elif status == 'done':
                print("\n⚠️ ⚠️  you already did the quiz\n")
            elif status == 'good' or status == 'first':
                quiz = nextStep()
                if quiz == None:
                    print("wait for lecturer to add a quiz\n")
                else:    
                    score, total = run_quiz(quiz)
                    score = display_results(score, total)
                    store_results(score,name,adm)

                
                
                
            
            

        elif (mode == '2'and position == '1'):  # Create a quiz
            selected_dept = select_dep()
            data = create_quiz(selected_dept)
            filename = f"{selected_dept}.json"
            save_quizzes(filename, data)
        
        elif (mode == '2' and position == '2'):
            print("  !!only lecturer can create quizes  \n\tchoose again\n")
            sub_main()
        elif mode == "3":
            os.system('cls'if os.name == 'nt'else 'clear')
            print("--------RESULTS-----------\n")
            view_result()
            print("press Q to quit...")
            print("\nany other key pressed will take you home")
            quit = input().upper()
            
            if quit== 'Q':
                os.system('cls'if os.name == 'nt'else 'clear')
                print("Thank you for using the Quiz App. Goodbye!\n")
                j = 'l'
                
            else:
                os.system('cls'if os.name == 'nt'else 'clear')
                sub_main()
        elif mode == '4'and position == '1':  # Exit
            deleted = delete_quiz()
            if deleted == None:
                print("deleted successfully")
            else:
                print("the department has no questions")
        elif mode == '4'and position == '2':
            print("\nonly lecturers can delete a quiz\n")
        if mode != '3':
            input("\nPress Enter to continue...")
            os.system('cls' if os.name == 'nt' else 'clear')
            display_welcome()
def main():

    display_welcome()
    sub_main()

main()