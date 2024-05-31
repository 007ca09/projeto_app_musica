import pygame
import os

class DatabaseManager:
    pygame.init()
    pygame.mixer.init()

    selected_track = 0
    music_vol = 0
    user_music_path = ''
    musics = []
    #função para carregar toda a base de dadosç
    #como é possível ver há uma supressão de erros, para impedir que o programa crashe
    #todos os modos do fluxo de arquivos estão em modo de leitura
    #as variáveis definidas acima serão carregadas assim que essa função for chamada lá nas classes EventManager(para pegar os valores atualizados do banco de dados) e na classe Renderizer(para carregar os valores salvos na tela)
    def database_loader(self):
        with open(f'{os.getcwd()}\\database\\current_track.txt', 'r') as file:
            try:
                self.selected_track = int(file.readlines()[0].strip())
            except (FileExistsError, FileNotFoundError, IndexError):
                pass        
        with open(f'{os.getcwd()}\\database\\music_data.txt', 'r') as file: 
            try:
                self.musics = file.readlines()
            except (FileExistsError, FileNotFoundError, IndexError):
                pass
        with open(f'{os.getcwd()}\\database\\current_volume.txt', 'r') as file:
            self.music_vol = float(file.readlines()[0].strip())
            if self.music_vol == 0.009999999999999247:
                pygame.mixer.music.set_volume(0)
            else:
                pygame.mixer.music.set_volume(self.music_vol)
        with open(f'{os.getcwd()}\\database\\path_folder_music.txt', 'r') as file:
            try:
                self.user_music_path = file.readlines()[0].strip()
            except (FileExistsError, FileNotFoundError, IndexError):
                pass