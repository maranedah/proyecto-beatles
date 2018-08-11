# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 15:26:50 2018

@author: mac2mac
"""
import os
import csv
#

import os

# Dependiendo del sistema operativo elige si usar el exe o el ejecutable
def to_midi(path_csv,path_midi_out):
    if os.name == 'nt':  # Si es windows usar el exe
        os.system('./midicsv-1.1/Csvmidi "{0}" "{1}"'.format(path_csv,path_midi_out))
    else: # Si es linux usar el compilado como ejecutable
        os.system('./midicsv-1.1/csvmidi "{0}" "{1}" '.format(path_csv, path_midi_out))


assert(os.path.exists('./splited_csv/'))

carpeta_generados_por_instrumento= 'midis_por_instrumento'

os.makedirs(os.path.join(carpeta_generados_por_instrumento,"Guitar"),exist_ok=True)
os.makedirs(os.path.join(carpeta_generados_por_instrumento,"Piano"),exist_ok=True)
os.makedirs(os.path.join(carpeta_generados_por_instrumento,"Drums"),exist_ok=True)
os.makedirs(os.path.join(carpeta_generados_por_instrumento,"Other"),exist_ok=True)
os.makedirs(os.path.join(carpeta_generados_por_instrumento,"Bass"),exist_ok=True)
os.makedirs(os.path.join(carpeta_generados_por_instrumento,"Voice"),exist_ok=True)


path="./splited_csv/"
dirs=os.listdir(path)

for i in range(len(dirs)):
    
    path2=path+dirs[i]
    
    dirs2=os.listdir(path2)
    
    
    num=[]
    ins=[]
    with open(path2+'/reconstruct.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
    #        h=h+1
    #        if h==100: break
    #       print(row)
            if row[2]==' Program_c':
                if (int(row[4])>=0 and int(row[4])<9):
                    num.append(row[0])
                    ins.append("Piano")
                if int(row[4])>=9  and int(row[4])<17:
                    num.append(row[0])
                    ins.append("Drums")
                if int(row[4])>=17 and int(row[4])<25 :
                    num.append(row[0])
                    ins.append("Other")
                if int(row[4])>=25  and int(row[4])<33 :
                    num.append(row[0])
                    ins.append("Guitar")
                if int(row[4])>=33  and int(row[4])<41 :
                    num.append(row[0])
                    ins.append("Bass")
                if int(row[4])>=41 and int(row[4])!=68 :
                    num.append(row[0])
                    ins.append("Drums")
                if int(row[4])==68:
                    num.append(row[0])
                    ins.append("Voice")
                    
    #num.append('6')
    #ins.append('Guitar')
    #print(ins)
    while True:
        if not num:
            break
        h=['0','1']
        B=ins[0]
        while B in ins:
            C=ins.index(B)-1
            h.append(num[C])
            num.remove(num[C])
            ins.remove(B)
        path3= os.path.join(carpeta_generados_por_instrumento, B)
        #print(h)
        h_real=['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20']#list(range(len(h)))
        with open(path2+'/reconstruct.csv', 'r') as f:
            csv_out_path = os.path.join(path3,dirs[i]+"_"+B+'.csv')
            midi_out_path = os.path.join(path3,dirs[i]+"_"+B+'.mid')
            with open(csv_out_path, 'w', newline='') as csvfile:
                reader = csv.reader(f)
                spamwriter = csv.writer(csvfile,delimiter=',')
                for row in reader:
                    if row[0] in h:
                        for p in range(len(h)):
                            if row[0]==h[p]:
                                if p==0:
                                    if row[2]==' Header':
                                        row[4]=str(len(h)-1)
                                row[0]=str(h_real[p])
                                if p>1:
                                    if row[2]==' End_track' or row[2]==' Start_track':
                                        pass
                                    else:
                                        row[3]=' '+str(p-2)
    #                                print(row)
                        spamwriter.writerow(row)
        to_midi(csv_out_path, midi_out_path)


