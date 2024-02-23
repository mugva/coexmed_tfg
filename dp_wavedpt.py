"""
En primer lloc, volem estudiar la direcció de l'onatge per a veure d'on prové l'onatge a cada punt de malla
majoritàriament. Per a fer-ho, calcularem la mitjana de les direccions tenint en compte que són variables angulars i,
per tant, hem de fer servir les funcions sinus i cosinus per a calcular-ne la mitjana.
"""

from apendixs import *
from apendixs import _path, _pathdata

var_name = 'Dp_wavedpt'
data_mean_angle = None
data_mean_radi = None

# demanam si volem executar el càlcul
res = input('Aquest càlcul pot tardar molt. Vols continuar? (s/[n])')
if res not in ('s', 'S'):
    raise SystemExit

# sabem que tenim 1400 punts de malla (0-1399) i 8760 hores per any, com que la sèrie temporal tant sí com no la
# necessitam sencera, procedirem a fer el càlcul de 200 punts en 200 punts.
pas = 200
for reg in tqdm(range(0, 1400, pas), desc=f'Recorrem punts de malla de {pas} en {pas}'):
    data_sin, data_cos = None, None
    for year in range(1950, 2023):
        data_raw = sio.loadmat(_pathdata + r"\{}.mat".format(year), variable_names=(var_name,))
        data = np.round(data_raw[var_name]).astype(int)[:, reg:reg + pas]
        data_radians = np.round(np.deg2rad(data), 4)
        data_radians = pd.DataFrame(data_radians)
        data_sin_temp = data_radians.apply(np.sin)
        data_cos_temp = data_radians.apply(np.cos)
        data_sin = pd.concat([data_sin, data_sin_temp], ignore_index=True) if data_sin is not None else data_sin_temp
        data_cos = pd.concat([data_cos, data_cos_temp], ignore_index=True) if data_cos is not None else data_cos_temp
    data_sin_mean = data_sin.mean()
    data_cos_mean = data_cos.mean()
    data_mean_angle_reg = np.arctan2(data_sin_mean, data_cos_mean)
    data_mean_angle_reg = np.rad2deg(data_mean_angle_reg)
    data_mean_angle = pd.concat([data_mean_angle, data_mean_angle_reg], ignore_index=True) if data_mean_angle is not None else data_mean_angle_reg
    data_mean_radi_reg = np.sqrt(data_sin_mean ** 2 + data_cos_mean ** 2)
    data_mean_radi = pd.concat([data_mean_radi, data_mean_radi_reg], ignore_index=True) if data_mean_radi is not None else data_mean_radi_reg
data_mean_res = {'angle': data_mean_angle, 'radi': data_mean_radi}

# guardam sa variable percentils en format .pkl
res = input('Vols guardar la mitjana de les direccions en un fitxer .pkl? (s/[n])')
if res in ('s', 'S'):
    nom_arxiu = input('Nom de l\'arxiu ("mitjana_Dp_wavedpt_FTS" per defecte) (sense extensió): ')
    if nom_arxiu == '':
        nom_arxiu = 'mitjana_Dp_wavedpt_FTS'
    with open(_path + r"\pkls\{}.pkl".format(nom_arxiu), 'wb') as f:
        pickle.dump(data_mean_res, f)
