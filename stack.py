#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class QuitException(BaseException):
    "To send back the quit message"
    pass

class UnknownCommandException(BaseException):
    "To send back that the command is unknown"
    pass

class StackUnderflowException(BaseException):
    "To send back that ther is not enough elemnets in the stack to proceed the command"
    pass

class Stack(list):
    "Use the list class to simulate a RPN calculator stack"

    def __init__(self):
        "Initialize the known commands and point to the according method"
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
        "Execute the given command, sending back eventual errors"
        try:
            command = self._stack_commands[cmd]
        except:
            raise UnknownCommandException("unknown command")
        try:
            command()
        except IndexError as e:
            raise StackUnderflowException("stack underflow")

    # Math methods
    def add(self):
        "Adds last two stack elements"
        self.append(self.pop() + self.pop())

    def substract(self):
        "Substracts last two stack elements"
        to_sub = self.pop()
        self.append(self.pop() - to_sub)

    def multiply(self):
        "Multiplies last two stack elements"
        self.append(self.pop() * self.pop())

    def divide(self):
        "Divides last two stack elements"
        to_div = self.pop()
        self.append(self.pop() / to_div)

    def power(self):
        "Powers last two stack elements"
        to_power = self.pop()
        self.append(self.pop() ** to_power)

    # Stack manipulation
    def dup(self):
        "Duplicates last stack element"
        to_dup = self.pop()
        self.append(to_dup)
        self.append(to_dup)

    def swap(self):
        "Swaps last two stack elements"
        first = self.pop()
        second = self.pop()
        self.append(first)
        self.append(second)

    def drop(self):
        "Removes last stack element"
        self.pop()

    def roll(self):
        "Rolls the stack (first element becomes last)"
        self.insert(0, self.pop())

    def rolld(self):
        "Rolls the stack (last element becomes first)"
        self.append(self.pop(0))

    def quit(self):
        "Send the quit exception to quit the calculator"
        raise QuitException("exit by user")
