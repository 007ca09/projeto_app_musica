import initializer
import render as rd
import pygame
import tkinter.filedialog as tkf
import os


class EventManager:
    #definindo variáveis de uso global nesta classe
    exec_if_music_start = False
    state_of_music = False
    init = initializer.DatabaseManager()
    init.database_loader()
    
    #função para salvar última alteração feita pelo usuário
    def save_last_data(self, path, content_data):
        with open(f'database\\{path}', 'w') as file: #escrevendo no banco de dados
            file.write(str(content_data))
    #função para poder mundar a música
    def change_music(self):
        rd.current_track_display.set(self.init.musics[self.init.selected_track].strip()) #musics é um array e selected_track é o ponteiro que aponta para a música correspondente no banco de dados
        pygame.mixer.music.unload() #quando essa função for chamada 'pygame.mixer.music.unload()' é invocado para descarregar a música
    #função para abrir uma caixa de diálogo para perguntar ao usuário onde ele quer abrir a pasta de músicas dele
    def askdirectory_btn_press(self):
        self.init.user_music_path = tkf.askdirectory() #inicializando a caixa de diálogo
        current_dir = os.getcwd() #obtendo o diretório atual
        self.save_last_data('path_folder_music.txt', self.init.user_music_path) # Aqui a função de save vai salvar o caminho que está a pasta de músicas do usuário no banco de dados 'path_folder_music.txt'
        self.save_last_data('current_track.txt', '0') #Como uma forma de evitar bugs e afins, toda vez que o usuário abrir a caixa de dialogo ele vai resetar o ponteiro da faixa atual para 0, que seria o menor valor para o conjunto de músicas
        #abrindo o arquivo em modo de escrita, como uma forma de limpar o banco de dados. Novamente para evitar sobrescrita desnecessária
        with open(f'{current_dir}\\database\\music_data.txt', 'w') as file:
            pass
        os.chdir(self.init.user_music_path) #mudando o diretório para a pasta de músicas que o usuário escolheu na caixa de diálogos
        #Aqui há uma definição de um algoritmo de para pegar os nomes das músicas do usuário e colocar dentro do banco de dados de músicas. OBS: os.listdir() retorna um vetor de quantos diretórios tem na pasta 
        for i in range(0, len(os.listdir()), 1):
            with open(f'{current_dir}\\database\\music_data.txt', 'a') as file:
                file.write(f'{os.listdir()[i]}\n') #Como os.listdir() retorna um vetor, [i] para pegar cada posição em formato de string e pôr em music_data.txt com uma quebra de linha   
    #função para iniciar e resetar a música
    def start_reset_btn_press(self):
        pygame.mixer.music.load(f'{self.init.user_music_path}\\{self.init.musics[self.init.selected_track].strip()}')
        pygame.mixer.music.play()
        self.state_of_music = False #essa variável ela indica o estado atual que a música está, se é pausado ou não pausado(música em andamento)
        self.exec_if_music_start = True #essa variável indica quando que o usuário vai poder pausar ou não. Se a música não tiver começado o usuário não poderá pausar a música
        #quando essa função for chamada, ela vai iniciar e o label de estado atual da música vai ficar como 'PAUSE' indicando que a música está tocando e que o o usuário pode pausa-la
        rd.state_of_music_display.set('PAUSE')
    #função para pausar e despausar a musica
    def play_pause_btn_press(self):     
        if self.exec_if_music_start:#essa condição tem como base a variável exec_if_music_start como citei acima
            if not self.state_of_music: #se state_of_music for falso, quer dizer que a música não foi pausada ainda. Ou seja, quando o usuário clicar aparecerá 'PLAY' indicando para o usuário que a música pausou
                pygame.mixer.music.pause()
                rd.state_of_music_display.set('PLAY')
                self.state_of_music = True
            else: #Mesma lógica de cima só que funcionando da forma contrária
                pygame.mixer.music.unpause()
                rd.state_of_music_display.set('PAUSE')
                self.state_of_music = False
    #função para voltar uma música. OBS: quando há a troca de música, o estado do label de estado fica como 'PLAY' já que por sua vez, a música para, quando há a troca de música
    def prev_btn_press(self):
        rd.state_of_music_display.set('PLAY')
        self.exec_if_music_start = False #Variável de condição se o usuário poder pausar a música vai par False, indicando que a música precisa ser iniciada
        if self.init.selected_track - 1 < 0: # se o ponteiro que aponta para música atual voltando uma casa for menor que zero, então eu posiciono esse ponteiro para o final da lista de músicas. OBS: o (- 1) é necessário pois se o ponteiro for para a primeira música, e o usuário voltar mais uma música, ele iria apresentar um erro de ListOutOfRange, ai para evitar esse bug, utilizamos esse  - 1
            self.init.selected_track = len(self.init.musics) - 1
            self.save_last_data('current_track.txt', self.init.selected_track)
        else:
            self.init.selected_track -= 1
            self.save_last_data('current_track.txt', self.init.selected_track)
        self.change_music()

    #função para avançar uma música
    def next_btn_press(self):
        rd.state_of_music_display.set('PLAY')
        self.exec_if_music_start = False
        if self.init.selected_track + 1 > len(self.init.musics) - 1: #Se a posição do ponteiro for igual a 4 e a quantidade de músicas também for 4, ele volta para a posição inicial, dando esse efeito de 'deslize', não sei explicar.
            self.init.selected_track = 0
            self.save_last_data('current_track.txt', self.init.selected_track)
        else:
            self.init.selected_track += 1
            self.save_last_data('current_track.txt', self.init.selected_track)
        self.change_music()
    #função de diminuir o volume da música, que também fica salvo no banco de dados. Ambas funções operam com float e com uma imprecisão de ponto flutuante. O backend faz toda a operação de aritmética apenas de 0 a 1, e para o usuário é mostrado de 0 a 100    
    def min_btn_press(self):
        #aqui há uma verificação para saber se o volume da música chegou a 0 que é equivalente a esse número => 0.009999999999999247
        if self.init.music_vol > 0.009999999999999247: #Número com imprecisão de ponto flutuante que é equivalente ao valor zero
            self.init.music_vol -= 0.01
            pygame.mixer.music.set_volume(self.init.music_vol)    
            rd.music_vol_display.set(f"VOLUME: {int(self.init.music_vol * 100)}")
            self.save_last_data('current_volume.txt', self.init.music_vol)
        if self.init.music_vol == 0.009999999999999247: #Verificação se o volume da música é igual a esse valor(zero)
            pygame.mixer.music.set_volume(0) 
    #função de aumentar    
    def max_btn_press(self):
        if self.init.music_vol < 1:
            self.init.music_vol += 0.01
            pygame.mixer.music.set_volume(self.init.music_vol)
            rd.music_vol_display.set(f"VOLUME: {int(self.init.music_vol * 100)}") #aqui precisamos fazer o * 100 para transformar para uma equivalente porcentagem e colocar ela como inteiro, eliminando todas as casas decimais desncessárias para o usuário ver
            self.save_last_data('current_volume.txt', self.init.music_vol)
