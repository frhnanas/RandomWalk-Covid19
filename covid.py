# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 04:21:48 2020

@author: Farhan
"""


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Populasi:
    def __init__(individu,i, posx, posy, x, y, t_pulih, bergerak):
        # ID tiap Individu
        individu.id = i
        
        # Penempatan tiap Individu
        individu.x = x
        individu.y = y

        # Posisi tiap Individu
        individu.posx = posx
        individu.posy = posy
        
        # Status tiap Individu (Terinfeksi/Imun)
        individu.terinfeksi = False
        individu.sembuh = False
        individu.imun = False
        
        # Individu bergerak/tidak
        individu.bergerak = bergerak

        # Pergerakan tiap Individu
        if individu.bergerak:
            individu.deltax = 0
            individu.deltay = 0
        else:
            individu.deltax = (individu.x - individu.posx)
            individu.deltay = (individu.y - individu.posy)

        # Waktu saat Individu Terinfeksi
        individu.t_terinfeksi = -1
        
        # Waktu pemulihan
        individu.t_pulih = t_pulih


    def __str__(individu):
        return "Individu "+individu.id+" berada di ("+str(individu.posx)+", "+str(individu.posy)+")"

    def cek_sehat(individu,i):
        # Mengubah status Individu menjadi Sehat jika waktu Terinfeksi melebihi waktu Pemulihan
        if individu.t_terinfeksi>-1:
            if i-individu.t_terinfeksi>individu.t_pulih:
                individu.pulih()
                
    def infeksi(individu,i):
        # Keadaan saat Individu Terinfeksi
        individu.terinfeksi = True
        individu.sembuh = False
        individu.imun = False
        individu.t_terinfeksi = i

    def pulih(individu):
        # Keadaan saat Individu Pulih (pulih = imun terhadap virus)
        individu.terinfeksi = False
        individu.sembuh = True
        individu.imun = True

    def set_posisi(individu,x,y):
        # Menempatkan tiap Individu ke posisi
        individu.x = x
        individu.y = y
        if individu.bergerak:
            individu.deltax = 0
            individu.deltay = 0
        else:
            individu.deltax = (individu.x - individu.posx)
            individu.deltay = (individu.y - individu.posy)
    def get_pos(individu):
        return (individu.posx,individu.posy)
    
    def update_pos(individu, n_posx, n_posy):
        # Fungsi untuk membuat pergerakan
        if(n_posx==0 and n_posy==0):
            individu.posx = individu.posx + individu.deltax
            individu.posy = individu.posy + individu.deltay
        else:
            individu.posx = n_posx
            individu.posy = n_posy

        # Generate Random
        rand = np.random.rand()
        # kanan
        if(rand<=0.25):
            individu.posx = individu.posx + 1
        # bawah
        elif(rand<=0.50):
            individu.posy = individu.posy - 1
        # kiri
        elif(rand<=0.75):
            individu.posx = individu.posx - 1
        # atas
        else:
            individu.posy = individu.posy + 1
        
        # Koreksi PBC
        if (individu.posx > 20): 
            individu.posx = individu.posx - 20
        if (individu.posx < 0): 
            individu.posx = individu.posx + 20
        if (individu.posy > 20):
            individu.posy = individu.posy - 20
        if (individu.posy < 0): 
            individu.posy = individu.posy + 20

    def get_warna(individu):
        if individu.terinfeksi:
            return 'red'
        else:
            return 'black'


# inisialisasi
n = 200  # Individu = 200 individu
r_infeksi = 5  # Rasio Individu Terinfeksi = 5%
t_pulih = 10   # Waktu pemulihan = 10 hari
p_bergerak = 80  # Probabilitas Individu bergerak = 80%

terinfeksi = 0
populasi = []

# Generate Individu di posisi andom dan infeksi 5%
for i in range(n):
    p = Populasi(i, np.random.randint(low=0, high=20), np.random.randint(low=0, high=20), 
                np.random.randint(low=0, high=20), np.random.randint(low=0, high=20),t_pulih, False)

    if np.random.rand()<r_infeksi/100:
        p.infeksi(0)
        terinfeksi = terinfeksi+1
    if np.random.rand()>p_bergerak/100:
        p.bergerak = True

    populasi.append(p)

# Fungsi Plot/Visualisasi

fig = plt.figure(figsize=(18,9))
ax = fig.add_subplot(1,2,1)
cx = fig.add_subplot(1,2,2)
ax.axis('off')
cx.axis([0,50,0,n])

scatt = ax.scatter([p.posx for p in populasi], [p.posy for p in populasi],c='blue',s=8)
ruang = plt.Rectangle((0,0),20,20,fill=False) # Ukuran ruang = 20 x 20 unit
ax.add_patch(ruang)

grafik1,=cx.plot(terinfeksi,color="red",label="Terinfeksi")
grafik2,=cx.plot(terinfeksi,color="black",label="Tidak Terinfeksi")
cx.legend(handles=[grafik2,grafik1])
cx.set_xlabel("Waktu (hari)")
cx.set_ylabel("Jumlah Individu")

inf = [terinfeksi]
smb = [0]
t = [0]


# Fungsi update Posisi tiap Individu per Frame
def update(frame,smb,inf,t):
    terinfeksi = 0
    recover = 0
    warna = []
    for p in populasi:
        # cek durasi sakit tiap individu
        p.cek_sehat(frame)

        # Animasi pergerakan tiap Individu
        p.update_pos(0,0)
        
        if p.sembuh:
            recover += 1 # Jumlah Individu yang Pulih
        if p.terinfeksi:
            terinfeksi += 1 # Jumlah Individu yang Terinfeksi
            # Cek penyebaran virus
            for org in populasi:
                if org.id==p.id or org.terinfeksi or org.sembuh or org.imun:
                    pass
                else:
                    pos1 = p.get_pos()
                    pos2 = org.get_pos()
                    if pos1==pos2:
                        org.infeksi(frame)

        warna.append(p.get_warna()) # merah Terinfeksi, hitam tidak Terinfeksi

    print("Hari ke",frame,":",int(terinfeksi),"Terinfeksi")

    #kondisi stop jika jumlah terinfeksi sudah 0
    if terinfeksi == 0:
        animation.event_source.stop()

    # Update Plot
    smb.append(recover)
    inf.append(terinfeksi)
    t.append(frame)

    # Visualisasi Matplotlib
    offsets = np.array([[p.posx for p in populasi], [p.posy for p in populasi]])
    scatt.set_offsets(np.ndarray.transpose(offsets))
    scatt.set_color(warna)
    grafik1.set_data(t,inf)
    grafik2.set_data(t,smb)
    return scatt,grafik1,grafik2

#Menjalankan Animasi
animation = FuncAnimation(fig, update, interval=10,fargs=(smb,inf,t),blit=True)
plt.title("Simulasi Penyebaran Virus")
plt.show()