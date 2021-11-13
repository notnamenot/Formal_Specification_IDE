# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
# import Image

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    root = Tk()     # root window
    root.title("IDE XD")

    frame1_UC = LabelFrame(root, text="Use Case Diagram", padx=10, pady=10)
    frame2_scenario = LabelFrame(root, text="Scenarios", padx=10, pady=10)
    frame3_flowchart = LabelFrame(root, text="Flowchart")

    frame1_UC.grid(row=0, column=0)
    frame2_scenario.grid(row=0, column=1)
    frame3_flowchart.grid(row=0, column=2)


    #################### FRAME1 - UC Diagram ####################

    def open_file():
        frame1_UC.filename = filedialog.askopenfilename(initialdir=".", title="Select file", filetypes=(("png files", "*.png"), ("all files", "*.*")))
        filename = frame1_UC.filename
        lbl_filename = Label(frame1_UC, text=filename)
        lbl_filename.pack()     # grid(row=0, column=0)
        global img_UC
        img_UC = ImageTk.PhotoImage(Image.open(filename))
        global lbl_img
        lbl_img = Label(frame1_UC, image=img_UC) # width=100
        lbl_img.pack()      #grid(row=1, column=0)


    btn_import_image = Button(frame1_UC, text="Import", command=open_file)
    btn_import_image.pack()


    #################### FRAME2 - SCENARIOS ####################

    frame_input_scenario = LabelFrame(frame2_scenario)
    frame_input_scenario.pack()

    input_scenario = Entry(frame_input_scenario, width=50, borderwidth=3)
    input_scenario.grid(row=0,column=0)  # columnspan=3, , sticky=W+E
    # input_scenario.pack(anchor=N)
    input_scenario.insert(0, "Enter scenario...")

    def add_scenario_clicked():
        scenario = input_scenario.get()
        words = scenario.split()    # defaul split on any whitespace
        print(words)
        global btns
        btns = []

        global frame_splited_scenario
        frame_splited_scenario = LabelFrame(frame2_scenario)
        frame_splited_scenario.pack()

        for i in range(len(words)):
            btn = Button(frame_splited_scenario, text=words[i])
            btn.grid(row=0, column=i)
            btns.append(btn)



    btn_add_scenario = Button(frame_input_scenario, text="Add", command=add_scenario_clicked)
    btn_add_scenario.grid(row=0, column=1)





    # root.filename = filedialog.askopenfilename(initialdir=".", title="Select file", filetypes=(("png files", "*.png"), ("all files", "*.*")))
    # filename = Label(frame1_UC, text=root.filename).grid(row=0, column=0)
    #
    # uc_img = ImageTk.PhotoImage(Image.open(root.filename))
    # lbl_img = Label(frame1_UC, image=uc_img, width=100)
    # lbl_img.grid(row=1, column=0)


    # option = StringVar()
    # option.set("Menu") # default
    # dropdown_menu = OptionMenu(frame1_UC, option, "Import")
    # dropdown_menu.grid(row=0, column=0)

    # def myClick():
    #     # myLbl = Label(root, text="Hurra", fg="blue", bg="red") # .pack dodawało by kolejne!!
    #     myLbl = Label(root, text=e.get(), fg="blue", bg="red") # .pack dodawało by kolejne!!
    #     #myLbl.config(text = e.get())
    #     myLbl.grid(row=4, column=4)
    #
    #
    # #creating a label WIdget
    # myLabel1 = Label(root, text="Hello world!", bd=1, relief=SUNKEN, anchor=E)
    # myLabel2 = Label(root, text="Hello galaxy!")
    #
    # myButton = Button(root, text="Enter scenario:", state=NORMAL, padx=50, command=myClick).grid(row=3,column=3) # DISEABLED
    #
    #
    # # shoving it  onto screen
    # #myLabel.pack()
    # myLabel1.grid(row=0, column=0, columnspan=2) # west+ east
    # myLabel2.grid(row=1, column=1)
    #
    #
    # e = Entry(root, width=50, borderwidth=3)
    # e.grid(row=6,column=5, sticky=W+E )#columnspan=3
    # e.insert(0,"hint")
    #
    # def buttonClicked(slowo):
    #     e.delete(0,END)
    #     e.insert(0,slowo)
    #
    # passParamBtn = Button(root, text="slowo", command=lambda: buttonClicked(e.get()+"!"))
    # passParamBtn.grid(row=3,column=0)
    #
    #
    # uc_img = ImageTk.PhotoImage(Image.open("top-level-use-cases-7699.png"))
    # lbl_img = Label(image=uc_img, width=100)
    # lbl_img.grid(row=6,column=2)

    root.mainloop()
