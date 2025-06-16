import random

def grade_comic(image_data_base64):
    # Simulate grading for now — replace with real model later
    possible_grades = ['9.8', '9.6', '9.4', '9.2', '9.0', '8.5', '8.0', '7.5', '7.0', '6.5', '6.0']
    flaws = ['None', 'Spine creases', 'Corner dings', 'Small tear', 'Color fade', 'Finger bends', 'Staple rust']
    
    grade = random.choice(possible_grades)
    found_flaws = random.sample(flaws, k=random.randint(0, 2)) if grade != '9.8' else ['None']
    
    return grade, found_flaws
