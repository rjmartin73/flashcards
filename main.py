from tkinter import Button, Label, PhotoImage, Canvas, Tk, Entry
from tkinter import END, NW, W, E, S, N, ttk
import pandas as pd
import json
import random
import time
deck_name = ""
questions = {}
charmap = "utf8"
chosen_card = ""
deck = {}

# CONSTANTS
BG_COLOR = "#B1DDC6"
TEXT_COLOR = "#656565"


# create deck file from csv to json
def create_deck():
    """
    Create a question/answer deck from a csv file.
    Format of the csv should be in the form of:
    Question Header,Answer Header
    question1,answer1
    question2,answer2
    etc.
    """
    file = open(f"data/{deck_name}.csv", "r", encoding=charmap)
    data = pd.read_csv(file)
    print(data)
    _deck_name = file.name.split("/", 1)
    _deck_name = _deck_name[1].replace(".csv", "")
    deck_description = "Top 100 most common Spanish words"
    question_header = data.columns[0]
    answer_header = data.columns[1]
    print(deck_name, deck_description)
    record = {
                "deck": deck_name,
                "description": deck_description,
                "question_header": question_header,
                "answer_header": answer_header,
                "questions": {}
    }

    details = None
    for row in data.itertuples():
        q_num = row[0]
        question = row[1]
        answer = row[2]
        update = {f"question_number_{q_num}": {"question": question,
                                               "answer": answer,
                                               "know_it": 0
                                               }
                  }
        record["questions"].update(update)

    data_file = open(f"data/{deck_name}.json", "w")
    json.dump(record, data_file, indent=4)
    data_file.close()


def load_deck(file_name: str):
    global questions, deck
    file_name = f"data/{file_name}.json"
    data = open(file_name)
    deck = json.load(data)
    questions = deck["questions"]
    print(deck)


def next_question(know_it: int, question_num: int):
    global questions, deck, chosen_card

    if know_it:
        questions[chosen_card]["know_it"] = 1
        print(questions[chosen_card])

    card_no = random.randint(0, len(questions) - 1)
    chosen_card = f"question_number_{card_no}"
    print(chosen_card)
    while questions[chosen_card]["know_it"] == 1:
        card_no = random.randint(0, len(deck) - 1)
        chosen_card = f"question_number_{card_no}"
    card = questions[chosen_card]

    canvas.delete("header_text")
    canvas.delete("value_text")
    canvas.delete("bg_image")
    canvas.create_image(10, 10, image=canvas_image_f, anchor=NW, tags=["bg_image"])
    canvas.create_text(400, 150, fill=TEXT_COLOR, text=deck["question_header"].title()
                       , font=("Arial", 40, "italic"), tags=["header_text"])
    q = card["question"]
    a = card["answer"]
    canvas.create_text(400, 263, fill=TEXT_COLOR, text=q, font=("Arial", 60, "bold"),
                       tags=["value_text"])
    window.update()
    time.sleep(5)
    canvas.delete("header_text")
    canvas.delete("value_text")
    canvas.delete("bg_image")
    canvas.create_image(10, 10, image=canvas_image_r, anchor=NW, tags=["bg_image"])
    canvas.create_text(400, 150, fill=TEXT_COLOR, text=deck["answer_header"].title(),
                       font=("Arial", 40, "italic"), tags=["header_text"])
    canvas.create_text(400, 263, fill=TEXT_COLOR, text=a, font=("Arial", 60, "bold")
                       , tags=["value_text"])


def start_session(file_name: str):
    global questions
    load_deck(file_name)
    next_question(0, 0)


def close_win():
    global deck_name
    deck_name = user_form_entry.get()
    user_form.destroy()


# --------------------------- UI Setup --------------------------- #
user_form = Tk()
user_form.config(width=400, height=400)
user_form_label = Label(user_form, text="Which deck would you like to use?")
user_form_entry = Entry(user_form)
user_form_button = Button(user_form, text="ok", command=close_win)

user_form_label.pack()
user_form_entry.pack()
user_form_button.pack()
user_form.mainloop()


window = Tk()
window.title(f"Flashy-{deck_name.replace('_', ' ').title()}")
window.config(background=BG_COLOR, pady=50, padx=50)

canvas_image_f = PhotoImage(file="images/card_front.png")
canvas_image_r = PhotoImage(file="images/card_back.png")

right_image = PhotoImage(file="images/right.png")
right_button = Button(window, image=right_image, highlightthickness=0, border=0, borderwidth=0,
                      command=lambda: next_question(1, 1))
right_button.grid(column=2, row=2, sticky=N)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(window, image=wrong_image, highlightthickness=0, border=0, borderwidth=0,
                      command=lambda: next_question(0, 0))
wrong_button.grid(column=1, row=2, sticky=N)

canvas = Canvas(window, width=800, height=526, highlightthickness=0, background=BG_COLOR)

card_image = canvas.create_image(10, 10, image=canvas_image_f, anchor=NW, tags=["bg_image"])
header_text = canvas.create_text(400, 150, fill=TEXT_COLOR, text="Flash", font=("Arial", 40, "italic")
                                 , tags=["header_text"])
value_text = canvas.create_text(400, 263, fill=TEXT_COLOR, text="Cards", font=("Arial", 60, "bold")
                                , tags=["value_text"])

canvas.grid(row=1, column=1, columnspan=2, sticky=NW)
# create_deck()
start_session(deck_name)

if __name__ == '__main__':
    window.mainloop()


