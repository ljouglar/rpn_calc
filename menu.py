#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy, curses
from stack import Stack, QuitException, UnknownCommandException, StackUnderflowException, AngleUnitChangeException

class Menu:
    "Show the calculator interface, handles user input"
    STATUS_LINE_Y = 0
    STACK_X = 0
    STACK_SIZE = 5
    MSG_LINE_Y = STATUS_LINE_Y + STACK_SIZE + 2

    def __init__(self):
        "Initialize an empty stack"
        self.stack = Stack()
        self.message_line = ""

    def get_status_line(self):
        "Show angle unit at top of calculator"
        if self.stack.conv == 1.0:
            return "RAD"
        else:
            return "DEG"

    def get_input(self, prompt = "> "):
        """Handles user input key by key :
            - [esc] or "q" to quit the calculator
            - [enter] to duplicate last stack element or to lauch the command being constituted
            - [backspace] to remove last stack element
            - +, -, * and / operands to execute the operation
            - any other key to constitute the command or a stack element"""
        result = ""
        prompt_y = self.STATUS_LINE_Y + 1 + self.STACK_SIZE
        while True:
            self.stdscr.addstr(prompt_y, self.STACK_X, "                       ")
            self.stdscr.addstr(prompt_y, self.STACK_X, prompt + result)
            curses.flushinp()
            key = self.stdscr.getch()
            if key == 27 or (chr(key) == "q" and result == ""):
                result = "q"
                break
            elif key == 127 or key == 263:
                if result == "":
                    result = "drop"
                    break
                else:
                    result = result[:-1]
            elif key == 13 or key == 10:
                break
            elif chr(key) in ["+", "-", "*", "/", "!"]:
                if result == "":
                    result = chr(key)
                else:
                    result += " " + chr(key)
                break
            else:
                result += chr(key)
        self.message_line = ""
        return result

    def print_stack(self):
        "Print stack content on screen, plus status and message lines"
        self.stdscr.addstr(self.STATUS_LINE_Y, self.STACK_X, self.get_status_line())
        for y in range(0, self.STACK_SIZE):
            line_y = self.STATUS_LINE_Y + self.STACK_SIZE - y
            try:
                self.stdscr.addstr(line_y, self.STACK_X, str(self.stack[-y - 1]))
            except:
                break
        self.stdscr.addstr(self.MSG_LINE_Y, self.STACK_X, self.message_line)

    def will_it_float(self, str):
        "Indicate wether a string can be converted to float or not"
        try:
            float(str)
            return True
        except ValueError:
            return False

    def run(self):
        "Handles user input wher the [enter] key is pressed"
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        try:
            while True:
                self.stdscr.clear()
                self.print_stack()
                cmds = self.get_input()
                for cmd in cmds.split(" "):
                    saved_stack = copy.deepcopy(self.stack)
                    try:
                        if self.will_it_float(cmd):
                            self.stack.append(float(cmd))
                        else:
                            self.stack.execute_command(cmd)
                    except StackUnderflowException as e:
                        self.message_line = str(e)
                        self.stack = saved_stack
                    except ZeroDivisionError as e:
                        self.message_line = "division by zero"
                        self.stack = saved_stack
                    except AngleUnitChangeException as e:
                        pass # Nothing to do, just re-show stack
                    except UnknownCommandException as e:
                        self.message_line = str(e)
                    except QuitException as e:
                        self.message_line = str(e)
                        exit(0)
                    except Exception as e:
                        self.message_line = str(e)
                        self.stack = saved_stack
        finally:
            self.stdscr.keypad(False)
            curses.nocbreak()
            curses.echo()
            curses.endwin()

if __name__ == "__main__":
    Menu().run()
