# -*- coding: utf-8 -*-
"""AnnyVera_fusionseñales.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1q_XHEe3T-JGe6b6W5_aHoAq5n08R9NLJ
"""

!git clone https://github.com/StefaniaAV/IABO.git

"""Librerias necesarias"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""Función para la lectura de los archivos"""

def lectura(archivo, AX,AY,AZ,GX,GY,GZ):
  df = pd.read_csv(archivo, delimiter = ';', names = ['ax', 'ay', 'az', 'gx', 'gy', 'gz'])
  ax= df['ax']
  ay=df['ay']
  az=df['az']
  gx=df['gx']
  gy=df['gy']
  gz=df['gz']
  AX=np.append(AX,np.array(ax))
  AY=np.append(AY,np.array(ay))
  AZ=np.append(AZ,np.array(az))
  GX=np.append(GX,np.array(gx))
  GY=np.append(GY,np.array(gy))
  GZ=np.append(GZ,np.array(gz))
  return AX,AY,AZ,GX,GY,GZ

"""#**Diseño con Deep Learning**

Creación de imágenes con señales
"""

N=40                   # Número de muestras por ventana
nV=2500                  # Número de muestras de la señal
segment = np.floor(nV/N)    # Número de segmetos de la señal
print("Segmentos : ",segment)

import cv2
from google.colab.patches import cv2_imshow
import matplotlib.pyplot as plt

AX,AY,AZ,GX,GY,GZ=lectura("IABO/data/avanzar/avanzar_1.csv",0.0,0.0,0.0,0.0,0.0,0.0)
for i in range(2,21):
  AX,AY,AZ,GX,GY,GZ=lectura(f"IABO/data/avanzar/avanzar_{i}.csv",AX,AY,AZ,GX,GY,GZ)



# Normalización de las señales
AXmax=AX.max()
AXmin=AX.min()
AX=(AX-AXmin)/(AXmax-AXmin)
AYmax=AY.max()
AYmin=AY.min()
AY=(AY-AYmin)/(AYmax-AYmin)
AZmax=AZ.max()
AZmin=AZ.min()
AZ=(AZ-AZmin)/(AZmax-AZmin)
GXmax=GX.max()
GXmin=GX.min()
GX=(GX-GXmin)/(GXmax-GXmin)
GYmax=GY.max()
GYmin=GY.min()
GY=(GY-GYmin)/(GYmax-GYmin)
GZmax=GZ.max()
GZmin=GZ.min()
GZ=(GZ-GZmin)/(GZmax-GZmin)

# Imagen creada con la señal
size=(49,40)
imagen = np.ones(size)/1.0
for i in range(0,49):
  ventana=np.array(GX[int(i*N):int((i+1)*N)])
  imagen[i,:] = ventana
plt.imshow(imagen,vmin=0,vmax=1)

# Imagen creada con la energía de la señal
size=(49,40)
EAX=np.multiply(AX,AX)
imagen=np.ones(size)/1.0
for i in range(0,49):
  ventana=np.array(EAX[int(i*N):int((i+1)*N)])
  imagen[i,:]=ventana
plt.imshow(imagen,vmin=0,vmax=1)

from scipy.fft import fft, ifft

y=fft(ventana)
plt.plot(abs(y))

"""Se utiliza el espectro de la energía de la señal"""

size=(49,40)
EAY=np.multiply(AY,AY)
imagen=np.ones(size)/1.0
for i in range(0,49):
  ventana=np.array(AY[int(i*N):int((i+1)*N)])
  y=fft(ventana)
  imagen[i,:]=abs(y)/2
plt.imshow(imagen,vmin=0,vmax=1)

from scipy.fftpack import  dct
size=(49,40)
EAY=np.multiply(AY,AY)
imagen=np.ones(size)/1.0
for i in range(0,49):
  ventana=np.array(AY[int(i*N):int((i+1)*N)])
  y=dct(ventana)
  imagen[i,:]=abs(y)/4
plt.imshow(imagen,vmin=0,vmax=1)

"""### ***Fusion de señales para crear imagenes***

### **Gesto avanzar**
"""

