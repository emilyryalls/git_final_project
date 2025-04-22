class GoalException(Exception):
    def __init__(self, message="You need to select a fitness goal to access your workout plan"):
        super().__init__(message)