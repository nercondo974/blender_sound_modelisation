import bpy
import math
import numpy as np
import scipy.io.wavfile as wave
from numpy.fft import fft

### Initialisation
taille_section = 12
nombre_section = 12

rayon_sphere = 1

delta_l = math.pi / taille_section
delta_e = (2 * math.pi) / nombre_section

filename = "file.wav"
filepath = "path" 

### Méthodes
def recupFrequence(spectres):
    liste = []
    for i in range(12):
        liste.append(sum(spectres[int(len(spectres)/12)*i:int(len(spectres)/12)*(i+1)]))
    return liste

def recupSpectre(data,rate,debut,duree):
    start = int(debut*rate)
    stop = int((debut+(duree/12))*rate)

    spectre = np.absolute(fft(data[start:stop]))
    if(spectre.max()!= 0.0):
        spectre = spectre/spectre.max()
    return recupFrequence(spectre)

### Recuperation des amplitudes de frequence en fonction du temps

rate,data = wave.read(filepath+"/"+filename)

n = data.size
duree = 1.0*n/rate

listeFreq = []
for i in range(0, nombre_section):
    listeFreq.append(recupSpectre(data,rate,i*(duree/nombre_section),duree/nombre_section))

#tracerSpectre(data,rate,0.0,0.5)
            

### Generation liste coordonnées
listesC = []

for i in range (0, nombre_section):

    listeC = []
    for j in range (0, taille_section):

        listeC.append([rayon_sphere+listeFreq[i][j], j * delta_l, i * delta_e])

    listesC.append(listeC)

### Generation de l'objet

#generate vertices
def convCoordPol(liste, i, j):
        c = liste[i][j]
        x = c[0] * math.sin(c[1]) * math.cos(c[2])
        y = c[0] * math.sin(c[1]) * math.sin(c[2])
        z = c[0] * math.cos(c[1])
        return (x,y,z)

listesV = []
for i in range (0, nombre_section):
    listeV = []
    for j in range(0,taille_section):
        listeV.append(convCoordPol(listesC, i, j))
    listesV.append(listeV)
 
#generate faces
def convVert2Face(liste, i, j):
    if(nombre_section-1 > i & taille_section-1 > j):
        A = listesV[i][j]
        B = listesV[i+1][j]
        C = listesV[i+1][j+1]
        D = listesV[i][j+1]
        return (A,B,C,D)

faces = []
for i in range (nombre_section):
    for j in range (taille_section):
        faces.append(convVert2Face(listesV,i,j))

#create mesh and object
#mesh = bpy.data.meshes.new("audio_sphere")
#object = bpy.data.objects.new("audio_sphere",mesh)
 
#set mesh location
#object.location = bpy.context.scene.cursor_location
#bpy.context.scene.objects.link(object)
 
#create mesh from python data
#mesh.from_pydata(verts,[],faces)
#mesh.update(calc_edges=True)

### export STL
