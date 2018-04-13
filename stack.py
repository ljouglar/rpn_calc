class QuitException(BaseException):
    pass

class UnknownCommandException(BaseException):
    pass

class StackUnderflowException(BaseException):
    pass

class Stack(list):
    def __init__(self):
        self._stack_commands = {
            "+": self.add, "add": self.add,
            "-": self.substract, "sub": self.substract, "subs": self.substract,
            "*": self.multiply, "mul": self.multiply, "mult": self.multiply,
            "/": self.divide, "div": self.divide, "divide": self.divide,
            "^": self.power, "**": self.power, "power": self.power,

            "": self.dup, "dup": self.dup,
            "swp": self.swap, "swap": self.swap,
            "drop": self.drop,
            "clr": self.clear, "clear": self.clear,
            "roll": self.roll,
            "rolld": self.rolld,

            "q": self.quit, "quit": self.quit, "exit": self.quit,
        }

    def execute_command(self, cmd):
        try:
            command = self._stack_commands[cmd]
        except:
            raise UnknownCommandException("commande inconnue")
        try:
            command()
        except IndexError as e:
            raise StackUnderflowException("pas assez d'arguments")

    # Math methods
    def add(self):
        self.append(self.pop() + self.pop())

    def substract(self):
        to_sub = self.pop()
        self.append(self.pop() - to_sub)

    def multiply(self):
        self.append(self.pop() * self.pop())

    def divide(self):
        to_div = self.pop()
        self.append(self.pop() / to_div)

    def power(self):
        to_power = self.pop()
        self.append(self.pop() ** to_power)

    # Stack manipulation
    def dup(self):
        to_dup = self.pop()
        self.append(to_dup)
        self.append(to_dup)

    def swap(self):
        first = self.pop()
        second = self.pop()
        self.append(first)
        self.append(second)

    def drop(self):
        self.pop()

    def roll(self):
        self.insert(0, self.pop())

    def rolld(self):
        self.append(self.pop(0))

    def quit(self):
        raise QuitException("sortie normale du programme")
