import bpy
import math

### Initialisation
taille_section = 12
nombre_section = 12

rayon_sphere = 1

delta_l = math.pi / taille_section
delta_e = (2 * math.pi) / nombre_section

filename = "file_name.mp3"
filepath = "path goes here" 


### Recuperation des amplitudes de frequence en fonction du temps

### Generation liste coordonnées
listesC = []

for i in range (0, nombre_section):

    listeC = []
    for j in range (0, taille_section):

        listeC.append([rayon_sphere, j * delta_l, i * delta_e])

    listesC.append(listeC)

### Generation de l'objet

#generate vertices
listesV = []
verts = []
for i in range (0, nombre_section):
    listeV = []
    for j in range(0,taille_section):

        c = listesC[i][j]
 
        x = c[0] * math.sin(c[1]) * math.cos(c[2])
        y = c[0] * math.sin(c[1]) * math.sin(c[2])
        z = c[0] * math.cos(c[1])
 
        vert = (x,y,z)
        verts.append(vert)
        listeV.append(vert)
    listesV.append(listesV)
 
 
#generate faces
faces = []
for i in range (0, nombre_section):
    for j in range (0, taille_section):

        A = listesV[i][j]
        B = listesV[i+1][j]
        C = listesV[i+1][j+1]
        D = listesV[i][j+1]
 
        face = (A,B,C,D)
        faces.append(face)
 
#create mesh and object
mesh = bpy.data.meshes.new("audio_sphere")
object = bpy.data.objects.new("audio_sphere",mesh)
 
#set mesh location
object.location = bpy.context.scene.cursor_location
bpy.context.scene.objects.link(object)
 
#create mesh from python data
mesh.from_pydata(verts,[],faces)
mesh.update(calc_edges=True)

### export STL