import os
import turtle
import csv
from csv_filter_track import csv_to_midi
# carpeta out_midis


validos = {
'guitar' : 30 ,
'bass' : 35,
'reed' : 68
}
tracks = {
'guitar' : 2 ,
'bass' : 3,
'reed' : 4
}


n_canales = 3

# por elementos en carpetas
carpeta='/home/inquisidor/Desktop/incognito/proyecto-beatles/midis_por_instrumento/test'
out_f= 'midis_por_instrumento'

l_f = os.listdir(carpeta)
assert(len(l_f) == n_canales),'DEBE TENER SOLO 3 ARCHIVOS DENTRO'

# a csv
tipo_csv = '.csv'
base_folder= 'temp_csv'
os.makedirs(base_folder,exist_ok=True)
csv_list = []

inst_dict = {}
channel_count = 0
for p_midi in l_f:	 
    name_midi=os.path.splitext(p_midi)[0]
    print(name_midi)
    inst = name_midi.split('_')[1]
    print(inst)
    full_path_midi = os.path.join(carpeta,p_midi)
    path_csv_out = os.path.join(base_folder , name_midi+tipo_csv)
    os.system('midicsv-1.1/midicsv "{0}" "{1}" '.format(full_path_midi,path_csv_out))
    csv_list.append(path_csv_out)
    inst_dict[inst] = path_csv_out
print(inst_dict)
assert(len(inst_dict) == n_canales)
out_csv_full_inst = os.path.join(out_f,'resultado.csv')

diccionario_track={i : [] for i in range(6)}


    

key_list = ['guitar','bass','reed']
dict_global = {}
track_global = 2
canal = 0
header = ''
comandos_validos = [' Control_c', ' Note_on_c', ' Note_off_c']
for inst_key in key_list:
    archivo_csv_current = inst_dict[inst_key]
    dict_global[inst_key]={}

    with open(archivo_csv_current,'r') as csv_c:
        default_dict = {'Control_c': [], 'Notes': []}
        reader = csv.reader(csv_c)
        for row in reader:
            track = int(row[0])

            if track == 0:
                continue
            if not track in dict_global[inst_key]:
                dict_global[inst_key][track] = default_dict
            if row[2] in comandos_validos:
                if row[2].strip() == 'Control_c':
                    dict_global[inst_key][track]['Control_c'].append([row[4], row[5]])

                if row[2].strip() in ['Note_on_c',"Note_off_c"]:
                    dict_global[inst_key][track]['Notes'].append([row[1],row[2],row[4],row[5]])

with open(out_csv_full_inst, 'w') as csvfile:
    spamwriter = csv.writer(csvfile,delimiter=',')

    total_channels = sum([len(track_dict.keys()) for track_dict in dict_global.values() ]) + 1
    spamwriter.writerow(['0', ' 0', ' Header', ' 1', str(total_channels), ' 480'])

    spamwriter.writerow([str(1), ' 0', ' Start_track'])
    spamwriter.writerow([str(1), str(0), ' End_track'])

    for k in dict_global:
        track_dict = dict_global[k]
        for track_key in track_dict:
            #Comienza el track
            spamwriter.writerow([str(track_global), ' 0', ' Start_track'])
            #Anotamos todos los control_c necesarios
            for instruction in track_dict[track_key]['Control_c']:
                spamwriter.writerow([str(track_global), ' 0', ' Control_c', str(canal), instruction[0], instruction[1]])
            #Damos program c para tener sonido de instrumento
            spamwriter.writerow([str(track_global), ' 0', ' Program_c', str(canal), validos[k]])

            for note in track_dict[track_key]['Notes']:
                spamwriter.writerow([str(track_global), note[0], note[1], str(canal), note[2], note[3]])
                last_time = note[0]

            #last_time se actualiza en cada iteracion del track, hasta que se acabe
            spamwriter.writerow([str(track_global), str(last_time), ' End_track'])

            canal+=1
            track_global+=1
    spamwriter.writerow(['0','0','End_of_file'])  

# pasar a midi
csv_to_midi(out_csv_full_inst,os.path.join(out_f,'resultado.mid'))

print("Terminado")
