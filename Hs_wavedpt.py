from apendixs import *
from apendixs import _path, _pathdata


var_name = 'Hs_wavedpt'
data_calc = None

# demanam si volem executar el càlcul
res = input('Aquest càlcul pot tardar molt. Vols continuar? (s/[n])')
if res not in ('s', 'S'):
    raise SystemExit

pas = 200
for reg in tqdm(range(0, 1400, pas), desc=f'Recorrem punts de malla de {pas} en {pas}'):
    data_reg = None
    for year in range(1950, 2023):
        data_raw = sio.loadmat(_pathdata + r"\{}.mat".format(year),
                               variable_names=(var_name,))
        data_temp = pd.DataFrame(data_raw[var_name][:, reg:reg + pas])
        data_reg = pd.concat([data_reg, data_temp], ignore_index=True) if data_reg is not None else data_temp
    data_calc_reg = data_reg.quantile(q=[0.5, 0.95, 0.99], axis=0)
    data_calc = pd.concat([data_calc, data_calc_reg], axis=1,
                          ignore_index=True) if data_calc is not None else data_calc_reg

# guardam sa variable percentils en format .pkl
res = input('Vols guardar els percentils en un fitxer .pkl? (s/[n])')
if res in ('s', 'S'):
    nom_arxiu = input('Nom de l\'arxiu ("percentils_Hs_wavedpt_FTS" per defecte) (sense extensió): ')
    if nom_arxiu == '':
        nom_arxiu = 'percentils_Hs_wavedpt_FTS'
    with open(_path + r"\pkls\{}.pkl".format(nom_arxiu), 'wb') as f:
        pickle.dump(data_calc, f)