AX,AY,AZ,GX,GY,GZ=lectura("IABO/data/avanzar/avanzar_1.csv",0.0,0.0,0.0,0.0,0.0,0.0)
for i in range(2,21):
  AX,AY,AZ,GX,GY,GZ=lectura(f"IABO/data/avanzar/avanzar_{i}.csv",AX,AY,AZ,GX,GY,GZ)

from scipy.fftpack import  dct
size=(49,40)
#EAY=np.multiply(AY,AY)
imagen=np.ones(size)/1.0
for i in range(0,49):
  ventana1=np.array(AX[int(i*N):int((i+1)*N)])
  ventana2=np.array(AY[int(i*N):int((i+1)*N)])
  ventana3=np.array(AZ[int(i*N):int((i+1)*N)])
  ventana4=np.array(GX[int(i*N):int((i+1)*N)])
  ventana5=np.array(GY[int(i*N):int((i+1)*N)])
  ventana6=np.array(GZ[int(i*N):int((i+1)*N)])
  #y=ventana1*ventana2*ventana3+ventana4+ventana6-ventana5
  #y=(ventana4+ventana5+ventana6+ventana3)/ventana1 dan unas repetidas
  #y=(ventana2*ventana3+ventana4)/(ventana6-ventana5) + ventana1**2

  #y = ventana1*(ventana2)**1/2 + (ventana3*ventana4-ventana5**2) sirve
  y = ventana1*(ventana2)*1/2 + (ventana3*ventana4)
  #y = ventana1**(ventana2)*1/2 + (ventana3*ventana4)
  imagen[i,:] = y
plt.imshow(imagen,vmin=0,vmax=1)

"""### **Gesto detener**

"""

AX,AY,AZ,GX,GY,GZ=lectura("IABO/data/detener/detener_1.csv",0.0,0.0,0.0,0.0,0.0,0.0)
for i in range(2,21):
  AX,AY,AZ,GX,GY,GZ=lectura(f"IABO/data/detener/detener_{i}.csv",AX,AY,AZ,GX,GY,GZ)

from scipy.fftpack import  dct
size=(49,40)
imagen=np.ones(size)/1.0
for i in range(0,49):
  ventana1=np.array(AX[int(i*N):int((i+1)*N)])
  ventana2=np.array(AY[int(i*N):int((i+1)*N)])
  ventana3=np.array(AZ[int(i*N):int((i+1)*N)])
  ventana4=np.array(GX[int(i*N):int((i+1)*N)])
  ventana5=np.array(GY[int(i*N):int((i+1)*N)])
  ventana6=np.array(GZ[int(i*N):int((i+1)*N)])
  #y=(ventana4+ventana5+ventana6+ventana3)/ventana1
  #y=ventana1*ventana2*ventana3+ventana4+ventana6-ventana5
  #y=(ventana2*ventana3+ventana4)/(ventana6-ventana5) + ventana1**2 da repetido

  #y = ventana1*(ventana2)**1/2 + (ventana3*ventana4-ventana5**2) sirve
  y = ventana1*(ventana2)**1/2 + (ventana3*ventana4)
  #y = ventana1**(ventana2)*1/2 + (ventana3*ventana4)
  imagen[i,:]=y
plt.imshow(imagen,vmin=0,vmax=1)

"""### **Gesto devolverse**"""

AX,AY,AZ,GX,GY,GZ=lectura("IABO/data/devolverse/devolverse_1.csv",0.0,0.0,0.0,0.0,0.0,0.0)
for i in range(2,21):
  AX,AY,AZ,GX,GY,GZ=lectura(f"IABO/data/devolverse/devolverse_{i}.csv",AX,AY,AZ,GX,GY,GZ)

