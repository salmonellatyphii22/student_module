def calculate_grade(total):
    if total >= 90:
        return "A"
    elif total >= 75:
        return "B"
    elif total >= 60:
        return "C"
    elif total >= 50:
        return "D"
    else:
        return "F"


def calculate_gpa(marks_list):
    total_points = 0
    total_subjects = len(marks_list)

    grade_map = {"A": 10, "B": 8, "C": 6, "D": 5, "F": 0}

    for m in marks_list:
        total_points += grade_map.get(m.grade, 0)

    return total_points / total_subjects if total_subjects else 0