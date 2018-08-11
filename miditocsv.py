import os, sys

path="./midi/"
dirs=os.listdir(path)
dirs2=[]
for file in dirs:
  if ".mid" in file:
    dirs2.append(file)

os.makedirs('csv',exist_ok=True)
for a in dirs2:
  path_midi = os.path.join("midi",a)
  path_csv_out = os.path.join("csv",os.path.splitext(a)[0]+'.csv')
  os.system('midicsv-1.1/midicsv "{0}" "{1}" '.format(path_midi,path_csv_out))
print("Terminado")

