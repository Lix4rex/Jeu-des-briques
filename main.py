from tkinter import *
import tkinter.font as font

class Space():
    def __init__(self, window, height):
        self.label = Label(window, text = "", height = height)
        self.label.pack()


fen = Tk()
fen.title("42")

fen.geometry("600x600")

game_frame = Frame(fen)

current_game = "3x3"


### Shape of grid game
row = 3
column = 3
case_matrix = []


canvas_info = Canvas(game_frame, bg = "red", height = 100, width = 500)

nb_attempt = 0
nb_attempt_info = canvas_info.create_text(100, 50, text = str(nb_attempt) + " attempt", font = font.Font(family = "Times New Roman", size = 18, weight = "bold"))

win_info = canvas_info.create_text(250, 50, text = "", font = font.Font(family = "Times New Roman", size = 18, weight = "bold"))

fichier = open("scores.txt", "r")
temp = fichier.read()
fichier.close()

chaines_scores = temp.split("\n")
print(chaines_scores)
dico_scores = {}
for elt in chaines_scores:
    if len(elt) >= 7:
        dico_scores[elt[0:3]] = int(elt[6:])

bestscore_info = canvas_info.create_text(380, 50, text = "Best", font = font.Font(family = "Times New Roman", size = 18, weight = "bold"))


canvas_info.pack()

Space(game_frame, 6)

grid_frame = Frame(game_frame)

win = False
 


def check_end():
    global win
    for i in range(row):
        for j in range(column):
            if not(case_matrix[i][j].activate):
                return False
            
    ### it's win here, every case is activated ###
    win = True
    canvas_info.itemconfig(win_info, text = "YOU WIN !!")
    canvas_info.configure(bg = "green")

    if nb_attempt < dico_scores[current_game] or dico_scores[current_game] < 0:
        dico_scores[current_game] = nb_attempt

    fichier = open("scores.txt", "w")
    for key, value in dico_scores.items():
        fichier.write(key + " : " + str(value) + "\n")
    fichier.close()


    return True

class ButtonGame():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.activate = False
        self.neighbors = []
        self.button = Button(grid_frame, text = "", bg = "white", command = self.change, height = 2, width = 4)
        self.button.grid(row = self.x, column = self.y)

    def change(self):
        global nb_attempt

        if not(win):
            nb_attempt += 1
            temp = str(nb_attempt) + " attempt"
            if nb_attempt > 1:
                temp += "s"
            canvas_info.itemconfig(nb_attempt_info, text = temp)
            self.activate = not(self.activate)
            if self.activate :
                self.button.config(bg = "orange")
            else:
                self.button.config(bg = "white")

            for case in self.neighbors:
                case.activate = not(case.activate)
                if case.activate:
                    case.button.config(bg = "orange")
                else:
                    case.button.config(bg = "white")

            check_end()


grid_frame.pack()



### FIRST WINDOW ###


main = Frame(fen)

Space(main, 20)


options = Frame(main)


options_list = ["3x3", "5x5", "7x7", "9x9"]

value_inside = StringVar(options)
value_inside.set("3x3")  

question_menu = OptionMenu(options, value_inside, *options_list) 
question_menu.config(fg = "white", bg = "black", font = font.Font(family = "Times New Roman", size = 18, weight = "bold"))
question_menu.pack() 


options.pack()


def begin_game():
    global row, column, case_matrix, current_game

    current_game = value_inside.get()
    canvas_info.itemconfig(bestscore_info, text = "Best : " + str(dico_scores[value_inside.get()]))

    row = int(value_inside.get()[0])
    column = int(value_inside.get()[2])

    case_matrix = [[ButtonGame(i, j) for j in range(column)] for i in range(row)]
    for i in range(row):
        for j in range(column):
            if i == 0:
                if j == 0:
                    case_matrix[i][j].neighbors.append(case_matrix[i][j+1])
                    case_matrix[i][j].neighbors.append(case_matrix[i+1][j])
                elif j == column - 1:
                    case_matrix[i][j].neighbors.append(case_matrix[i][j-1])
                    case_matrix[i][j].neighbors.append(case_matrix[i+1][j])
                else:
                    case_matrix[i][j].neighbors.append(case_matrix[i][j-1])
                    case_matrix[i][j].neighbors.append(case_matrix[i][j+1])
                    case_matrix[i][j].neighbors.append(case_matrix[i+1][j])
            elif i == row - 1:
                if j == 0:
                    case_matrix[i][j].neighbors.append(case_matrix[i-1][j])
                    case_matrix[i][j].neighbors.append(case_matrix[i][j+1])
                elif j == column - 1:
                    case_matrix[i][j].neighbors.append(case_matrix[i-1][j])
                    case_matrix[i][j].neighbors.append(case_matrix[i][j-1])
                else:
                    case_matrix[i][j].neighbors.append(case_matrix[i-1][j])
                    case_matrix[i][j].neighbors.append(case_matrix[i][j-1])
                    case_matrix[i][j].neighbors.append(case_matrix[i][j+1])
            else:
                if j == 0:
                    case_matrix[i][j].neighbors.append(case_matrix[i-1][j])
                    case_matrix[i][j].neighbors.append(case_matrix[i][j+1])
                    case_matrix[i][j].neighbors.append(case_matrix[i+1][j])
                elif j == column - 1:
                    case_matrix[i][j].neighbors.append(case_matrix[i-1][j])
                    case_matrix[i][j].neighbors.append(case_matrix[i][j-1])
                    case_matrix[i][j].neighbors.append(case_matrix[i+1][j])
                else:
                    case_matrix[i][j].neighbors.append(case_matrix[i-1][j])
                    case_matrix[i][j].neighbors.append(case_matrix[i][j-1])
                    case_matrix[i][j].neighbors.append(case_matrix[i][j+1])
                    case_matrix[i][j].neighbors.append(case_matrix[i+1][j])

    game_frame.pack()
    main.pack_forget()

Space(main, 4)

play_button = Button(main, command = begin_game, text = "PLAY", fg = "blue", bg = "black", font = font.Font(family = "Times New Roman", size = 30, weight = "bold"))
play_button.pack()


main.pack()



fen.mainloop()