import json  # enable you to use json file inbuilt functions
import os  # enable you to use terminal commands like mkdir or cls


def display_welcome():
    """Display welcome message for the quiz application."""
    print("Welcome to the Multiple Choice Quiz App!")
    print("=" * 50)


def menu():
    """
    Display main menu options and get user choice
    Returns the selected menu option
    """
    print("\nWhat would you like to do?")
    print("1. Take a quiz")
    print("2. Create a new quiz")
    print("3. view results")
    print("4. delete some quiz")
    print("5. exit")

    while True:#keep asking you until you enter the correct input
        choice = input("\nEnter your choice...: ")
        if choice in ["1", "2", "3", "4", "5"]:
            return choice
        print("Invalid input. Please enter 1, 2, 3, 4 or 5.")


def select_dep():
    """
    Display department options and get user selection
    Returns the selected department abbreviation
    """
    departments = ["CPE", "MPE", "CSC", "TLE","MIT","EC"]
    for i, dep in enumerate(departments, 1): #enumerates items in a list
        print(f"{i}:{dep}")
    dept_num = ["1", "2", "3", "4","5","6"]

    # Validate department selection
    while True:
        dept = input("select department number: ")
        if dept in dept_num:
            break
        print("invalid department entered kindly selct between 1-6: ")

    selected_dept = departments[dept_num.index(dept)]#this finds the index of the input in dept_num
                                                    #and retrieve the corresponding department with that index
    return selected_dept

def load_quizzes(filename):
    """
    Load quiz data from a JSON file
    Handles file not found and JSON decode errors
    """
    try:
        with open(filename, "r") as file:
            data = json.load(file)#stores the data from filename to a variable called data
        return data
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:#thiss is when the son format in filename is wrong
        print(f"Error: The file {filename} contains invalid JSON.")
        return {"quizzes": []}


