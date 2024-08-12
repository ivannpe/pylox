from app.tokentype import TokenType
class Token:
    def __init__(self, type: TokenType, lexeme, literal, line) -> None:
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self) -> str:
        return f"{self.type} {self.lexeme} {self.literal}"