class ExperienceException(Exception):
    def __init__(self, message="You need to select your experience level to access your workout plan"):
        super().__init__(message)