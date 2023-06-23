import numpy as np
import time
import os as os
from shutil import rmtree
import matplotlib.pyplot as plt

#Funciones necesarias

# Para inicializar los valores iniciales que dependen de la derivada lo haremos con una aproximación progresiva del tiempo

def g(x):
    return 0


'''
# En este caso tomamos una condición tipo struck en 0.4 , 0.5 max
def g(x):
    if( x<=0.4):
        return 2.5*x
    else:
        return -(10/6)*x
'''

'''
# En este caso tomamos una condición tipo struck en 0.1 , 1 max
def g(x):
    if( x<=0.1):
        return 50000*x
    if (x <= 0.2):
        return 50000*(0.2-x)
    else:
        return 0

'''
'''
# En este caso tomamos una condición tipo crc c0=1000 x0 = 0.5
def g(x):
    if (0.4<=x <= 0.6):
        return 1000/2 * (1+np.cos(np.pi*(x-0.4)/0.1))
    else:
        return 0
'''


# Condición de contorno en el eje de posición tipo seno
def f(x):
    aux = []
    for i in x:
        aux.append(np.sin(2*np.pi*i))
    return aux # Tener cuidado con la función por si se sale del rango


'''
#Condición de contorno en el eje de posición tipo pico
def f(x):
    aux = []
    for i in x:
        if( i<=0.25):
            aux.append(0)
        elif ( i<=0.5):
            aux.append(4*(i-0.25))
        elif ( i<=0.75):
            aux.append(4*(0.75-i))
        else:
            aux.append(0)
    return aux
'''

'''
#Condición de contorno en el eje de posición tipo trapecio
def f(x):
    aux = []
    for i in x:
        if( i<=0.1):
            aux.append(0)
        elif ( i<=0.3):
            aux.append(5*i-0.5)
        elif ( i<=0.7):
            aux.append(1)
        elif ( i<=0.9):
            aux.append(-5*i+4.5)
        else:
            aux.append(0)
    return aux
'''

'''
#condicioón de tipo c_rc con x_hw= 0.2 x_0 = 0.5 c_0= 1
def f(x):
    aux = []
    for i in x:
        if( i<=0.3):
            aux.append(0)
        elif ( i<=0.7):
            aux.append((1+np.cos(np.pi * (i-0.5)/0.2))/2)

        else:
            aux.append(0)
    return aux
'''

'''
# Condición de contorno en el eje de posición tipo plano
def f(x):
    lon = len(x)
    return np.zeros(lon)
'''

# Definimos una función para usar en el método explícito y poder cambiarlo de manera rápida si hace falta
def Explicito(x1, x2, x3, x4,mu):  # Si queremos hacerlo en un file independiente tendremos que añadir el mu
    return  mu ** 2 * (x1 + x2) + 2 * (1- mu ** 2) * x3 - x4


start = time.time()
print("Vamos a hacer una resolución numérica de la ecuación de onda u_tt-c^2u_xx=0")
print("Introduce c:")
c= float(input())
print("Introduce el nombre del directorio donde quieres guardar los archivos:")
directorio=input()


#Creamos una carpeta en la que se guardarán los datos
home = 'C:\\Users\\Ana Cuevas de Cózar\\PycharmProjects\\pythonProject2'
directoriofinal=home+'\\'+directorio+'\\'
#Si existe el directorio lo borra
try:
    rmtree(directoriofinal)
except:
    print('No existía el directorio, lo creamos')
os.mkdir(directoriofinal)


#Constantes necesarias
l=1
tmax= 1
m = int(l*300)# Constante representativa del número de trozos en los que separamos el espacio
h=l/m  #Cambiamos la h para que sea entera

k =h/c #Lo tomamos de esta forma para ganar en exactitud pagina 133 numerical sound synthesis


# Cambiamos k para hacer las comparaciones
'''
k =h/c * 0.9
k =h/c * 0.5
k =h/c * 0.1
k =h/c * 0.01
k =1.001*h/c
k =1.005*h/c
'''


n= int(tmax/k)
mu = c * k / h

if mu>1 :
    raise Exception('Mu es mayor que 1')
print(f'n{n}, c{c}, k{k}, h{h}, m{m}, mu{mu}')

# Creamos un mallado de puntos en los que aproximaremos la solución
x= np.linspace(0,l,num=m +1)
t= np.linspace(0,tmax,num=n +1)



# Creamos la matriz u de soluciones
# u(x,t)
u = np.empty((m + 1, n + 1), float)


# Añadimos antes que nada los nodos conocidos por las condiciones de contorno
u[:, 0] = f(x)

u[0, :] = np.zeros(n + 1)

u[m, :] = np.zeros(n + 1)
aux=[0]


# Para inicializar los valores iniciales que dependen de la derivada lo haremos con una aproximación progresiva del tiempo
for i in range(1, m):
    u[i, 1] = u[i, 0] + k * g(x[i])
    aux.append(g(x[i]))

aux.append(g(x[m]))

for j in range(2, n + 1):
    u[1:m, j] = Explicito(u[2:m+1,j-1], u[0:m-1,j-1], u[1:m,j-1], u[1:m,j-2],mu)


#Implementamos la solución de tipo onda viajera. #Solo para mu=1

# Creamos la matriz wl la solución viajera hacia la izquierda y wr hacia la derecha

wl = np.empty((m + 1, n + 1), float) #Solo para mu=1
wr = np.empty((m + 1, n + 1), float) #Solo para mu=1

#Inicializamos la solución
for i in range(0, m+1):
    if i==0:
        sumx =2* g(x[0])
    elif i==1:
        sumx = g(x[0])+g(x[1])
    else:
        sumx += g(x[i-1])+g(x[i])
    wl[i, 0] = 1 / 2 * f([x[i]])[0] + h / (4 * c) * (sumx) + k / 4 * 2*g(x[i]+c*t[0]) #Prueba apendice libro Bilbao
wr[0:m+1,0]=wl[0:m+1,0]


for j in range(1, n + 1):
    temp1 = wr[m,j-1]
    temp2 = wl[0,j-1]
    wr[1:m+1,j] = wr[0:m,j-1]
    wl[0:m ,j] = wl[1:m+1,j-1]
    wr[0,j] = -temp2
    wl[m,j] = -temp1


end = time.time()


plt.plot(x,aux,'k')
plt.xlabel('x')
plt.ylabel('g(x)')
plt.title(f'G')
plt.savefig(directoriofinal+'prueba g.png')
plt.close()

print(f'Ha tardado {np.floor(end-start)} segundos.')
np.save(directoriofinal+'u', u)
np.save(directoriofinal+'x', x)
np.save(directoriofinal+'t', t)


np.save(directoriofinal+'wl', wl) #Solo para mu=1
np.save(directoriofinal + 'wr', wr) #Solo para mu=1


np.save(directoriofinal+'constantes', [c, m,h,n,k,mu,tmax,l] ) #Guardar en cons las constantes que necesitemos para usarlas luego en el guardado del sonido