def save_quizzes(filename, data):
    """Save quizzes to a JSON file with proper formatting."""
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def select_quiz(quizzes):
    """
    Allow user to select a quiz from available options
    Returns the selected quiz object
    """
    if quizzes == None:
        print("No quizzes available.\n")
        return None

    print("\nAvailable Quizzes:")
    for i, quiz in enumerate(quizzes, 1):
        print(f"{i}. {quiz['title']} ({len(quiz['questions'])} questions)")

    # Validate quiz selection
    while True:
        try:
            choice = int(input(f"\nSelect a quiz (1-{len(quizzes)}): "))
            if 1 <= choice <= len(quizzes):
                return quizzes[choice - 1]
            print(f"Please enter a number between 1 and {len(quizzes)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def run_quiz(quiz):
    """
    run the quiz by displaying questions and collecting answers
    Returns score and total number of questions
    """
    score = 0
    questions = quiz["questions"]

    print(f"\nStarting quiz: {quiz['title']}")
    print(f"Number of questions: {len(questions)}")
    input("Press Enter to begin...")
    os.system("cls" if os.name == "nt" else "clear")  # Clear screen

    # Iterate through each question
    for i, question in enumerate(questions, 1):
        print(f"\nQuestion {i}: {question['question']}")

        # Display options with letters (A, B, C, D)
        options = question["options"]
        letters = ["A", "B", "C", "D"]
        for letter, option in zip(letters, options):#zip(letters, options) returns a list that contain tuples ie [('A',dog),('B',cat),('C',male),]
            print(f"{letter}. {option}")

        # Get and validate user answer
        while True:
            user_answer = input("\nYour answer (A/B/C/D): ").upper()
            if user_answer in letters:
                break
            print("Invalid input. Please enter A, B, C, or D.")

        # Check if answer is correct
        correct_answer = question["answer"]
        selected_option = options[letters.index(user_answer)]#this takes the user anser goes to letters list finds the index of the answer the user has entered ie the anser must be in that list but now at which index so it gets that index and find the option at that index example if user enters A as their answer the function goes to letters list and find the ndex of A (0) then goes to options list and get the option at zero index

        if selected_option == correct_answer:
            print("Correct! 🎉")
            score += 1
        else:
            print(f"Wrong! The correct answer is: {correct_answer}")

    return score, len(questions)


def display_results(score, total):
    """
    Display quiz results with percentage and performance feedback
    Returns the percentage score
    """
    print("\n" + "=" * 50)
    print("Quiz completed!")
    print(f"Your score: {score} out of {total}")
    percentage = (score / total) * 100
    print(f"That's {percentage:.1f}%")

    # Provide performance feedback based on score
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
    """
    Validate student name and registration number input
    Returns validated name and registration
    """
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
    return name, adm


def create_results_file():
    """
    Initialize the results.json file with empty structure
    Creates the file if it doesn't exist
    """
    results = {"details": []}
    with open("results.json", "w") as file:
        json.dump(results, file, indent=4)#this is a json function that takes the variable nammed result's content and keep them inside a newly created file


def store_results(score, name, adm):
    """
    Store a student's quiz results in results.json
    Appends new result to existing data
    """
    with open("results.json", "r") as file:
        results = json.load(file)
    os.remove("results.json")  # Remove old file

    info = {}
    info["name"] = name
    info["score"] = score
    info["registration"] = adm

    results["details"].append(info)  # Add new result

    # Write updated results back to file
    with open("results.json", "w") as file:
        json.dump(results, file, indent=4)


def view_result():
    """
    Display all quiz results from results.json file
    Shows name, score, and registration number for each student
    """
    try:
        with open("results.json", "r") as file:
            results = json.load(file)
        for i, result in enumerate(results["details"], 1):
            print(
                f"name---->{result['name']}\nscore---->{result['score']}\nadmission---->{result['registration']}\n"
            )
    except FileNotFoundError:
        print("no student has taken any quiz")


def already_did(adm):
    """
    Check if a student with given registration number has already taken a quiz
    Returns status indicating if student can take quiz
    """
    try:
        with open("results.json", "r") as file:
            results = json.load(file)
        
        if not results["details"]:
            return "first"  # No results yet
            
        for detail in results["details"]:
            if detail["registration"] == adm:
                return "done"  # Student already took quiz
                
        return "good"  # Student can take quiz
        
    except FileNotFoundError:
        return "error"  # Results file doesn't exist

def create_quiz(selected_dept):
    """
    Create a new quiz with questions and options
    Saves to the department's JSON file
    """
    filename = f"{selected_dept}.json"

    # Load existing quizzes or create new structure
    try:
        with open(filename, "r") as file:
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

    # Check if title already exists (case-insensitive)
    for quiz in department_quiz["quizzes"]:
        if quiz["title"].lower() == title.lower():
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
                question["question"] = question_text
                break
            print("Question cannot be empty.")

        # Get options (A, B, C, D)
        options = []
        letters = ["A", "B", "C", "D"]
        for letter in letters:
            while True:
                option = input(f"Enter option {letter}: ").strip()
                if option:
                    options.append(option)
                    break
                print("Option cannot be empty.")

        question["options"] = options

        # Get correct answer
        while True:
            correct_answer = input("Enter the correct answer (A/B/C/D): ").upper()
            if correct_answer in letters:
                question["answer"] = options[letters.index(correct_answer)]
                break
            print("Invalid input. Please enter A, B, C, or D.")

        # Add question to questions list
        questions.append(question)

        # Ask if user wants to add another question
        while True:
            another = input("\nAdd another question? (y/n): ").lower()
            if another in ["y", "n"]:
                break
            print("Please enter 'y' or 'n'.")

        if another == "n":
            break

    # Create the quiz object
    new_quiz = {"title": title, "questions": questions}

    # Add to department data
    department_quiz["quizzes"].append(new_quiz)

    print(f"\nQuiz '{title}' created successfully with {len(questions)} questions!")
    return department_quiz


def delete_quiz():
    """
    Delete a quiz from a department's JSON file
    Allows lecturer to select and remove a specific quiz
    """
    department = select_dep()
    filename = f"{department}.json"
    
    try:
        with open(filename, "r") as file:
            questions = json.load(file)
            
        if not questions["quizzes"]:
            return "empty"
            
        # Display quizzes
        print(f"\nQuizzes in {department}:")
        for i, quiz in enumerate(questions["quizzes"], 1):
            print(f"{i}: {quiz['title']}")

        # Get selection with validation
        while True:
            try:
                to_delete = int(input("Which quiz do you want to delete? (0 to cancel): "))
                if to_delete == 0:
                    return "cancelled"
                if 1 <= to_delete <= len(questions["quizzes"]):
                    # Confirm deletion
                    quiz_title = questions["quizzes"][to_delete-1]["title"]
                    confirm = input(f"Delete '{quiz_title}'? (y/n): ").lower()
                    if confirm == "y":
                        del questions["quizzes"][to_delete-1]
                        break
                    else:
                        return "cancelled"
                print(f"Please enter 1-{len(questions['quizzes'])} or 0 to cancel")
            except ValueError:
                print("Please enter a valid number.")
                
        # Save updated data safely
        temp_filename = f"{filename}.tmp"
        with open(temp_filename, "w") as file:
            json.dump(questions, file, indent=4)
        
        # Replace original file
        if os.path.exists(filename):#operating system function that check if in the path their exist file with that name
            os.remove(filename)#if their exist a file the file get deleted
        os.rename(temp_filename, filename)#the temp file is renamed here
            
        
        return "success"
        
    except FileNotFoundError:
        
        return "no_file"


def call_quiz():
    """
    Handle the process of selecting department and quiz
    Returns the selected quiz or None if no quizzes available
    """
    print("select the department you want it's quiz" + "-" * 40)
    depart = select_dep()
    filename = f"{depart}.json"

    try:
        data = load_quizzes(filename)
        quiz = select_quiz(data["quizzes"])
    except TypeError:#that is if data becomes none then you can't say data['quizzes] it will be type error
        return None
    return quiz


def sub_main():
    """
    Main application logic - handles user interaction flow
    Coordinates between different functions based on user choices
    """
    while True:

        # Get user role (lecturer or student)
        while True:
            print("\nThere are two personel here\n1. lecturer\n2. student")
            position = input("\nyou are entering as...").strip()
            if position == "1" or position == "2":
                break
            print("please select 1 or 2")

        mode = menu()

        # Lecturer taking quiz (for testing purposes)
        if position == "1" and mode == "1":
            while True:
                name = input("Enter the name...").strip()
                if name:
                    break
                print("name cannot be empty\n")
            adm = "lecturer"
            try:
                with open("results.json", "r") as file:
                    result = json.load(file)
            except FileNotFoundError:
                create_results_file()
            quiz = call_quiz()
            if quiz == None:
                print("wait for lecturer to add a quiz\n")
            else:
                score, total = run_quiz(quiz)
                score = display_results(score, total)
                store_results(score, name, adm)

        # Student taking quiz
        elif position == "2" and mode == "1":  # Take a quiz
            name, adm = validate()

            status = already_did(adm)
            if status == "error":
                create_results_file()
                quiz = call_quiz()

                if quiz == None:
                    print("wait for lecturer to add a quiz\n")
                else:
                    score, total = run_quiz(quiz)
                    score = display_results(score, total)
                    store_results(score, name, adm)

            elif status == "done":
                print("\n⚠️ ⚠️  you already did the quiz\n")
            elif status == "good" or status == "first":
                quiz = call_quiz()
                if quiz == None:
                    print("wait for lecturer to add a quiz\n")
                else:
                    score, total = run_quiz(quiz)
                    score = display_results(score, total)
                    store_results(score, name, adm)

        # Lecturer creating quiz
        elif mode == "2" and position == "1":  # Create a quiz
            selected_dept = select_dep()
            data = create_quiz(selected_dept)
            filename = f"{selected_dept}.json"
            save_quizzes(filename, data)

        # Student trying to create quiz (not allowed)
        elif mode == "2" and position == "2":
            print("  !!only lecturer can create quizes  \n\tchoose again\n")
           
            

        # View results
        elif mode == "3":
            os.system("cls" if os.name == "nt" else "clear")
            print("--------RESULTS-----------\n")
            view_result()
            print("press Q to quit...")
            print("\nany other key pressed will take you home")
            quit = input().upper()

            if quit == "Q":
                os.system("cls" if os.name == "nt" else "clear")
                print("Thank you for using the Quiz App. Goodbye!\n")
                j = "l"
            else:
                os.system("cls" if os.name == "nt" else "clear")
                

        # Lecturer deleting quiz
        elif mode == "4" and position == "1":  # Delete quiz
            deleted = delete_quiz()
            if deleted == "success":
                print("deleted successfully")
            elif deleted == "cancelled":
                os.system("cls" if os.name == 'nt' else 'clear')
            elif deleted == "no_file" or deleted == "empty":
                print("the department has no questions")

        # Student trying to delete quiz (not allowed)
        elif mode == "4" and position == "2":
            print("\nonly lecturers can delete a quiz\n")
        elif mode == "5":
            os.system("cls" if os.name == "nt" else "clear")
            print("thank you for using my app")
            
            break

        # Clear screen and continue (except for view results)
        if mode != "3":
            input("\nPress Enter to continue...")
            os.system("cls" if os.name == "nt" else "clear")
            display_welcome()


def main():
    """
    Main entry point of the application
    Initializes welcome screen and starts main logic
    """
    display_welcome()
    sub_main()


# Start the application
main()