import pickle
import matplotlib.pyplot as plt
# import pandas as pd
from funcions import llegir_pkl

# flags ______________________________________________________________________________________________________________
flags = {
    'percentils.pkl': True,
    'Plot_general': False
}

# main _______________________________________________________________________________________________________________
if flags['percentils.pkl']:
    path = r"D:\tfg\percentils.pkl"
    percentils = llegir_pkl(path)

    percentils_reformat = {}

    punts_malla = [353, 764, 912, 1021, 1291, 1319, 1339, 1366]
    variables = ['elev_hydro', 'elev_wavedpt', 'Hs_wavedpt', 'Tp_wavedpt', 'Dp_wavedpt']

    for punt in punts_malla:
        percentils_reformat[punt] = {}
        for var in variables:
            percentils_reformat[punt][var] = {}
            for year in percentils.keys():
                percentils_reformat[punt][var][year] = percentils[year][var][punt]

if flags['Plot_general']:
    # ara llegim sa variable percentils
    with open(r"D:\tfg\percentils.pkl", 'rb') as f:
        percentils = pickle.load(f)

    # reformatejam el diccionari percentils perquè les keys siguin els punts de malla
    percentils_reformat = {}
    for punt in [353, 764, 912, 1021, 1291, 1319, 1339, 1366]:
        percentils_reformat[punt] = {}
        for year in percentils.keys():
            percentils_reformat[punt][year] = percentils[year]['Hs_wavedpt'][punt]

    # representam en un gràfic els percentils de cada punt de malla
    # volem fixar l'altura vertical a valors vixes compresos entre els 1 i 5 metres
    fig, ax = plt.subplots(2, 4, figsize=(10, 5))
    for i, punt in enumerate(percentils_reformat.keys()):
        ax[i // 4, i % 4].plot(percentils_reformat[punt].keys(), percentils_reformat[punt].values())
        ax[i // 4, i % 4].set_title('Punt {}'.format(punt))
        ax[i // 4, i % 4].set_xlabel('Any')
        ax[i // 4, i % 4].set_ylabel('Hs (m)')
        ax[i // 4, i % 4].grid()
        ax[i // 4, i % 4].set_ylim(1, 5.5)
    plt.tight_layout()
    plt.show()
