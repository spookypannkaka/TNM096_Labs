from aima.csp import CSP, min_conflicts
import random

class Schedule(CSP):
    def __init__(self, initial_assignment=None):
        super().__init__(
            variables=classes, # To be assigned values (rooms, time)
            domains={cls: [(room, time) for room in rooms for time in times] for cls in classes}, # Possible values for the variables
            neighbors={cls: [other for other in classes if other != cls and check_class_year(cls) == check_class_year(other)] for cls in classes}, # Class neighbors are in the same year
            constraints=self.schedule_constraints
        )
        if initial_assignment:
            self.current = initial_assignment
        else:
            self.current = self.initial_placement()

    # Check constraints for classes. A and B are classes, a and b are the values assigned to them (room, time)
    def schedule_constraints(self, A, a, B, b):
        # Constraint 1: Two classes cannot meet in the same room at the same time
        if a == b:
            return False
        
        # Constraint 2: Classes of the same year cannot be at the same time, except MT501 and MT502
        if check_class_year(A) == check_class_year(B) and a[1] == b[1]:  # Check if same year and same time
            if not ((A in ['MT501', 'MT502'] and B in ['MT501', 'MT502']) and a[1] != b[1]):
                return False
        
        return True

    # Create time table
    def initial_placement(self):
        initial = {}
        for cls in classes:
            chosen_room = random.choice(rooms)
            chosen_time = random.choice(times)
            initial[cls] = (chosen_room, chosen_time)
        return initial

# Definitions
classes = ['MT101', 'MT102', 'MT103', 'MT104', 'MT105', 'MT106', 'MT107', 'MT201', 'MT202', 'MT203', 'MT204', 'MT205', 'MT206', 'MT301', 'MT302', 'MT303', 'MT304', 'MT401', 'MT402', 'MT403', 'MT501', 'MT502']
times = [9, 10, 11, 12, 1, 2, 3, 4]
rooms = ['TP51', 'SP34', 'K3']

initial_schedule = {
    'MT101': ('TP51', 9), 'MT102': ('SP34', 12), 'MT103': ('K3', 11),
    'MT104': ('TP51', 10), 'MT105': ('SP34', 1), 'MT106': ('K3', 2),
    'MT107': ('TP51', 4), 'MT201': ('SP34', 2), 'MT202': ('K3', 1),
    'MT203': ('TP51', 3), 'MT204': ('SP34', 9), 'MT205': ('K3', 12),
    'MT206': ('TP51', 4), 'MT301': ('SP34', 3), 'MT302': ('K3', 10),
    'MT303': ('TP51', 9), 'MT304': ('SP34', 10), 'MT401': ('K3', 11),
    'MT402': ('TP51', 2), 'MT403': ('SP34', 1), 'MT501': ('K3', 3), 'MT502': ('TP51', 2)
}

# Returns the first number of the class code, as it represents the class year
def check_class_year(cls):
    for char in cls:
        if char.isdigit():
            return int(char)
    return None

# Display the schedule
def display_schedule(schedule):
    timetable = {time: {room: None for room in rooms} for time in times}
    
    for cls, (room, time) in schedule.items():
        if time in timetable and room in timetable[time]:
            timetable[time][room] = cls

    for time in times:
        print(f"{time}: {timetable[time]}")

solution = min_conflicts(Schedule(initial_assignment=initial_schedule))

if solution:
    display_schedule(solution)
else:
    print("Failed to find a solution")





''' Task 4 '''
def preference_score(schedule):
    score = 0

    for cls, (room, time) in schedule.items():
        # Preferation 1: Schedules that do not schedule classes at 9, 12, and 4
        if time not in [9, 12, 4]:
            score += 1  # Reward for not being at 9, 12, 4

        # Preferation 2: Schedules where MT501 and MT502 are scheduled at 1 or 2
        if cls in ['MT501', 'MT502'] and time in [1, 2]:
            score += 1  # Reward schedules that place these classes at preferred times

    return score

def find_best_schedule():
    number_of_attempts = 1000

    best_score = float('-inf')
    best_schedule = None

    for _ in range(number_of_attempts):
        current_schedule = min_conflicts(Schedule())
        if current_schedule:
            score = preference_score(current_schedule)
            if score > best_score:
                best_score = score
                best_schedule = current_schedule

    return best_schedule

best_schedule = find_best_schedule()

''''if best_schedule:
    display_schedule(best_schedule)
else:
    print("Failed to find a solution")'''