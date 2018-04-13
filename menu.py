#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy, curses
from stack import Stack, QuitException, UnknownCommandException, StackUnderflowException

class Menu:
    "Show the calculator interface, handles user input"

    def __init__(self):
        "Initialize an empty stack"
        self.stack = Stack()
        self.message_line = ""

    def get_input(self, prompt = "> "):
        """Handles user input key by key :
            - [esc] or "q" to quit the calculator
            - [enter] to duplicate last stack element or to lauch the command being constituted
            - [backspace] to remove last stack element
            - +, -, * and / operands to execute the operation
            - any other key to constitute the command or a stack element"""
        result = ""
        while True:
            self.stdscr.addstr(8, 0, "                       ")
            self.stdscr.addstr(8, 0, prompt + result)
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
            elif chr(key) in ["+", "-", "*", "/"]:
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
        "Print the stack content on screen, plus the message line"
        for y in range(0, 7):
            try:
                self.stdscr.addstr(7 - y, 0, str(self.stack[-y - 1]))
            except:
                break
        self.stdscr.addstr(9, 0, self.message_line)

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
                    except UnknownCommandException as e:
                        self.message_line = str(e)
                    except QuitException as e:
                        self.message_line = str(e)
                        exit(0)
        finally:
            self.stdscr.keypad(False)
            curses.nocbreak()
            curses.echo()
            curses.endwin()

if __name__ == "__main__":
    Menu().run()
