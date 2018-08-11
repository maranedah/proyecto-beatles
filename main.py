

# Instala el midicsv-1.1
import urllib.request
import tarfile
import os

# instala midicsv si no esta
if not os.path.exists("midicsv-1.1"):
    midicsv_comprimido = urllib.request.urlopen("http://www.fourmilab.ch/webtools/midicsv/midicsv-1.1.tar.gz")
    with open('midicsv-1.1.tar.gz','wb') as output:
      output.write(midicsv_comprimido.read())

    # descomprime
    tar = tarfile.open("midicsv-1.1.tar.gz", "r:gz")
    tar.extractall()
    tar.close()

    # borra tar.gz
    os.remove("midicsv-1.1.tar.gz")

    # si es linux compila si es windows usa exe nomas
    if os.name == 'nt':  # Si es windows usar el exe
        print("Estamos en windows no hay que compilar")
    else:  # Si es linux usar el compilado como ejecutable
        print("Se compila el midicsv")
        build_dir = "midicsv-1.1"
        cwd = os.getcwd() # get current directory
        try:
            os.chdir(build_dir)
            resultado = os.system("make")
        finally:
            os.chdir(cwd)

        assert(resultado == 0),"Fallo la compilacion de midicsv realizar compilacion manual y volver a ejecutar script."

# procesa los midis
resultado = os.system("python miditocsv.py")
assert(resultado == 0),"Fallo en miditocsv"

# Filtra csv por tracks
resultado = os.system("python csv_filter_track.py")
assert(resultado == 0),"Fallo en csv_filter_track.py"


# Filtra csv por instrumentos
resultado = os.system("python SplitMidis.py")
assert(resultado == 0),"Fallo en SplitMidis.py"

