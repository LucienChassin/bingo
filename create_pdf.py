


from copy import deepcopy
from pathlib import Path
import json
from random import shuffle
import random
from typing import List

DELEGATION = json.loads(Path("delegation.json").read_text('utf-8'))
CUSTOM = [
    "Plan tour eiffel", "Macron !!", "Drapeau algérien",
    "Drapeau breton", "Antoine dupont", "Un espoir français", "Il pleut",
    "Celine", "Aya Nakamura", "Plan d'un enfant mignon content","plan d'un plonguer",
    "Anne Hidalgo et la seine","Blaque de Nelson Montfort","Bisous d'une fille à la caméra",
    "Coeur à la caméra","Mec qui tire la geule","Notre Dame","La flamme"
]
NB_WORDS = 16
NB_DELEGATION = 6
NB_CUSTOM = NB_WORDS - NB_DELEGATION

DRINK = {
     'red':('double shot',[1]),
 'green':('donne 3 gorgée',[2,3,4]),
 'black':('prend 3 gorgée',[5,6,7]),
 'purple':('shot',[8,9]),
 'pink':('donne 1 shot',[10,11]),
}


def choose_color() -> str:
    i = random.randint(1,11)
    for k,(v,u) in DRINK.items():
        if i in u:
            return k
    raise NotImplementedError

def set_cell_color(pdf, color):
    if color == 'red':
        pdf.set_text_color(255, 0, 0)
    elif color == 'green':
        pdf.set_text_color(0, 255, 0)
    elif color == 'black':
        pdf.set_text_color(0, 0, 0)
    elif color == 'purple':
        pdf.set_text_color(128, 0, 128)
    elif color == 'pink':
        pdf.set_text_color(255, 192, 203)


def create_words() -> List[str]:
    delegation = deepcopy(DELEGATION)
    shuffle(delegation)
    delegation = iter(delegation)
    deleg=[]
    while len(deleg)<NB_DELEGATION:
        pays = next(delegation)
        if  len(pays)<20:
            deleg.append(pays)
        
    custom = deepcopy(CUSTOM)
    shuffle(custom)
    custom = custom[:NB_CUSTOM]
    
    
    
    words = custom + deleg
    shuffle(words)
    
    return words


from typing import List
import pandas as pd
from fpdf import FPDF



def create_pdf(words:List[str]):
    assert len(words) == NB_WORDS
    # Shuffle the words to randomize the bingo card
    import random
    random.shuffle(words)
    nb_col = 4
    nb_line = len(words) // nb_col
    assert nb_col * nb_line - len(words) ==0
    # Create a 4x4 grid for the bingo card
    grid = [words[i:i+nb_col] for i in range(0, len(words), nb_col)]



    # Create a DataFrame from the grid
    bingo_df = pd.DataFrame(grid)

    # Display the DataFrame
    print(bingo_df)

    # Create PDF in landscape mode
    class PDF(FPDF):
        def __init__(self):
            super().__init__(orientation='L')
        
        def header(self):
            set_cell_color(self,"black")
            self.image('logo_left.png', 10, 8, 33)
            self.image('logo_right.png', self.w - 43, 8, 33)
            self.set_font('Arial', 'B', 28)
            # self.cell(0, 30, 'Bingo JO', 0, 1, 'C')
            self.image('bingo.jpg', self.w/2-55, 8, 100)
            self.ln(40)

        def footer(self):
            
            self.set_y(-15)
            self.set_font('Arial', 'I', 16)
            cell_width = self.w / len(DRINK)
            for i,(k,(v,u)) in enumerate(DRINK.items()):
                set_cell_color(self,k)
                self.set_x(self.w - cell_width * (len(DRINK) - i))
                self.cell(cell_width, 10, f'{k}: {v}', 0, 0, 'C')

        def create_bingo_card(self, data):
            self.add_page()
            self.set_font('Arial', 'B', 12)
            
            # Set table size to fill most of the page, leaving space for title and footer
            margin = 10
            available_height = self.h - self.get_y() - margin - 15  # 15 units for footer space
            available_width = self.w - 2 * margin
            
            col_width = available_width / nb_col
            row_height = available_height / nb_line

            # Calculate starting x position to center the table
            start_x = margin

            self.set_y(self.get_y())

            for row in data:
                self.set_x(start_x)
                for item in row:
                    
                    set_cell_color(self,choose_color())
                    self.cell(col_width, row_height, item,border=1, align='C')
                self.ln(row_height)

    pdf = PDF()
    pdf.create_bingo_card(grid)
    pdf_output = "bingo_card_landscape_filled.pdf"
    pdf.output(pdf_output)

    print(f"Bingo card created: {pdf_output}")
    
if __name__ == "__main__":
    create_pdf(create_words())