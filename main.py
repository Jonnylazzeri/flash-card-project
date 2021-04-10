from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

data = pandas.read_csv('./data/german_english_flash.csv')
words_to_learn = ''

word = ''
data_dict = {}

if words_to_learn:
    to_learn = words_to_learn.to_dict(orient='records')
else:
    to_learn = data.to_dict(orient='records')



def change_side():
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(lang_text, text="English", fill='white')
    canvas.itemconfig(word_text, text=word["English"], fill='white')


def change_word():
    global word, flip_timer
    window.after_cancel(flip_timer)
    canvas.itemconfig(canvas_image, image=card_front)
    word = random.choice(to_learn)
    canvas.itemconfig(lang_text, text="German", fill='black')
    canvas.itemconfig(word_text, text=word["German"], fill='black')
    flip_timer = window.after(3000, change_side)


def right_guess():
    change_word()
    to_learn.remove(word)
    global data_dict
    data_dict = {
        'German': [blah["German"] for blah in to_learn],
        'English': [blah["English"] for blah in to_learn]
    }
    global words_to_learn
    d = pandas.DataFrame(data_dict)
    words_to_learn = d.to_csv("./data/words_to_learn.csv", index=False)



LANG_FONT = ("Ariel", 40, "italic")
WORD_FONT = ("Ariel", 60, "bold")

window = Tk()
flip_timer = window.after(3000, change_side)
window.title("German Flash")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file='./images/card_front.png')
card_back = PhotoImage(file='./images/card_back.png')
canvas_image = canvas.create_image(400, 263, image=card_front)
lang_text = canvas.create_text(400, 150, font=LANG_FONT)
word_text = canvas.create_text(400, 263, font=WORD_FONT)
canvas.grid(row=0, column=0, columnspan=2)

right_image = PhotoImage(file="./images/right.png")
wrong_image = PhotoImage(file="./images/wrong.png")
right_button = Button(image=right_image, borderwidth=0, highlightthickness=0, command=right_guess)
right_button.grid(row=1, column=1)
wrong_button = Button(image=wrong_image, borderwidth=0, highlightthickness=0, command=change_word)
wrong_button.grid(row=1, column=0)

change_word()

window.mainloop()
