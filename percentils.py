# import pickle
import matplotlib.pyplot as plt
# import pandas as pd
from funcions import llegir_pkl, round_list
from crea_fitxers import DATA
import numpy as np
from numpy import pi
from tqdm import tqdm

# variables __________________________________________________________________________________________________________
punts_interes = {'Portocolom': 1366, 'Es Trenc': 1291, 'Port de Sóller': 353, 'Cap Farrutx': 1319, 'Men. Nord': 764,
                 'Men. Sud': 1021, 'Eivissa Est': 912, 'Formentera Sud': 1339}

variables = ['elev_hydro', 'elev_wavedpt', 'Hs_wavedpt', 'Tp_wavedpt', 'Dp_wavedpt']

# main _______________________________________________________________________________________________________________
path = r"D:\tfg\percentils.pkl"
percentils = llegir_pkl(path)

percentils_reformat = {}

for punt in punts_interes.keys():
    percentils_reformat[punt] = {}
    for var in variables:
        percentils_reformat[punt][var] = {}
        for year in percentils.keys():
            percentils_reformat[punt][var][year] = percentils[year][var][punts_interes[punt]]

# main2 ______________________________________________________________________________________________________________
# volem llegir altura significativa i direccion de les onades als punts d'interes per a tots els anys
data = DATA(punts=punts_interes, variables=['Hs_wavedpt', 'Dp_wavedpt'])
# feim round a les direccions
for punt in punts_interes.keys():
    for anyi in data[punt]['Dp_wavedpt'].keys():
        round_list(data[punt]['Dp_wavedpt'][anyi])
anys = list(data[list(data.keys())[0]][list(data[list(data.keys())[0]].keys())[0]].keys())
# com que les direccions van de 15 en 15, ara volem comptar quants cops surt cada direcció per després poder fer un
# histograma radial
# separarem les dades només per punt, tendrem un diccionari amb 8 keys, una per cada punt i cada key tindrà un dict amb
# la direcció com a key i el nombre de cops que surt com a value (en tots els anys)

recompte_direccions = {}
for punt in punts_interes.keys():
    recompte_direccions[punt] = {}
    # inicialitzam el diccionari amb totes les direccions possibles
    for angle in range(0, 360, 15):
        recompte_direccions[punt][angle] = 0
    for anyi in anys:
        for val in data[punt]['Dp_wavedpt'][anyi]:
            recompte_direccions[punt][round(val)] += 1

# cream variable amb valors normalitzats
recompte_direccions_norm = {}
for punt in punts_interes.keys():
    recompte_direccions_norm[punt] = {}
    for angle in range(0, 360, 15):
        recompte_direccions_norm[punt][angle] = (recompte_direccions[punt][angle] /
                                                 sum(recompte_direccions[punt].values()))

# main3 ______________________________________________________________________________________________________________
# ara volem esbrinar quina és l'altura significativa màxima per a cada punt i direcció durant tota la serie temporal per
# poder-ho representar al mateix gràfic
# primer volem crear un diccionari estil dict[punt][direcció] = Hs max de tots els anys per aquella direcció
Hs_95_99 = {}
for punt in punts_interes.keys():
    Hs_95_99[punt] = {}
    Hs_any = []
    Dp_any = []
    for anyi in anys:
        Hs_any += data[punt]['Hs_wavedpt'][anyi]
        Dp_any += data[punt]['Dp_wavedpt'][anyi]
    for angle in tqdm(range(0, 360, 15), desc=f'Recorrent direccions de {punt}'):
        Hs_95_99[punt][angle] = {'p95': 0, 'p99': 0}
        idxs = np.array(Dp_any) == angle
        if True in idxs:
            p95 = np.percentile(np.array(Hs_any)[idxs], 95)
            p99 = np.percentile(np.array(Hs_any)[idxs], 99)
            Hs_95_99[punt][angle] = {'p95': p95, 'p99': p99}

# plot _______________________________________________________________________________________________________________
# Ara volem fer un diagrama de barres amb les direccions de les onades per a cada punt en plots radials. Cada barra, per
# tant, tendrà una amplada de 15 graus i una altura igual al nombre de cops que surt aquesta direcció.
# a més, volem dibuixar-hi una linia que representi els percentils 95 i 99 de l'altura significativa per a cada direcció
# i punt
# important que els percentils han d'estar representats en una escala diferent a la de les barres, per tant, hauran de
# estar en un altre eix y
from funcions import polar_twin

fig, axs = plt.subplots(2, 4, subplot_kw=dict(polar=True))
axs = axs.ravel()  # convertim l'array de 2x4 a un array de 8x1
for i, punt in enumerate(punts_interes.keys()):
    # Dibuixem les barres en l'eix Y
    axs[i].bar(x=np.array(list(recompte_direccions_norm[punt].keys())) * pi / 180,
               height=recompte_direccions_norm[punt].values(), width=15 * pi / 180)

    radii95 = []
    radii99 = []
    for angle in range(0, 360, 15):
        radii95.append(Hs_95_99[punt][angle]['p95'])
        radii99.append(Hs_95_99[punt][angle]['p99'])

    # Normalitzem les dades dels percentils al mateix rang que les dades de les barres
    # radii95_norm = [r / max(radii95) * max(recompte_direccions_norm[punt].values()) for r in radii95]
    # radii99_norm = [r / max(radii99) * max(recompte_direccions_norm[punt].values()) for r in radii99]

    # Dibuixem les línies dels percentils en el mateix eix Y que les barres
    ax2 = polar_twin(axs[i])
    ax2.plot(np.array(range(0, 360, 15)) * pi / 180, radii95, color='r')
    ax2.plot(np.array(range(0, 360, 15)) * pi / 180, radii99, color='g')
    ax2.set_theta_zero_location('N')
    ax2.set_theta_direction(-1)
    axs[i].set_title(punt)
    axs[i].set_theta_zero_location('N')
    axs[i].set_theta_direction(-1)

plt.show()
