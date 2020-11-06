import os

#nord=open(os.system("cut -d'N' -f1 '/home/guillaume/Téléchargements/Waypoints.yml' | cut -d':' -f2 > /home/guillaume/Téléchargements/nord.txt"))

secondes=open(os.system('cut -d"\'" -f2 | cut -d\" -f1 /home/guillaume/Téléchargements/nord.txt '))

for line in secondes.read():
    print(line)
#
# for line in secondes.read():
#     s=str(line)
#
#
#


#os.system("cut -d'W' -f2 '/home/guillaume/Téléchargements/Waypoints.yml' | cut -d',' -f2 > /home/guillaume/Téléchargements/ouest.txt")
#ouest=open("/home/guillaume/Téléchargements/ouest.txt")


