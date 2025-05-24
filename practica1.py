class song:
    def __init__(self,titulo,artista,duracion):
        self.titulo=titulo
        self.artista=artista
        self.duracion=duracion

    def imprimir(self):
        return f"La Cancion {self.titulo} de {self.duracion} de duracion esta compuesta por {self.artista}"

class playlist:
    def __init__(self,nombre):
        self.nombre=nombre
        self.song=[]
    
    def add_song(self,song):
        self.song.append(song)
    
    def remove_song(self,song):
        self.song.remove(song)
    
    def total_duration(self):
        total=0
        for x in self.song:
            total=total+ x.duracion
        return (total)

    def show_song(self):
        for x in self.song:
            print(x.imprimir())

cancion=song("hola","ricardo",23)
play=playlist("prueba")
play.add_song(cancion)
play.show_song()   