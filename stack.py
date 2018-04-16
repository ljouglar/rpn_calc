#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math

class QuitException(BaseException):
    "To send back the quit message"
    pass

class UnknownCommandException(BaseException):
    "To send back that the command is unknown"
    pass

class StackUnderflowException(BaseException):
    "To send back that ther is not enough elemnets in the stack to proceed the command"
    pass

class AngleUnitChangeException(BaseException):
    "To send back that the angle unit has changed"
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
            "!": self.fact, "fact": self.fact, "sqrt": self.sqrt,

            "chs": self.chs, "abs": self.abs, "inv": self.inv,
            "e": self.e, "exp": self.exp, "ln": self.ln, "log": self.log,

            "deg": self.deg, "rad": self.rad,
            "pi": self.pi, "sin": self.sin, "cos": self.cos, "tan": self.tan,
            "asin": self.asin, "acos": self.acos, "atan": self.atan,

            "": self.dup, "dup": self.dup,
            "swp": self.swap, "swap": self.swap,
            "drop": self.drop,
            "clr": self.clear, "clear": self.clear,
            "roll": self.roll,
            "rolld": self.rolld,

            "q": self.quit, "quit": self.quit, "exit": self.quit,
        }
        self.conv = 1.0 # radians by default

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
        try:
            self.append(self.pop() - to_sub)
        except:
            self.append(- to_sub)


    def multiply(self):
        "Multiplies last two stack elements"
        self.append(self.pop() * self.pop())

    def divide(self):
        "Divides last two stack elements"
        to_div = self.pop()
        self.append(round(self.pop() / to_div, 9))

    def power(self):
        "Powers last two stack elements"
        to_power = self.pop()
        self.append(self.pop() ** to_power)

    def fact(self):
        "Factorial last stack elements"
        self.append(math.factorial(self.pop()))

    def sqrt(self):
        "Square root last stack elements"
        self.append(round(math.factorial(self.pop()), 9))


    def chs(self):
        "Change last stack elements sign"
        self.append(- self.pop())

    def abs(self):
        "Absolute last stack elements value"
        self.append(math.fabs(self.pop()))

    def inv(self):
        "Inverse last stack elements"
        self.append(round(1.0 / self.pop(), 9))


    # Exp methods
    def e(self):
        "Pushes e constant to stack"
        self.append(math.e)

    def exp(self):
        "Exponential last stack elements"
        self.append(math.exp(self.pop()))

    def ln(self):
        "Neperian logarithm last stack elements"
        self.append(round(math.log(self.pop()), 9))

    def log(self):
        "Logarith last stack elements"
        self.append(round(math.log10(self.pop()), 0))


    # Trigo methods
    def deg(self):
        self.conv = math.pi / 180.0
        raise AngleUnitChangeException("angle unit changed to DEG")

    def rad(self):
        self.conv = 1.0
        raise AngleUnitChangeException("angle unit changed to RAD")

    def pi(self):
        "Pushes PI constant to stack"
        self.append(math.pi)

    def sin(self):
        "Apply sinus function to last stack element"
        self.append(round(math.sin(self.conv * self.pop()), 9))

    def cos(self):
        "Apply cosinus function to last stack element"
        self.append(round(math.cos(self.conv * self.pop()), 9))

    def tan(self):
        "Apply tangent function to last stack element"
        self.append(round(math.tan(self.conv * self.pop()), 9))

    def asin(self):
        "Apply arcsinus function to last stack element"
        self.append(round(math.asin(self.conv * self.pop()), 9))

    def acos(self):
        "Apply arccosinus function to last stack element"
        self.append(round(math.acos(self.conv * self.pop()), 9))

    def atan(self):
        "Apply arctangent function to last stack element"
        self.append(round(math.atan(self.conv * self.pop()), 9))


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
        "Rolls up the stack (last element becomes first)"
        self.append(self.pop(0))

    def rolld(self):
        "Rolls down the stack (first element becomes last)"
        self.insert(0, self.pop())

    def quit(self):
        "Send the quit exception to quit the calculator"
        raise QuitException("exit by user")
