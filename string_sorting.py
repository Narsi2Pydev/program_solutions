import logging
from tkinter import *

logger = logging.getLogger(__name__)

window = Tk()

window.title("Welcome to String Sorting app")

window.geometry('700x500')

lbl = Label(window, text="Enter a sentence to sort")

lbl.grid(column=0, row=0)

txt = Entry(window,width=60)

txt.grid(column=1, row=0)

lbl_1 = Label(window, text="output of sorted string ")

lbl_1.grid(column=0, row=1)

lbl_2 = Label(window, text="")

lbl_2.grid(column=1, row=1)


def sort_the_solution(value=None):
    """
    this function retruns the sorted alphabets in asceding order for test cases or return the value in the app
    :param string_value: input a senctence to this function to run through main function
    :return: string of ascending alphabets
    """
    string_value= value  if value else str(txt.get())
    only_strings = [i.lower() for i in string_value if i.isalpha()]
    for j in range(len(only_strings)):
        for k in range(len(only_strings)):
            if only_strings[j] < only_strings[k]:
                only_strings[j], only_strings[k] = only_strings[k], only_strings[j]

    ordered_alphabets = ''.join(only_strings)
    logger.info(ordered_alphabets)
    if not value:
      lbl_2.configure(text=ordered_alphabets)
    else:
      return ordered_alphabets

def main():
    """
    This has added for  running the program with main function
    :return:
    """
    input_string = input("enter the sring:")
    string_values = sort_the_solution(input_string)
    print(string_values)

btn = Button(window, text="Run sort", command=sort_the_solution)

btn.grid(column=2, row=0)

window.mainloop()

