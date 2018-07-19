import os, sys

path="./midi/"
dirs=os.listdir(path)
print(dirs)
dirs2=[]
for file in dirs:
  if ".mid" in file:
    dirs2.append(file)
print(dirs2)
print(len(dirs2))
os.system('mkdir csv')
for a in dirs2:
  os.system('midicsv midi/'+a+ ' csv/'+os.path.splitext(a)[0]+'.csv')
print("Terminado")
