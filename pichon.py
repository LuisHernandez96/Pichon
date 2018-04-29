import tkinter as tk
import tkinter.scrolledtext as tkst
import subprocess
from tkinter import ttk
from GlobalVars import globals
from tkinter import filedialog

class Bolt(tk.Frame):

    _boltDescription = "Pichon is a programming environment with the purpose of helping people not very familiar with programming concepts to understand them by creating new and fun experiences.\n\nWith Pichon the user is able to create a 3D environment in which he will be able to move around, collect objects and complete a goal, all this while using a friendly high-level programming language. To know more about Bolt functionality, click on the buttons to the left."
    _functionsDescription = "The FUNCTIONS section allows the user to create predefined functions. A function is basically encapsuating several lines of code into a single one that is easier to use.\n\nA function is defined in the following way:\nfunction dataType id(parameters){\n}\n\nLet's define a function to return the square of a number:\nfunction int square(int a){\n    return a * a;\n}\n\nNow all we need to do is call our function like this: square(5) => 25."
    _environmentDescription = "The ENVIRONMENT section is where the user will define how the 3D environment will look like using a set of user-defined and predefined functions, explained more in depth in the Predefined functions section."
    _movementDescription = "The MOVEMENT section is where the user will define how the user will move around the preivously defined environment using a set of user-defined and predefined functions, explained more in depth in the Predefined functions section."
    _predefinedFunctions = "Pichon has several predefined functions that help the user define a 3D environment and move around it.\n\nSome functions can only be used in the ENVIRONMENT section and some of them can only be used in the MOVEMENT section.\n\nMOVEMENT functions:\nup(): Move the player 1 unit up.\ndown(): Move the player 1 unit down.\nforward(): Move the player 1 unit forward.\nturnRight(): Turn the player 90º to the right.\nturnLeft(): Turn the player 90º to the left.\n\nENVIRONMENT functions:\nstart(x, y, z): Defines the (x, y , z) coordinates where the user will first appear.\ngoal(x, y, z): Defines the (x, y, z) coordinates where the user needs to arrive.\nspawnObject(cube|sphere, x, y, z): Places a CUBE object or a SPHERE object at the given (x, y, z) coordinate. CUBE objects act as obstacles to the user, while SPHERE objects act as collectibles that the user needs to pick up before reaching the goal."
    _loopsDescription = "Loops are useful to execute some piece of code several times. Pichon offers two kinds of loops, the For loop and the While loop.\n\nFor example, if the user wants to move forward 10 times:\nUsing a for loop:\nint a;\nfor(a = 0; a < 10; a = a + 1){\n    forward();\n};\n\nUsing a while loop:\nint a = 0;\nwhile(a < 10){\n    forward();\n    a = a + 1;\n};\n"
    _conditionsDescription = "Conditions help the user decide whena given piece of code will execute or not, given certain conditions.\n\nFor example:\nint a = 10;\nint b = 5;\nif(a < b){\n    print(a);\n}\nelse{\n    print(b);\n}"

    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.master = master

        self.menuBar = tk.Menu(self)
        self.fileMenu = tk.Menu(self.menuBar, tearoff = 0)
        self.fileMenu.add_command(label = 'Open', command = self._openFile)
        self.fileMenu.add_command(label = 'Save as...', command = self._saveAs)
        self.menuBar.add_cascade(label = 'File', menu = self.fileMenu)

        self.bolt = tk.Button(self, text="What is Pichon?")
        self.functions = tk.Button(self, text="FUNCTIONS")
        self.environment = tk.Button(self, text="ENVIRONMENT")
        self.movement = tk.Button(self, text="MOVEMENT")
        self.predefined_functions = tk.Button(self, text="Predefined functions")
        self.for_loop = tk.Button(self, text="Loops")
        self.conditions = tk.Button(self, text="Conditions")
        self.help_label = tkst.ScrolledText(self, state = tk.DISABLED, height = 10)
        self.code_editor_label = tk.Label(self, text = "Code editor")
        self.console_label = tk.Label(self, text = "Console")
        self.separator = ttk.Separator(self)
        self._changeHelpText("Click any button on the left to display some help!")

        self.text_area = tkst.ScrolledText(self, height = 20)
        self.console = tkst.ScrolledText(self, state = tk.DISABLED, height = 10)

        self.run = tk.Button(self, text = "Run!", command = self._runProgram)

        self.text_area.insert(tk.END, 
            (
                "FUNCTIONS{\n\n"
                "}"
                "\n\n"
                "ENVIRONMENT{\n\n"
                "}"
                "\n\n"
                "MOVEMENT{\n\n"
                "}"
                "\n"
            )
        )

        self.master.config(menu = self.menuBar)
        self.bolt.grid(row = 0, column = 0, padx = 5)
        self.predefined_functions.grid(row = 0, column = 1, padx = 5)
        self.functions.grid(row = 0, column = 2, padx = 5)
        self.environment.grid(row = 0, column = 3, padx = 5)
        self.movement.grid(row = 0, column = 4, padx = 5)
        self.for_loop.grid(row = 0, column = 5, padx = 5)
        self.conditions.grid(row = 0, column = 6, padx = 5)
        self.help_label.grid(row = 1, column = 0, columnspan = 7, sticky = "we")
        self.separator.grid(row = 2, columnspan = 7, sticky = "we", pady = 10)
        self.code_editor_label.grid(row = 3, columnspan = 7)
        self.text_area.grid(row = 4, column = 0, columnspan = 7, sticky = "we", padx = 10)
        self.run.grid(row = 5, column = 0, pady = 10, ipadx = 5)
        self.console_label.grid(row = 6, columnspan = 7)
        self.console.grid(row = 7, column = 0, columnspan = 7, sticky = "we", padx = 10)

        self.bolt.bind("<Button-1>", self._on_bolt_enter)
        self.functions.bind("<Button-1>", self._on_functions_enter)
        self.environment.bind("<Button-1>", self._on_environment_enter)
        self.movement.bind("<Button-1>", self._on_movement_enter)
        self.predefined_functions.bind("<Button-1>", self._on_predefined_functions_enter)
        self.for_loop.bind("<Button-1>", self._on_for_enter)
        self.conditions.bind("<Button-1>", self._on_conditions_enter)

    def _runProgram(self):
        program = self.text_area.get(1.0, tk.END)
        self.run.config(state = tk.DISABLED)
        tk.Frame.update(self)
        cp = subprocess.run(['python', 'ParserScanner.py', '{}'.format(program)], stdout = subprocess.PIPE)
        message = cp.stdout
        self.run.config(state = tk.NORMAL)
        self.console.config(state = tk.NORMAL)
        self.console.delete(1.0, tk.END)
        self.console.insert(tk.END, message)
        self.console.config(state = tk.DISABLED)

    def _openFile(self):
        self.master.filename =  filedialog.askopenfilename(initialdir = "/", title = "Select a file", filetypes = [("Pichon","*.pichon")])
        if(self.master.filename != ''):
            file = open(self.master.filename, 'r')
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, file.read())
            file.close()

    def _saveAs(self):
        self.master.filename =  filedialog.asksaveasfilename(initialdir = "/", title = "Save as...", filetypes = [("Pichon","*.pichon")])
        file = open(self.master.filename, 'w')
        file.write(self.text_area.get(1.0, tk.END))
        file.close()

    def _changeHelpText(self, helpTxt):
        self.help_label.config(state = tk.NORMAL)
        self.help_label.delete(1.0, tk.END)
        self.help_label.insert(tk.END, helpTxt)
        self.help_label.config(state = tk.DISABLED)

    def _on_bolt_enter(self, event):
        self._changeHelpText(self._boltDescription)

    def _on_functions_enter(self, event):
        self._changeHelpText(self._functionsDescription)

    def _on_environment_enter(self, event):
        self._changeHelpText(self._environmentDescription)

    def _on_movement_enter(self, event):
        self._changeHelpText(self._movementDescription)

    def _on_predefined_functions_enter(self, event):
        self._changeHelpText(self._predefinedFunctions)

    def _on_for_enter(self, event):
        self._changeHelpText(self._loopsDescription)

    def _on_conditions_enter(self, event):
        self._changeHelpText(self._conditionsDescription)

if __name__ == "__main__":
    root = tk.Tk()
    #w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    #root.geometry("%dx%d+0+0" % (w, h))
    Bolt(root).grid()
    root.mainloop()
