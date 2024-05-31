import tkinter as tk
import events
import initializer


class Renderizer:
    def __init__(self): #Construtor da classe
        evm = events.EventManager()
        init = initializer.DatabaseManager()
        
        #inicializando o banco de dados antes da janela entrar em loop
        init.database_loader()
        #janela em loop e renderização dos componentes
        w = tk.Tk()
        global music_vol_display
        global current_track_display
        global state_of_music_display
        #criando as variáveis de texto
        music_vol_display = tk.StringVar()
        current_track_display = tk.StringVar()
        state_of_music_display = tk.StringVar()    
    
        #definindo dimensões
        w.geometry("200x200")
        w.resizable(False, False)
            
        #criando os botões 
        askdirectory_btn = tk.Button(w, text="OPEN", command=evm.askdirectory_btn_press)
        prev_btn = tk.Button(w, text ="PREV", command=evm.prev_btn_press)
        min_btn = tk.Button(w, text="MIN", command=evm.min_btn_press)
        max_btn = tk.Button(w, text="MAX", command=evm.max_btn_press)
        play_pause_btn = tk.Button(w, textvariable=state_of_music_display, command=evm.play_pause_btn_press)
        next_btn = tk.Button(w, text="NEXT", command=evm.next_btn_press)
        start_reset_btn = tk.Button(w, text="START", command=evm.start_reset_btn_press)
        
        #criando e renderizando a faixa(musica) atual que está tocando
        current_track = tk.Label(w, textvariable=current_track_display, font="Arial 12")
        current_track.place(x= 55 , y=40)
        #renderizando o volume atual
        current_vol = tk.Label(w, textvariable=music_vol_display)
        current_vol.place(x = 10, y = 150)
            
        #renderizando texto de eventos contínuos
        state_of_music_display.set('PLAY')
        music_vol_display.set(f"VOLUME: {int(init.music_vol * 100)}")
        #tratando erro de inicialização da faixa(musica) atual tocando quando for carregada do banco de dados
        try:
            current_track_display.set(init.musics[init.selected_track].strip())
        except (FileExistsError, FileNotFoundError, IndexError):
            pass
        
        #posicionando os elementos na tela
        start_reset_btn.place(x=80, y=110)
        askdirectory_btn.place(x=10, y=20)
        prev_btn.place(x=10,y=70)
        min_btn.place(x=10, y=110)
        max_btn.place(x=150, y=110)
        play_pause_btn.place(x= 80, y = 70)
        next_btn.place(x=150,y=70)
            
        w.mainloop()