import random
from datetime import datetime, timedelta

# Function to print the menu
def print_menu():
    
    print("\nYou may select one of the following:")
    print(" 1) Add student")
    print(" 2) Search student")
    print(" 3) Search course")
    print(" 4) Add course completion")
    print(" 5) Show student's record")
    print(" 0) Exit")
    print("What is your selection?")

# Function to add a new student
def add_student():
    print("Enter the first name of the student:")
    first_name = input()
    print("Enter the last name of the student:")
    last_name = input()

    # Check if names contain only letters and start with capital letters
    if not first_name.isalpha() or not last_name.isalpha() or not first_name.istitle() or not last_name.istitle():
        print("Names should contain only letters and start with capital letters.")
        return

    majors = {'CE': 'Computational Engineering', 'EE': 'Electrical Engineering', 'ET': 'Energy Technology',
              'ME': 'Mechanical Engineering', 'SE': 'Software Engineering'}
    print("Select student's major:")
    for code, major in majors.items():
        print(f" {code}: {major}")

    major_selection = input("What is your selection?\n")

    if major_selection not in majors:
        print("Invalid major selection.")
        return

    # Generate email address
    email = f"{first_name.lower()}.{last_name.lower()}@lut.fi"

    # Generate unique study number
    study_number = random.randint(10000, 99999)
    while study_number in used_study_numbers:
        study_number = random.randint(10000, 99999)

    # Get current year
    starting_year = datetime.now().year

    # Append student information to data/students.txt where data is folder where we all records
    with open('data/students.txt', 'a') as file:
        file.write(f"{study_number},{first_name},{last_name},{starting_year},{major_selection},{email}\n")

    print("Student added successfully!")

# Function to search for a student
def search_student():
    search_term = input("Give at least 3 characters of the students first or last name:\n")
    
    if len(search_term) < 3:
        print("Search term must contain at least 3 characters.")
        return

    matching_students = []

    # Search for matching students in data/students.txt where data is folder where we all records
    with open('data/students.txt', 'r') as file:
        for line in file:
            student_data = line.strip().split(',')
            student_id, first_name, last_name = student_data[0], student_data[1], student_data[2]
            
            if search_term.lower() in first_name.lower() or search_term.lower() in last_name.lower():
                matching_students.append(f"ID: {student_id}, First name: {first_name}, Last name: {last_name}")

    if not matching_students:
        print("No matching students found.")
    else:
        print("Matching students:")
        for student_info in matching_students:
            print(student_info)

# Function to search for a course
def search_course():
    search_term = input("Give at least 3 characters of the name of the course or the teacher:\n")
    
    if len(search_term) < 3:
        print("Search term must contain at least 3 characters.")
        return

    matching_courses = []

    # Search for matching courses in  data/courses.txt where data is folder where we all records
    with open('data/courses.txt', 'r') as file:
        for line in file:
            course_data = line.strip().split(',')
            course_id, course_name, credits, teachers = course_data[0], course_data[1], course_data[2], course_data[3:]
            
            if any(search_term.lower() in term.lower() for term in [course_name] + teachers):
                teacher_list = ', '.join(teachers)
                matching_courses.append(f"ID: {course_id}, Name: {course_name}, Credits: {credits}, Teacher(s): {teacher_list}")

    if not matching_courses:
        print("No matching courses found.")
    else:
        print("Matching courses:")
        for course_info in matching_courses:
            print(course_info)

