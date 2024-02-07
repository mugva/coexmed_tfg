from funcions import reforma
import pandas as pd
import scipy.io as sio
from tqdm import tqdm
import pickle

# flags ______________________________________________________________________________________________________________
flags = {
    'Crea_csv_coords': False,
    'Lector_costa': False,
    'Lector_batimetria': False,
    'Percentils_temp': False
}

# main _______________________________________________________________________________________________________________
if flags['Crea_csv_coords']:
    path = r"D:\tfg\Data_CoExMed_Balears\1950.mat"

    coords = sio.loadmat(path, variable_names=('lat', 'lon'))
    coords = reforma(data=coords, keys=('lat', 'lon'))
    # guardam únicament les coordenades
    coords = pd.DataFrame({key: coords[key] for key in coords.keys() if key in ['lat', 'lon']})

    # guardam dict en un csv
    res = input('Vols guardar les coordenades en un csv? (s/[n])')
    if res in ('s', 'S'):
        coords.to_csv(r'D:\tfg\coords.csv', index=True, index_label='index')

    # ara cercam ses coordenades des nostros punts d'interés
    punts = [353, 764, 912, 1021, 1291, 1319, 1339, 1366]
    coords_punts_int = coords.iloc[punts, :]
    res = input('Vols guardar les coordenades dels punts d\'interés en un csv? (s/[n])')
    if res in ('s', 'S'):
        coords_punts_int.to_csv(r'D:\tfg\coords_punts_int.csv', index=True, index_label='index')

elif flags['Lector_costa']:  # no funciona
    # llegim arxiu matlab v7.3
    import h5py

    path = r"D:\tfg\Costas_Islas_Baleares.mat"
    f = h5py.File(path, 'r')
    # guardam les variables en un dict
    costa = {}
    for key in f.keys():
        costa[key] = f[key][:]


elif flags['Lector_batimetria']:  # no funciona
    # llegiu arxiu en format csv
    path = r"D:\tfg\Mean depth in multi colour (no land)\Mean depth in multi colour (no land).csv"
    batimetria = pd.read_csv(path, sep=',', header=0, index_col=0, encoding='charmap')


elif flags['Percentils_temp']:
    '''
    Per llegir els percentils guardats en un fitxer .pkl, emprau sa funció llegir_pkl() de funcions.py
    '''
    # calculam es percentils 95 i 99 de cada any de l'altura significativa
    # per fer-ho recorrem cada arxiu del 1950 fins a 2020
    percentils = {}
    # empleam sa llibraria tqdm per fer una barra de progrés
    for year in tqdm(range(1950, 2023), desc='Càlcul percentils per any'):
        path = r"D:\tfg\Data_CoExMed_Balears\{}.mat".format(year)
        var_names = ('elev_hydro', 'elev_wavedpt', 'Hs_wavedpt', 'Tp_wavedpt', 'Dp_wavedpt')
        data_raw = sio.loadmat(path, variable_names=var_names)
        # cream diccionari de dataframes
        df = {}
        for key in var_names:
            df[key] = pd.DataFrame(data=data_raw[key])
        # ens quedam només amb les columnes (punts espaials) d'interès
        punts = [353, 764, 912, 1021, 1291, 1319, 1339, 1366]
        df_punts = {}
        for key in df.keys():
            df_punts[key] = df[key].iloc[:, punts]
        # calculam els percentils
        percentils_i = {}
        for key in df_punts.keys():
            percentils_i[key] = df_punts[key].quantile(q=[0.95, 0.99], axis=0)
        # guardam dins un dict
        percentils[year] = percentils_i

    # guardam sa variable percentils en format .py
    res = input('Vols guardar els percentils en un fitxer .pkl? (s/[n])')
    if res in ('s', 'S'):
        with open(r"D:\tfg\percentils.pkl", 'wb') as f:
            pickle.dump(percentils, f)


# ara definirem una funció que ens permeti llegir totes les dades dels punts que li indiquem, així com de les variables
# que li indiquem, i que ens retorni un diccionari amb totes les dades ordenat per punt, any i variable.
# en cas de omitir les variables, retornarà totes les variables i en cas d'omitir els punts, retornarà tots els punts
def DATA(punts=None, variables=None, anys=range(1950, 2023)) -> dict:
    """
    Llegeix totes les dades dels punts que li indiquem, així com de les variables que li indiquem, i que ens retorni un
    diccionari amb totes les dades ordenat per punt, any i variable.
    :param punts: punts d'on es volen llegir les dades. 'tots' per llegir totes les dades, None per els punts d'interés
    :param variables: variables que es volen llegir. None per llegir totes les variables
    :param anys: anys dels quals es volen llegir les dades
    :return: dict amb les dades llegides
    """
    if variables is None:
        variables = ['elev_hydro', 'elev_wavedpt', 'Hs_wavedpt', 'Tp_wavedpt', 'Dp_wavedpt']
    if punts is None:
        punts = {'Portocolom': 1366, 'Es Trenc': 1291, 'Port de Sóller': 353, 'Cap Farrutx': 1319,
                 'Men. Nord': 764, 'Men. Sud': 1021, 'Eivissa Est': 912, 'Formentera Sud': 1339}
    elif punts == 'tots':
        # TODO: fer que també funcioni si es volen llegir tots els punts
        pass

    data = {}
    for anyi in tqdm(anys, desc='Llegint anys'):
        path = r"D:\tfg\Data_CoExMed_Balears\{}.mat".format(anyi)
        data_raw = sio.loadmat(path, variable_names=variables)

        df_tot = {}
        for key in variables:
            df_tot[key] = pd.DataFrame(data=data_raw[key])

        df_punts = {}
        for key in df_tot.keys():
            df_punts[key] = df_tot[key].iloc[:, list(punts.values())]

        data[anyi] = df_punts

    # posam amb l'ordre desitjat, reformam i retornam
    data_ref = {}
    for kpunt, vpunt in punts.items():
        data_ref[kpunt] = {}
        for var in variables:
            data_ref[kpunt][var] = {}
            for anyi in anys:
                data_ref[kpunt][var][anyi] = list(data[anyi][var][vpunt])

    return data_ref
