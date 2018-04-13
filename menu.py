#!/usr/bin/env python
import copy, curses
from stack import Stack, QuitException, UnknownCommandException, StackUnderflowException

class Menu:
    def __init__(self):
        self.stack = Stack()
        self.message_line = ""

    def get_input(self, prompt = "> "):
        result = ""
        while True:
            self.stdscr.addstr(8, 0, "                       ")
            self.stdscr.addstr(8, 0, prompt + result)
            key = self.stdscr.getch()
            if key == 27 or (chr(key) == "q" and result == ""):
                result = "q"
                break
            elif key == 127:
                if result == "":
                    result = "drop"
                    break
                else:
                    result = result[:-1]
            elif key == 13 or key == 10:
                break
            elif chr(key) in ["+", "-", "*", "/"] and result == "":
                result = chr(key)
                break
            else:
                result += chr(key)
        self.message_line = ""
        return result

    def print_stack(self):
        for y in range(0, 7):
            try:
                self.stdscr.addstr(7 - y, 0, str(self.stack[-y - 1]))
            except:
                break
        self.stdscr.addstr(9, 0, self.message_line)

    def will_it_float(self, str):
        try:
            float(str)
            return True
        except ValueError:
            return False

    def run(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        try:
            while True:
                self.stdscr.clear()
                self.print_stack()
                cmd = self.get_input()
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
                    self.message_line = "division par zéro"
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
