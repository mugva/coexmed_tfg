import pickle
import matplotlib.pyplot as plt
# import pandas as pd
from funcions import llegir_pkl

# PUNTS D'INTERÉS:
# 	MALLORCA:
# 		Portocolom:       lat 39.4056 lon 3.28015	1366
# 		Es Trenc:         lat 39.3139 lon 2.96132	1291
# 		Port de Sóller:   lat 39.8193 lon 2.70529	353
# 		Cap Farrutx:      lat 39.8188 lon 3.36039	1319
# 	MENORCA:
# 		Men. Nord:          lat 40.0658 lon 3.91506	764
# 		Men. Sud:           lat 39.8946 lon 4.04837	1021
# 	PITIÜSES:
# 		Eivissa Est:      lat 39.0998 lon 1.59909	912
# 		Formentera Sud:   lat 38.6297 lon 1.44099	1339

# variables __________________________________________________________________________________________________________
punts_interes = {'Portocolom': 1366, 'Es Trenc': 1291, 'Port de Sóller': 353, 'Cap Farrutx': 1319, 'Men. Nord': 764,
                 'Men. Sud': 1021, 'Eivissa Est': 912, 'Formentera Sud': 1339}

variables = ['elev_hydro', 'elev_wavedpt', 'Hs_wavedpt', 'Tp_wavedpt', 'Dp_wavedpt']

# flags ______________________________________________________________________________________________________________
flags = {
    'percentils.pkl': True,
    'Plot_general': True
}

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

if flags['Plot_general']:
    # ara llegim sa variable percentils
    with open(r"D:\tfg\percentils.pkl", 'rb') as f:
        percentils = pickle.load(f)

    # representam en un gràfic els percentils de cada punt de malla
    # volem fixar l'altura vertical a valors vixes compresos entre els 1 i 5 metres
    fig, ax = plt.subplots(2, 4, figsize=(10, 5))
    for i, punt in enumerate(percentils_reformat.keys()):
        ax[i // 4, i % 4].plot(percentils_reformat[punt].keys(), percentils_reformat[punt].values())
        ax[i // 4, i % 4].set_title('Punt {}'.format(punts_interes[punt]))
        ax[i // 4, i % 4].set_xlabel('Any')
        ax[i // 4, i % 4].set_ylabel('Hs (m)')
        ax[i // 4, i % 4].grid()
        ax[i // 4, i % 4].set_ylim(1, 5.5)
    plt.tight_layout()
    plt.show()
