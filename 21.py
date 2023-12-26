import tkinter as tk
from tkinter import messagebox

class Baralho:
    cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    valcards = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    naipe = ['Copas', 'Espadas', 'Ouros', 'Paus']
    cardvals = dict(zip(cards, valcards))
    
class Players:
    jogador1 = ['Jogador 1']
    jogador2 = ['Jogador 2']
    on_hold = False
    
class Valores:
    valor_placar_player1 = 0
    valor_placar_player2 = 0


def create_toplevel(master, title, size):
    toplevel = tk.Toplevel(master)
    toplevel.title(title)
    toplevel.geometry(size)
    return toplevel
    
def interface_init():
    global janela
    
    janela = tk.Tk()
    janela.title('Jogar 21')
    janela.geometry('200x70+100+100')
    
    j1var = tk.StringVar()
    j2var = tk.StringVar()
    
    jogador1_label = tk.Label(janela, text= 'Jogador Nº 1')
    jogador2_label = tk.Label(janela, text= 'Jogador Nº 2')
    jogador1_entry = tk.Entry(janela, width= 12, textvariable= j1var)
    jogador2_entry = tk.Entry(janela, width= 12, textvariable= j2var)
    confirm_button = tk.Button(janela, width= 8, height= 1, text= 'Confirmar', command = lambda: init_confirm(j1var, j2var, janela), bg = 'Chartreuse', fg= 'black')
    
    jogador1_label.place(x= 5, y= 2)
    jogador2_label.place(x= 110, y= 2)
    jogador1_entry.place(x= 5, y= 20)
    jogador2_entry.place(x= 110, y= 20)
    confirm_button.place(x= 65, y= 43)
    
    janela.mainloop()

def init_confirm(j1var, j2var, janela):
    j1 = j1var.get()
    j2 = j2var.get()
    if j1 == '' and j2 == '':
        del Players.jogador1[0]
        del Players.jogador2[0]
        Players.jogador1.insert(0, 'Jogador 1')
        Players.jogador2.insert(0, 'Jogador 2')
        pass
    if j1 != '' and j2 == '':
        del Players.jogador1[0]
        Players.jogador1.insert(0, j1)
    if j1 == '' and j2 != '':
        del Players.jogador2[0]
        Players.jogador2.insert(0, j2)
    if j1 != '' and j2 != '':
        del Players.jogador1[0]
        Players.jogador1.insert(0, j1)
        del Players.jogador2[0]
        Players.jogador2.insert(0, j2)
    
    interface_game(janela)
    
def game_play_time_check(lista_botao_atual, lista_botao_seguinte):
    for botao in lista_botao_atual:
        botao['state'] = 'disabled'
        botao['bg'] = 'Silver'
    for botao in lista_botao_seguinte:
        botao['state'] = 'normal'
        botao['bg'] = 'Red'
    lista_botao_seguinte[0].focus()

def game_card_pull():
    import random
    for i in range(0, random.randint(1, 15)):
        carta = random.choice(Baralho.cards)
    cartaval = Baralho.cardvals[carta]
    return cartaval

def on_click_puxar_carta(label_p1, label_p2, lista_botao_atual, lista_botao_seguinte, game, playtime):
    if playtime == 'Jogador 1':
        p1 = Players.jogador1[0]
        p2 = Players.jogador2[0]
    else:
        p1 = Players.jogador2[0]
        p2 = Players.jogador1[0]
    if Players.on_hold == False:
        labelget = label_p1.cget('text')
        valcard = game_card_pull()
        label_p1['text'] = str(int(labelget) + valcard)
        if int(label_p1['text']) == '21':
            messagebox.showinfo('Vitória', f'{p1} venceu!', parent= game)
            play_again(game, p1)
        elif int(label_p1['text']) > 21:  
            messagebox.showinfo('Derrota', f'{p2} venceu!', parent= game)
            play_again(game, p2)
        elif int(label_p1['text']) < 21:
            game_play_time_check(lista_botao_atual, lista_botao_seguinte)
    else:
        label_1 = label_p1.cget('text')
        label_2 = label_p2.cget('text')
        valcard = game_card_pull()
        label_p1['text'] = str(int(label_1) + valcard)
        if int(label_p1['text']) == '21':
            messagebox.showinfo('Vitória', f'{p1} venceu!', parent= game)
            Players.on_hold = False
            play_again(game, p1)
        elif int(label_p1['text']) > 21:  
            messagebox.showinfo('Derrota', f'{p2} venceu!', parent= game)
            Players.on_hold = False
            play_again(game, p2)
        elif int(label_p1['text']) > int(label_2):
            messagebox.showinfo('Vitória', f'{p1} venceu!', parent= game)
            Players.on_hold = False
            play_again(game, p1)
        elif int(label_p1['text']) < 21 and int(label_p1['text']) < int(label_2) or int(label_p1['text']) == int(label_2):
            game_play_time_check(lista_botao_atual, lista_botao_seguinte)
            Players.on_hold = False
        