# Function to add a course completion
def add_course_completion():
    course_id = input("Give the course ID:\n")
    student_id = input("Give the student ID:\n")

    # Check if the course and student exist
    if not check_course_exists(course_id) or not check_student_exists(student_id):
        print("Course or student does not exist.")
        return

    # Check if the student has passed the course earlier
    old_grade = get_student_course_grade(student_id, course_id)
    if old_grade:
        new_grade = int(input(f"Student has passed this course earlier with grade {old_grade}\nGive the grade:\n"))
        if new_grade <= old_grade:
            print("New grade is not higher than the old grade. No changes made.")
            return

    # Validate the new grade
    if new_grade > 6:
        print("Grade is not a correct grade.")
        return

    # Check if the date is valid
    date_str = input("Enter a date (DD/MM/YYYY):\n")
    try:
        completion_date = datetime.strptime(date_str, '%d/%m/%Y')
        today = datetime.now()
        if completion_date > today:
            print("Input date is later than today. Try again!")
            return
        if (today - completion_date).days > 30:
            print("Input date is older than 30 days. Contact 'opinto'.")
            return
    except ValueError:
        print("Invalid date format. Use DD/MM/YYYY. Try again!")
        return

    # Add the completion to data/passed.txt where data is a folder where we store all records
    with open('data/passed.txt', 'a') as file:
        file.write(f"{course_id},{student_id},{date_str},{new_grade}\n")

    print("Record added!")

# Function to show student's record
def show_student_record():
    student_id = input("Enter the student ID:\n")

    # Check if the student exists
    if not check_student_exists(student_id):
        print("Student does not exist.")
        return

    # Get student information from data/students.txt where data is folder where we all records
    with open('data/students.txt', 'r') as file:
        for line in file:
            student_data = line.strip().split(',')
            if student_data[0] == student_id:
                student_info = f"Student ID: {student_data[0]}\nName: {student_data[2]}, {student_data[1]}\nStarting year: {student_data[3]}\nMajor: {majors[student_data[4]]}\nEmail: {student_data[5]}"

    # Get passed courses information from  data/passed.txt  where data is folder where we all records
    passed_courses = []
    total_credits = 0
    total_grade = 0

    with open('data/passed.txt', 'r') as file:
        for line in file:
            passed_data = line.strip().split(',')
            if passed_data[1] == student_id:
                course_info = get_course_info(passed_data[0])
                passed_courses.append(f"Course ID: {passed_data[0]}, Name: {course_info['name']}, Credits: {course_info['credits']}, Grade: {passed_data[3]}, Completion Date: {passed_data[2]}")
                total_credits += int(course_info['credits'])
                total_grade += int(passed_data[3])

    # Display student record
    print("\nStudent Record:")
    print(student_info)
    print("\nPassed Courses:")
    for course in passed_courses:
        print(course)
    print("\nTotal Credits: ", total_credits)
    print("Average Grade: ", total_grade / len(passed_courses) if passed_courses else 0)

# Function to check if a course exists
def check_course_exists(course_id):
    with open('data/courses.txt', 'r') as file:
        for line in file:
            if line.strip().split(',')[0] == course_id:
                return True
    return False

# Function to check if a student exists
def check_student_exists(student_id):
    with open('data/students.txt', 'r') as file:
        for line in file:
            if line.strip().split(',')[0] == student_id:
                return True
    return False

# Function to get a student's grade for a specific course
def get_student_course_grade(student_id, course_id):
    with open('data/passed.txt', 'r') as file:
        for line in file:
            passed_data = line.strip().split(',')
            if passed_data[1] == student_id and passed_data[0] == course_id:
                return int(passed_data[3])
    return None

# Function to get information about a course
def get_course_info(course_id):
    with open('data/courses.txt', 'r') as file:
        for line in file:
            course_data = line.strip().split(',')
            if course_data[0] == course_id:
                return {'name': course_data[1], 'credits': course_data[2], 'teachers': course_data[3:]}

# Main program loop
used_study_numbers = set()

# Load existing study numbers
with open('data/students.txt', 'r') as file:
    for line in file:
        # Skip empty lines
        if not line.strip():
            continue

        study_number = int(line.strip().split(',')[0])
        used_study_numbers.add(study_number)


majors = {'CE': 'Computational Engineering', 'EE': 'Electrical Engineering', 'ET': 'Energy Technology',
          'ME': 'Mechanical Engineering', 'SE': 'Software Engineering'}

while True:
    print_menu()
    choice = input()
    if choice == '1':
        add_student()
    elif choice == '2':
        search_student()
    elif choice == '3':
        search_course()
    elif choice == '4':
        add_course_completion()
    elif choice == '5':
        show_student_record()
    elif choice == '0':
        print("Exiting the program. Goodbye!")
        break
    else:
        print("Invalid selection. Please try again.")