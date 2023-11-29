class ErrorCode:
    """
    Константы для описания ошибок в модуле аутентификации.
    """
    AUTHENTICATION_REQUIRED = "Authentication required."
    AUTHORIZATION_FAILED = "Authorization failed. User has no access."
    INVALID_TOKEN = "Invalid token."
    INVALID_CREDENTIALS = "Invalid credentials."
    EMAIL_TAKEN = "Email is already taken."
    REFRESH_TOKEN_NOT_VALID = "Refresh token is not valid."
    REFRESH_TOKEN_REQUIRED = "Refresh token is required either in the body or cookie."
    INVALID_EMAIL_RESET_PASS_CONFIRM_TOKEN = "Email or reset pass token invalid, try again."
