class GoalAndExperienceException(Exception):
    def __init__(self, message="You need to select both your fitness goal and experience level to access your workout plan"):
        super().__init__(message)