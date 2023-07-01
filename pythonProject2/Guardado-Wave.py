import numpy as np
from scipy.io.wavfile import write

print("Vamos a guardar nuestros datos en formato wav")
print("Introduce el nombre de la carpeta:")
dir= str(input())


#Creamos el directorio
directorio='C:\\Users\\Ana Cuevas de Cózar\\PycharmProjects\\pythonProject2\\'+dir+'\\'


#Añadimos los datos
datos = np.load(directorio+'u.npy', mmap_mode='r')
t = np.load(directorio+'t.npy', mmap_mode='r')
x = np.load(directorio+'x.npy', mmap_mode='r')
[f, m1,h1,n1,k1,mu,tmax,l]= np.load(directorio+'constantes.npy', mmap_mode='r')

'''
#Para la solución exacta
datoswl = np.load(directorio+'wl.npy', mmap_mode='r') 
datoswr = np.load(directorio+'wr.npy', mmap_mode='r') 
'''

m1=int(m1)
n1=int(n1)

#Constantes necesarias
sample_rate = 44100
n2 = int(tmax*sample_rate)
t_necesario= np.linspace(0,tmax,n2 +1)


# Escogiendo un punto en particular
# Comprobamos donde está el punto de mayor amplitud en el instante inicial y en ese punto es donde veremos como se mueve la onda.
pos_readout= np.where(datos[:,0]==max(datos[:,0]))[0][0]

if pos_readout==0:
    pos_readout= int(m1/(2*l))
    print('Cambio la posicion a 0.5')


wave_table = datos[pos_readout] # Elijo un punto en el espacio en el que veremos el movimiento de la cuerda
output = np.interp(t_necesario,  t, wave_table)

'''
#Para la solución exacta
wave_table2 = datoswr[pos_readout]+datoswl[pos_readout] # 
output = np.interp(t_necesario,  t, wave_table)
'''

'''
# Sumando todos los puntos en espacio que tenemos.
wave_table = np.zeros(n1 + 1)
for i in range(0, m1+1):
    wave_table += datos[i, :]

wave_table= wave_table/(m1+1)
output = np.interp(t_necesario,  t, wave_table)
'''

'''
#Vamos a modificar los limites para que suene a un nivel de volumen adecuado, para ello teben ser en torno al orden e-1 o e-2
#gain= 0
#amplitud = 10** (gain/20)
#output *=amplitud


# Para que al principio y final se escuche mas suave
#output = fade(output)
'''

#Guardamos
write(directorio+f'Sonido.wav',sample_rate,output)