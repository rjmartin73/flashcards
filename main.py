from tkinter import Button, Label, PhotoImage, Canvas, Tk
from tkinter import END, NW, W, E, S, N, ttk
import pandas as pd
import json

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
    file = open("data/french_words.csv", "r")
    data = pd.read_csv(file)
    _deck_name = file.name.split("/", 1)
    _deck_name = _deck_name[1].replace(".csv", "")
    deck_description = "Top 100 most common french words"
    question_header = data.columns[0]
    answer_header = data.columns[1]
    print(deck_name)
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


# --------------------------- UI Setup --------------------------- #
deck_name = "french_words"

window = Tk()
window.title(f"Flashy-{deck_name.replace('_', ' ').title()}")
window.config(background=BG_COLOR, pady=50, padx=50)

canvas_image_f = PhotoImage(file="images/card_front.png")
canvas_image_r = PhotoImage(file="images/card_back.png")

right_image = PhotoImage(file="images/right.png")
right_button = Button(window, image=right_image, highlightthickness=0, border=0, borderwidth=0)
right_button.grid(column=2, row=2, sticky=N)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(window, image=wrong_image, highlightthickness=0, border=0, borderwidth=0)
wrong_button.grid(column=1, row=2, sticky=N)

canvas = Canvas(window, width=800, height=526, highlightthickness=0, background=BG_COLOR)

card_image = canvas.create_image(10, 10, image=canvas_image_f, anchor=NW)
header_text = canvas.create_text(400, 150, fill=TEXT_COLOR, text="header", font=("Arial", 40, "italic"))
value_text = canvas.create_text(400, 263, fill=TEXT_COLOR, text="value", font=("Arial", 60, "bold"))


canvas.grid(row=1, column=1, columnspan=2, sticky=NW)

if __name__ == '__main__':
    window.mainloop()