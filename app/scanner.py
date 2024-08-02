from app.token import Token
import sys
class Scanner:
    def __init__(self, source) -> None:
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.exit_code = 0

    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        
        self.tokens.append(Token("EOF", "","null",self.line))
        return self.tokens

    def scan_token(self):
        c= self.advance()

        match c:
            case "(":
                self.add_token("LEFT_PAREN")
            case ")":
                self.add_token("RIGHT_PAREN")
            case "{":
                self.add_token("LEFT_BRACE")
            case "}":
                self.add_token("RIGHT_BRACE")
            case ",":
                self.add_token("COMMA")
            case ".":
                self.add_token("DOT")
            case "-":
                self.add_token("MINUS")
            case "+":
                self.add_token("PLUS")
            case ";":
                self.add_token("SEMICOLON")
            case "*":
                self.add_token("STAR")
            case "!":
                self.add_token("BANG_EQUAL" if self.match("=") else "BANG")
            case "=":
               self.add_token("EQUAL_EQUAL" if self.match('=') else "EQUAL") 
            case "<":
                self.add_token("LESS_EQUAL" if self.match("=") else "LESS")
            case ">":
                self.add_token("GREATER_EQUAL" if self.match("=") else "GREATER")
            case "/":
                if self.match("/"):
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                else:
                    self.add_token("SLASH")
            case " ":
                pass
            case "\r":
                pass
            case "\t":  
                pass
            case "\n":
                self.line += 1
            case '"':
                self.string()
            case _:
                print(f"[line {self.line}] Error: Unexpected character: {c}", file=sys.stderr)
                self.exit_code = 65

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()
        
        if self.is_at_end():
           print(f"[line {self.line}] Error: Unterminated string.", file=sys.stderr)
           self.exit_code = 65 
           return

        self.advance()
        value = self.source[self.start + 1 : self.current - 1]
        self.add_token("STRING", value)

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        
        self.current += 1
        return True

    def peek(self):
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def is_at_end(self):
        return self.current >= len(self.source)
    
    def advance(self):
        self.current += 1
        return self.source[self.current -1]

    def add_token(self, type, literal = None):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, literal, self.line))
