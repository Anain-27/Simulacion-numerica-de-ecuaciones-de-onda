import numpy as np
import matplotlib.pyplot as plt
from os import mkdir
from shutil import rmtree

print("Vamos a guardar nuestras imagenes")
print("Introduce el nombre de la carpeta:")
dir= str(input())


#Creamos los directorios
directorio='C:\\Users\\Ana Cuevas de Cózar\\PycharmProjects\\pythonProject2\\'+dir+'\\'
cuerda=directorio + 'Imagenes Cuerda\\'
onda= directorio+ 'Imagenes Onda\\'
try:
    rmtree(cuerda)
    rmtree(onda)
except:
    print('No existían las imagenes, las creamos')
mkdir(onda)
mkdir(cuerda)



#Añadimos los datos
datos = np.load(directorio+'u.npy', mmap_mode='r')

#Solo para ondas viajeras, para mu=1
datoswl = np.load(directorio+'wl.npy', mmap_mode='r') #Solo para mu=1
datoswr = np.load(directorio+'wr.npy', mmap_mode='r') #Solo para mu=1


t = np.load(directorio+'t.npy', mmap_mode='r')
x = np.load(directorio+'x.npy', mmap_mode='r')
[f, m,h,n,k,mu,tmax,l]= np.load(directorio+'constantes.npy', mmap_mode='r')

n=int(n)
m=int(m)

#Vamos a pintar las imagenes de a posición de la cuerda en instantes selecionados
plt.plot(x, datos[:, 0], 'k')

'''
plt.plot(x, datoswl[:, 0], 'r') #Solo para mu=1
plt.plot(x, datoswr[:, 0], 'b') #Solo para mu=1
'''

plt.ylim(-1.1,1.1)
plt.xlabel('x')
plt.ylabel('u')
plt.title(f'Cuerda en el instante {t[0]},\nmin={min(datos[:,0])}, max={max(datos[:,0])}')
plt.savefig(cuerda+f'Cuerda_instante_{0}.png')
plt.close()


if (int(2*n/f)+2)/100 > 1:
    aux=int((int(2*n/f)+2)/100)
else:
    aux=1

for j in range(1, 2*int(2*n/f)+2):

    if j %aux ==0 :
        plt.plot(x, datos[:, j], 'k')


        plt.plot(x, datoswl[:, j], 'r') #Solo para mu=1
        plt.plot(x, datoswr[:, j], 'b') #Solo para mu=1


        plt.ylim(-1.1,1.1)
        plt.xlabel('x')
        plt.ylabel('u')
        plt.title(f'Cuerda en el instante {t[j]},\nmin={min(datos[:,j])}, max={max(datos[:,j])}')
        plt.savefig(cuerda+f'Cuerda_instante_{j}.png')
        plt.close()


#Pintamos la imagen de la onda en los 1000 primeros instantes en cada punto
for j in range(0, m + 1):
    plt.plot(t[0:10*int(2*n/f)+2], datos[j,0:10*int(2*n/f)+2],'r')
    plt.ylim(-1.1, 1.1)
    plt.xlabel('t')
    plt.ylabel('u')
    plt.title(f'Movimiento del punto {x[j]} en el espacio')  #axis tight
    plt.savefig(onda+f'PrimerosmilPunto_{j}.png')
    plt.close()

    plt.plot(t[0:10*int(2*n/f)+2], datos[j, n - (10*int(2*n/f)+2):n], 'b')
    plt.ylim(-1.1, 1.1)
    plt.xlabel('t')
    plt.ylabel('u')
    plt.title(f'Movimiento del punto {x[j]} en el espacio')  # axis tight
    plt.savefig(onda + f'UltimosmilPunto_{j}.png')
    plt.close()