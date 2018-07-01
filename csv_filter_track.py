import os
from shutil import copyfile
import subprocess
from subprocess import Popen, PIPE

os.listdir('./')
# La carpeta con los csv debe estar la misma raiz 
assert(os.path.exists('./csv')),'Debe tener carpeta de csv procesados en working space'
# Revisa que la carpeta ./midicsv-1.1 este en ruta
assert(os.path.exists('./midicsv-1.1')),'Debe tener carpeta midicsv en working space'
assert(os.path.exists('./midicsv-1.1/csvmidi')),'csvmidi no esta compilado'
assert(os.path.exists('./midicsv-1.1/midicsv')),'midicsv no esta compilado'


def filter_csv(csv_string):
    dont_use = ['Copyright_t',
                'Start_track',
                'End_track',
                'End_of_file',
                'Instrument_name_t',
                'MIDI_port',
                'Marker_t','SMPTE_offset','System_exclusive','Text_t','Title_t']


    tracks = {}
    channel_info = {}


    lineas = filter(lambda x : len(x) > 0 ,csv_string.split("\n"))
    for l in lineas:

        palabras = l.split(',')
        track = int(palabras[0].strip())
        comando = palabras[2].strip()
        
        if comando == 'Program_c':
            channel = int(palabras[3].strip())
            channel_info[track] = channel

        # Filtrar
        if comando in dont_use:
            continue

        # Colocar en canal
        if track in tracks:
            tracks[track].append(l)
        else:
            tracks[track] = [l]

    return tracks,channel_info



# crear csv y midi
def midi_to_csv(midi_path,out_csv_path):
    
    cmd = ['midicsv-1.1/midicsv',midi_path,out_csv_path]
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    rc = p.returncode
    
    if rc == 0:
        print("Proceso de {0} exitoso".format(midi_path))
    else:
        print("Error en proceso de {0} .... {1}".format(midi_path,'err'))


def csv_to_midi(csv_path,out_midi):
    cmd = ['midicsv-1.1/csvmidi',csv_path,out_midi]
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    rc = p.returncode
    
    if rc == 0:
        print("Proceso de {0} exitoso".format(csv_path))
    else:
        print("Error en proceso de {0} .... {1}".format(csv_path,'err'))
        


def reconstruct(tracks):
    
    header_track = '\n'.join(tracks[0])
    
    otros_tracks = []
    
    for i in range(1,len(tracks.keys())):
        track_format = """{t_n}, 0, Start_track\n{track_comands}\n{t_n},{l_t}, End_track"""
        
        cms='\n'.join(tracks[i])
        
        last = tracks[i][-1].split(',')[1]
        
        otros_tracks.append(track_format.format(t_n=i,track_comands=cms,l_t=last))
    
    lista_contenidos = [header_track] + otros_tracks + ["0, 0, End_of_file"]
    
    return '\n'.join(lista_contenidos)


files=os.listdir('./csv')
out_folder = './splited_csv'
guardar_copia_csv_or = False


for f_p in files:
    name,t = os.path.splitext(f_p)
    print(t)
    if t == '.csv':
        ffp = os.path.join('./csv',f_p)
        print("Procesando {0}".format(ffp))
        with open(ffp,'r') as f:
            st=f.read()
        
        dest_folder = os.path.join(out_folder,name)
        os.makedirs(dest_folder,exist_ok=True)
            
        if guardar_copia_csv_or:
            copyfile(ffp, os.path.join(dest_folder,'original.csv'))
            
        # Partir por track
        tracks,c_info = filter_csv(st)
        
        # Escribir tracks a disco
        
        for k in tracks:
            dst = os.path.join(dest_folder,'track_{0}.csv'.format(k))
            with open(dst,'w') as f:
                f.write('\n'.join(tracks[k]))
                

        # Ahora reconstruir y apreciar si sigue funcionando
        csv_string = reconstruct(tracks)

        
        with open(os.path.join(dest_folder,"reconstruct.csv"),'w') as f:
            f.write(csv_string)

        csv_to_midi(os.path.join(dest_folder,"reconstruct.csv"),os.path.join(dest_folder,"reconstruct.midi"))


