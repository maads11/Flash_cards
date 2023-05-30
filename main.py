
import tkinter
import pandas
import random
import list_integers
BACKGROUND_COLOR = "#B1DDC6"
# main window
root_window = tkinter.Tk()
root_window.geometry('800x650')
root_window.title('The FLash Card Project')
root_window.configure(bg=BACKGROUND_COLOR)
# dataframes
data = pandas.read_csv('data/french_words.csv')
copy = pandas.read_csv('data/french_words.csv')
# list of integers for smooth search of index
int_list = list_integers.generate_list()
# canvas
canvas = tkinter.Canvas(root_window, width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
# canvas images
back_card_image = tkinter.PhotoImage(file='images/card_back.png')
front_card_image = tkinter.PhotoImage(file='images/card_front.png')
front = canvas.create_image(410, 270, image=front_card_image)

canvas.grid(column=0, row=0, sticky='N')

# canvas titles
title = canvas.create_text(400, 140, text='Language', font=('arial', 20, 'bold', 'italic'))
word = canvas.create_text(400, 300, text='Word', font=('Arial', 20, 'bold'))


def right_answer():
    canvas.itemconfig(front, image=front_card_image)
    rand_int = random.choice(int_list)
    random_word = [data.loc[rand_int, 'French'], data.loc[rand_int, 'English']]
    index_num = data.index[data['French'] == data.loc[rand_int, 'French']].tolist()[0]
    canvas.itemconfig(title, text='French')
    canvas.itemconfig(word, text=f'{random_word[0]}')
    # Copy a row from the source DataFrame to the destination DataFrame

    data.drop(index=index_num, inplace=True)
    int_list.remove(index_num)


def wrong_answer():
    try:
        if canvas.itemcget(title, 'text') == 'French':
            foreign_key = canvas.itemcget(word, 'text')
            val = copy.loc[copy["French"] == foreign_key].values[0]
            canvas.itemconfig(front, image=back_card_image)
            canvas.itemconfig(title, text='English')
            canvas.itemconfig(word, text=f'{val[1]}')
        elif canvas.itemcget(title, 'text') == 'English':
            foreign_key = canvas.itemcget(word, 'text')
            val = copy.loc[copy["English"] == foreign_key].values[0]
            canvas.itemconfig(front, image=front_card_image)
            canvas.itemconfig(title, text='French')
            canvas.itemconfig(word, text=f'{val[0]}')

    except IndexError:
        pass


# button to use when you know the word
image_button_no = tkinter.PhotoImage(file='images/wrong.png')
button_no = tkinter.Button(image=image_button_no, command=wrong_answer)
button_no.grid(column=0, row=1, sticky='W', padx=50)

# button to use when you don't know the word
image_button_yes = tkinter.PhotoImage(file='images/right.png')
button_yes = tkinter.Button(image=image_button_yes, command=right_answer)
button_yes.grid(column=0, row=1, sticky='E', padx=50)

root_window.mainloop()
