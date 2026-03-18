from fastapi import HTTPException


class UserError(HTTPException):
    pass

class UserNotFoundError(UserError):
    def __init__(self, user_id=None):
        message = "User not found" if user_id is None else f"user with id {user_id} not found"
        super().__init__(status_code=404, detail=message)

class PasswordMismatchError(UserError):
    def __init__(self):
        super().__init__(status_code=400, detail="New passwords do not match")

class InvalidPasswordError(UserError):
    def __init__(self):
        super().__init__(status_code=401, detail="Current password is incorrect")

class AuthenticationError(HTTPException):
    def __init__(self, message: str =  "Could not validate user"):
        super().__init__(status_code=401, detail=message)




class TodoError(HTTPException):
    pass

class TodoCreationError(TodoError):
    def __init__(self):
        super().__init__(status_code=500, detail="Creation failed")

class TodoNotFoundError(TodoError):
    def __init__(self, todo_id):
        message = f"Todo not found for user" if not todo_id else f"todo not found for user {todo_id}"
        super().__init__(status_code=404, detail=message)
