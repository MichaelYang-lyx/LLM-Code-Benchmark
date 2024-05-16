
def numerical_letter_grade(grades):
    def get_letter_grade(gpa):
        if gpa == 4.0:
            return 'A+'
        elif gpa > 3.7:
            return 'A'
        elif gpa > 3.3:
            return 'A-'
        elif gpa > 3.0:
            return 'B+'
        elif gpa > 2.7:
            return 'B'
        elif gpa > 2.3:
            return 'B-'
        elif gpa > 2.0:
            return 'C+'
        elif gpa > 1.7:
            return 'C'
        elif gpa > 1.3:
            return 'C-'
        elif gpa > 1.0:
            return 'D+'
        elif gpa > 0.7:
            return 'D'
        elif gpa > 0.0:
            return 'D-'
        else:
            return 'E'

    return [get_letter_grade(gpa) for gpa in grades]

# example usage
print(numerical_letter_grade([4.0, 3, 1.7, 2, 3.5]))  # ['A+', 'B', 'C-', 'C', 'A-']