from scipy.fftpack import  dct
size=(49,40)
EAY=np.multiply(AY,AY)
imagen=np.ones(size)/1.0
for i in range(0,49):
  ventana1=np.array(AX[int(i*N):int((i+1)*N)])
  ventana2=np.array(AY[int(i*N):int((i+1)*N)])
  ventana3=np.array(AZ[int(i*N):int((i+1)*N)])
  ventana4=np.array(GX[int(i*N):int((i+1)*N)])
  ventana5=np.array(GY[int(i*N):int((i+1)*N)])
  ventana6=np.array(GZ[int(i*N):int((i+1)*N)])
  #y=ventana1*ventana2*ventana3*ventana4
  #y=ventana1*ventana2*ventana3+ventana4+ventana6-ventana5
  #y=(ventana4+ventana5+ventana6+ventana3)/ventana1

  #y = ventana1*(ventana2)**1/2 + (ventana3*ventana4-ventana5**2) sirve
  y = ventana1*(ventana2)**1/2 + (ventana3*ventana4)
  #y = ventana1**(ventana2)*1/2 + (ventana3*ventana4)
  imagen[i,:]=y
plt.imshow(imagen,vmin=0,vmax=1)

"""### **Gesto giro a la derecha**"""

AX,AY,AZ,GX,GY,GZ=lectura("IABO/data/derecha/derecha_1.csv",0.0,0.0,0.0,0.0,0.0,0.0)
for i in range(2,21):
  AX,AY,AZ,GX,GY,GZ=lectura(f"IABO/data/derecha/derecha_{i}.csv",AX,AY,AZ,GX,GY,GZ)

from scipy.fftpack import  dct
size=(49,40)
EAY=np.multiply(AY,AY)
imagen=np.ones(size)/1.0
for i in range(0,49):
  ventana1=np.array(AX[int(i*N):int((i+1)*N)])
  ventana2=np.array(AY[int(i*N):int((i+1)*N)])
  ventana3=np.array(AZ[int(i*N):int((i+1)*N)])
  ventana4=np.array(GX[int(i*N):int((i+1)*N)])
  ventana5=np.array(GY[int(i*N):int((i+1)*N)])
  ventana6=np.array(GZ[int(i*N):int((i+1)*N)])
  #y=(ventana2*ventana3+ventana4)/(ventana6-ventana5) + ventana1**2
  #y=ventana1*ventana2*ventana3+ventana4+ventana6-ventana5
  #y=(ventana4+ventana5+ventana6+ventana3)/ventana1
  #y=(ventana1+ventana2)**1/2 
  #y = ventana1*(ventana2)**1/2 - (ventana3*ventana4-ventana5**2) + ventana6

  #y = ventana1*(ventana2)**1/2 + (ventana3*ventana4-ventana5**2) sirve
  y = ventana1*(ventana2)**1/2 + (ventana3*ventana4)
  #y = ventana1**(ventana2)*1/2 + (ventana3*ventana4)
  imagen[i,:]=y
plt.imshow(imagen,vmin=0,vmax=1)

"""### **Gesto giro a la izquierda**"""

AX,AY,AZ,GX,GY,GZ=lectura("IABO/data/izquierda/izquierda_1.csv",0.0,0.0,0.0,0.0,0.0,0.0)
for i in range(2,21):
  AX,AY,AZ,GX,GY,GZ=lectura(f"IABO/data/izquierda/izquierda_{i}.csv",AX,AY,AZ,GX,GY,GZ)

from scipy.fftpack import  dct
size=(49,40)
EAY=np.multiply(AY,AY)
imagen=np.ones(size)/1.0
for i in range(0,49):
  ventana1=np.array(AX[int(i*N):int((i+1)*N)])
  ventana2=np.array(AY[int(i*N):int((i+1)*N)])
  ventana3=np.array(AZ[int(i*N):int((i+1)*N)])
  ventana4=np.array(GX[int(i*N):int((i+1)*N)])
  ventana5=np.array(GY[int(i*N):int((i+1)*N)])
  ventana6=np.array(GZ[int(i*N):int((i+1)*N)])
  #y=(ventana1+ventana2)**1/2 no sirve en una imagen
  #y=ventana1*ventana2*ventana3+ventana4+ventana6-ventana5
  #y = ventana1*(ventana2)**1/2 - (ventana3*ventana4-ventana5**2) + ventana6

  #y = ventana1*(ventana2)**1/2 + (ventana3*ventana4-ventana5**2) sirve
  y = ventana1*(ventana2)**1/2 + (ventana3*ventana4)
  #y = ventana1**(ventana2)*1/2 + (ventana3*ventana4)
  imagen[i,:]=y
plt.imshow(imagen,vmin=0,vmax=1)