def on_click_manter_carta(lista_botao_atual, lista_botao_seguinte, label_p1, label_p2, game, playtime):
    if Players.on_hold == False:
        Players.on_hold = True
        game_play_time_check(lista_botao_atual, lista_botao_seguinte)
    else:
        if playtime == 'Jogador 1':
            p1 = Players.jogador1[0]
            p2 = Players.jogador2[0]
        else:
            p1 = Players.jogador2[0]
            p2 = Players.jogador1[0]
        label_1 = label_p1.cget('text')
        label_2 = label_p2.cget('text')
        if int(label_1) > int(label_2):
            messagebox.showinfo('Vitória', f'{p1} venceu!', parent= game)
            Players.on_hold = False
            play_again(game, p1)
        elif int(label_1) < int(label_2):
            messagebox.showinfo('Vitória', f'{p2} venceu!', parent= game)
            Players.on_hold = False
            play_again(game, p2)
        elif int(label_1) == int(label_2):
            messagebox.showinfo('Empate', 'Empate!', parent= game)
            Players.on_hold = False
            play_again(game, 'Empate')
    
def interface_game(janela):
    
    game = create_toplevel(janela, 'Jogo', '300x270+67+102')
    game.resizable(False, False)
    game.grab_set()
    
    frame = tk.Frame(game, width= 300, height= 50, borderwidth= 2, relief= 'groove')
    frame2 = tk.Frame(game, width= 300, height= 220, borderwidth= 2, relief= 'groove', bg= 'Olive')
    frame.pack()
    frame2.pack()
    
    j1_placar = tk.Label(frame, text= Players.jogador1[0])
    j1_placar_val = tk.Label(frame, text= Valores.valor_placar_player1)   
    j2_placar = tk.Label(frame, text= Players.jogador2[0])   
    j2_placar_val = tk.Label(frame, text= Valores.valor_placar_player2)   
    
    j1_placar.place(x= 5, y= 2)
    j1_placar_val.place(x= 20, y= 20)
    j2_placar.place(x= 230, y= 2)
    j2_placar_val.place(x= 245, y= 20)
    
    j1_cards = tk.Label(frame2, text= 'Cartas ' + Players.jogador1[0], bg= 'Olive', fg= 'Yellow', font= ('', 9, 'bold'))
    j2_cards = tk.Label(frame2, text= 'Cartas ' + Players.jogador2[0], bg= 'Olive', fg= 'Yellow', font= ('', 9, 'bold'))
    j1_cards_val = tk.Label(frame2, text= '0', width= 13, height= 1, borderwidth= 2, relief= 'groove', bg= 'Crimson', fg= 'yellow')
    j2_cards_val = tk.Label(frame2, text= '0', width= 13, height= 1, borderwidth= 2, relief= 'groove', bg= 'Crimson', fg= 'yellow')
    j1_pux_cards = tk.Button(frame2, text= 'Puxar Carta', width= 13, height= 1, borderwidth= 2, relief= 'groove', bg= 'Red', fg= 'black', command= lambda: on_click_puxar_carta(j1_cards_val, j2_cards_val, botoes_j1, botoes_j2, game, p1time))
    j1_manter = tk.Button(frame2, text= 'Manter', width= 13, height= 1, borderwidth= 2, relief= 'groove', bg= 'Silver', fg= 'black', state= 'disabled', command= lambda: on_click_manter_carta(botoes_j1, botoes_j2, j1_cards_val, j2_cards_val, game, p1time))
    j2_pux_cards = tk.Button(frame2, text= 'Puxar Carta', width= 13, height= 1, borderwidth= 2, relief= 'groove', bg= 'Silver', fg= 'black', state= 'disabled', command= lambda: on_click_puxar_carta(j2_cards_val, j1_cards_val, botoes_j2, botoes_j1, game, p2time))
    j2_manter = tk.Button(frame2, text= 'Manter', width= 13, height= 1, borderwidth= 2, relief= 'groove', bg= 'Silver', fg= 'black', state= 'disabled', command= lambda: on_click_manter_carta(botoes_j2, botoes_j1, j2_cards_val, j1_cards_val, game, p2time))
    botoes_j1 = [j1_pux_cards, j1_manter]
    botoes_j2 = [j2_pux_cards, j2_manter]
    p1time = 'Jogador 1'
    p2time = 'Jogador 2'
    
    j1_cards.place(x= 90, y= 5)
    j1_cards_val.place(x= 93, y= 30)
    j1_pux_cards.place(x= 37, y= 55)
    j1_manter.place(x= 144, y= 55)
    j2_cards.place(x= 90, y= 115)
    j2_cards_val.place(x= 93, y= 135)
    j2_pux_cards.place(x= 37, y= 160)
    j2_manter.place(x= 144, y= 160)
    
def play_again(game, winner):
    ot = messagebox.askquestion('Jogar Novamente', 'Deseja jogar novamente?', parent= game)
    if ot == 'yes':
        if winner == Players.jogador1[0]:
            Valores.valor_placar_player1 += 1
            game.destroy()
            interface_game(janela)
        elif winner == Players.jogador2[0]:
            Valores.valor_placar_player2 += 1
            game.destroy()
            interface_game(janela)
        elif winner == 'Empate':
            game.destroy()
            interface_game(janela)
    else:
        Valores.valor_placar_player1 = 0
        Valores.valor_placar_player2 = 0
        game.destroy()


    
interface_init()