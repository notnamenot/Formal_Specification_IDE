from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

MAX_WIDTH = 600
MAX_HEIGHT = 800


class FrameUC(LabelFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, text="Use Case Diagram", *args, **kwargs)

        self.images = []

        self.frame_import_UC = Frame(self)
        self.frame_import_UC.pack()

        self.btn_import_image = Button(self.frame_import_UC, text="Import", command=self.open_file)
        self.btn_import_image.pack(side=LEFT)

        self.btn_prev = Button(self.frame_import_UC, text="<", state=DISABLED, command=lambda: self.prev_uc_clicked(0))
        self.btn_prev.pack(side=LEFT)

        self.lbl_filename = Label(self.frame_import_UC, text="")
        self.lbl_filename.pack(side=LEFT)

        self.btn_next = Button(self.frame_import_UC, text=">", state=DISABLED, command=lambda: self.next_uc_clicked(1))
        self.btn_next.pack(side=LEFT)

        self.img = ImageTk.PhotoImage(Image.open("uc_place_holder.png"))  # TODO wrzucić to shape
        self.panel = Label(self, image=self.img)
        self.panel.pack()

    def open_file(self):
        filename = filedialog.askopenfilename(initialdir=".", title="Select file", filetypes=(("all files", "*.*"),
                                                                                              ("png files", "*.png"),
                                                                                              ("jpg files", "*.jpg"),
                                                                                              ("jpeg files", "*.jpeg")))
        if not filename or filename in self.images:
            return

        self.set_uc_img(filename)
        self.images.append(filename)

        self.btn_next.configure(state=DISABLED)

        if len(self.images) > 1:
            self.btn_prev.configure(state=NORMAL)
            self.btn_prev.configure(command=lambda: self.prev_uc_clicked(len(self.images) - 2))  # przedostatni

        print("images", self.images)

    def set_uc_img(self, filename):
        self.lbl_filename.configure(text=filename)

        i = Image.open(filename)

        # print(i.size)  # 0 - width, 1 - height
        if i.size[0] > MAX_WIDTH:
            width_perc = (MAX_WIDTH / float(i.size[0]))
            height_size = int((float(i.size[1]) * float(width_perc)))
            i = i.resize((MAX_WIDTH, height_size), Image.ANTIALIAS)
        if i.size[1] > MAX_HEIGHT:
            height_perc = (MAX_HEIGHT / float(i.size[1]))
            width_size = int((float(i.size[0]) * float(height_perc)))
            i = i.resize((width_size, MAX_HEIGHT), Image.ANTIALIAS)

        img2 = ImageTk.PhotoImage(i)

        self.panel.configure(image=img2)
        self.panel.image = img2

    def next_uc_clicked(self, image_number):
        print("image_number", image_number)

        self.btn_prev.configure(command=lambda: self.prev_uc_clicked(image_number - 1))
        self.btn_next.configure(command=lambda: self.next_uc_clicked(image_number + 1))
        if image_number == len(self.images) - 1:
            self.btn_next.configure(state=DISABLED)
        self.btn_prev.configure(state=NORMAL)

        self.set_uc_img(self.images[image_number])

    def prev_uc_clicked(self, image_number):
        print("image_number", image_number)

        # self.grid_forget()

        self.btn_prev.configure(command=lambda: self.prev_uc_clicked(image_number - 1))
        self.btn_next.configure(command=lambda: self.next_uc_clicked(image_number + 1))
        if image_number == 0:
            self.btn_prev.configure(state=DISABLED)
        self.btn_next.configure(state=NORMAL)

        self.set_uc_img(self.images[image_number])
