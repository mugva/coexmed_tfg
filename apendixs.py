#%% Apèndix 0
import scipy.io as sio
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm
# from mpl_toolkits.basemap import Basemap
from matplotlib.colors import ListedColormap
import pickle
# import cmocean
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import matplotlib.ticker as mticker
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

# globals
_path = r"D:\tfg\codi\coexmed_tfg"
_pathdata = r"D:\tfg\Data_CoExMed_Balears"

#%% Apèndix A
"""
A continuació definim funcions simples que ens poden resultar de gran utilitat en el desenvolupament del treball. 
Sovint són creades per a facilitar la lectura del codi i per a casos molt específics.

Difícilment seran depenents d'altres llibreries o funcions. Encara així aprofitam per a importar les llibreries que 
més sovint farem servir.
"""


def isiterable(obj):
    """
    Comprova si un objecte és iterable
    :param obj: objecte a comprovar
    :return: True si és iterable, False si no ho és
    """
    try:
        iter(obj)
        return True
    except TypeError:
        return False


def lat_lon_depth() -> list:  # TODO: funciona però ho he fet de manera ràpida, crec que se toca poder implementar dins sa funció extractor_dades empleant es parametre 'variables'. REVISAR
    """
    Retorna una llista amb les latituds, longituds i profunditats dels punts de la nostra malla espacial.
    :return: list [lat, lon, depth]
    """
    path = _pathdata + r"\1950.mat"
    data_raw = sio.loadmat(path, variable_names=['lat', 'lon', 'depth'])

    return [data_raw['lat'][0], data_raw['lon'][0], data_raw['depth'][0]]


def llegir_pkl(path: str) -> dict:
    """
    Llegeix arxius en un fitxer .pkl
    :param path: path del fitxer .pkl
    :return: dades del fitxer .pkl en format diccionari.
    """
    with open(path, 'rb') as f:
        data = pickle.load(f)
    return data


#%% Apèndix B
"""
Introduïm aqui funcions pròpies de certa complexitat que ens seran d'utilitat més envant.

La funcionalitat, explicació i exemples d'ús de cada funció es troba documentada dins el mateix codi.
"""


def extractor_dades(punts='def', variables='def', anys=range(1950, 2023)) -> dict:
    """
    Llegeix les dades dels punts i variables que li indiquem. El diccionari resultant està ordenat per claus: punt, any, variable.
    Recordem que les dades són horàries i, per tant, cada any conté 8760 valors.
    :param punts: Punt o punts dels quals es volen llegir les dades. 'def' pels 8 punts d'interès, 'tot' per tots els punts. Ha de ser un enter o un objecte iterable d'enters.
    :param variables: Ídem que punts, però per les variables. 'def' per les 5 variables usuals, 'tot' per totes les variables. Ha de ser un string o un objecte iterable de strings.
    :param anys: Anys dels quals es volen llegir les dades.
    :return: dict amb les dades llegides.
    """
    if punts == 'def':  # punts per defecte
        punts = {'Portocolom': 1366, 'Es Trenc': 1291, 'Port de Sóller': 353, 'Cap Farrutx': 1319,
                 'Men. Nord': 764, 'Men. Sud': 1021, 'Eivissa Est': 912, 'Formentera Sud': 1339}
    elif punts == 'tot':  # tots els punts
        # TODO: fer que també funcioni si es volen llegir tots els punts
        raise NotImplementedError()
    elif not isinstance(punts, (int, list, tuple, dict)):
        # TODO: revisar aquest cas
        raise TypeError('Format no vàlid per a punts. Ha de ser int, list o tuple')

    if variables == 'def':  # variables per defecte
        variables = ('elev_hydro', 'elev_wavedpt', 'Hs_wavedpt', 'Tp_wavedpt', 'Dp_wavedpt')
    elif variables == 'tot':  # totes les variables
        # TODO: fer que també funcioni si es volen llegir totes les variables
        raise NotImplementedError('Encara no s\'ha implementat la lectura de totes les variables')
    elif not isinstance(variables, (str, list, tuple)):
        # TODO: revisar aquest cas
        raise TypeError('Format no vàlid per a variables. Ha de ser str, list o tuple')

    # TODO: fer comprovacions sobre els valors que s'introdueixen dins anys

    data = {}
    for anyi in tqdm(anys, desc='Llegint anys'):
        path = _pathdata + r"\{}.mat".format(anyi)
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


# COMPROVACIÓ
# dades_1999 = extractor_dades(punts='def', variables='def', anys=[1999])
# print(dades_1999['Portocolom']['elev_hydro'][1999][:10])


def plot_costa_Basemap(axi, reg=None, lati=None, loni=None,
                       res='h'):  # TODO: BORRAR, ara mateix ja no s'emplea perquè tenim Cartopy. Refer funció empleant cartopy
    """
    Pinta la línia de costa de la regió que li indiquem. Si no li indiquem res, pinta la línia de costa de les Illes Balears.
    :param axi: Eix sobre el qual volem pintar la línia de costa.
    :param reg: Regió de la qual volem pintar la línia de costa. Si no s'indica, es pintarà la línia de costa de les Illes Balears.
    :param lati: Latituds de la regió de la qual volem pintar la línia de costa.
    :param loni: Longituds de la regió de la qual volem pintar la línia de costa.
    :param res: Resolució de la línia de costa. 'c' per crude, 'l' per low, 'i' per intermediate, 'h' per high, 'f' per full.
    :return: None
    """

    # comprovam que els arguments siguin correctes
    if reg is not None and (lati is not None or loni is not None):
        raise ValueError('No es poden indicar simultàniament regió i latitud/longitud')
    if reg is None and (lati is None or loni is None):
        raise ValueError('S\'ha d\'indicar regió o latitud/longitud')
    regions_permeses = ('IB', 'MALL', 'MEN', 'EIV', 'FOR', 'MALL_MEN', 'PITI', 'TEST')
    if reg is not None:
        if not isinstance(reg, str):
            raise TypeError(
                'El nom de la regió ha de ser un string. Els valors permesos són: IB, MALL, MEN, EIV, FOR, MALL_MEN, '
                'PITI o TEST')
        reg = reg.upper()
        if reg not in regions_permeses:
            raise ValueError(
                'El nom de la regió no és vàlid. Els valors permesos són: IB, MALL, MEN, EIV, FOR, MALL_MEN, '
                'PITI o TEST')
        elif reg == 'IB':
            lati = [38.5, 40.5]
            loni = [1., 4.5]
        elif reg == 'MALL':
            lati = [39.2, 40.2]
            loni = [2.5, 4.5]
        # TODO: completar la resta de regions
    if lati is not None and loni is not None:
        if not isiterable(lati) or not isiterable(loni):
            raise TypeError('lat i lon han de ser objectes iterables')
        if len(lati) < 2 or len(loni) < 2:
            raise ValueError('lat i lon han de tenir com a mínim 2 valors')

    m = Basemap(projection='mill', llcrnrlat=min(lati), urcrnrlat=max(lati), llcrnrlon=min(loni), urcrnrlon=max(loni),
                resolution=res, ax=axi)
    m.drawcoastlines()

    return m


# COMPROVACIÓ
# import matplotlib.pyplot as plt
# plot_costa('IB')
# plt.show()


def crear_percentils(var_names=None, punts=None, full_time_series=False) -> None:
    """
    Crea un fitxer .pkl amb els percentils de les variables d'interès per a tots els punts.
    :param var_names: Noms de les variables d'interès. Per defecte ('elev_hydro', 'elev_wavedpt', 'Hs_wavedpt', 'Tp_wavedpt', 'Dp_wavedpt').
    :param punts: Punts espacials dels quals es volen calcular els percentils. Per defecte els 8 punts d'interès.
    :param full_time_series: Si es vol calcular la sèrie temporal completa. Si és False (per defecte), es calcularan els percentils per cada any.
    :return:
    """
    # demanam a l'usuari si vol executar la funció, ja que pot trigar molt
    res = input('Aquesta funció pot tardar molt. Vols continuar? (s/[n])')
    if res not in ('s', 'S'):
        return

    if var_names is None:
        var_names = ('elev_hydro', 'elev_wavedpt', 'Hs_wavedpt', 'Tp_wavedpt', 'Dp_wavedpt')
    elif not isiterable(var_names):
        raise TypeError(
            'var_names ha de ser un objecte iterable tot i que sigui d\'un sol element. Ex.: ("elev_hydro",) o ["elev_hydro"]')

    if punts is None:
        punts = [353, 764, 912, 1021, 1291, 1319, 1339, 1366]
    elif punts == 'tot':
        punts = list(range(0, np.shape(sio.loadmat(_pathdata + r"\1950.mat")['lat'])[1]))
    elif not isiterable(punts):
        raise TypeError('punts ha de ser un objecte iterable tot i que sigui d\'un sol element. Ex.: (353,) o [353]')

    if full_time_series:
        if len(var_names) > 1:
            raise Exception(
                'Si es vol calcular la sèrie temporal completa, només es pot calcular una variable a la vegada per evitar que el càlcul sigui massa llarg.')

    percentils_res = {}
    decimals = None
    df = {}
    var_name = var_names[0]
    if full_time_series:
        # demanam si és necessari arredonir els valors de les variables i si és així, quants decimals
        siround = input('Vols arrodonir els valors de les variables? (s/[n])')
        if siround in ('s', 'S'):
            decimals = int(input('A quants decimals?'))
    for year in tqdm(range(1950, 2023), desc='Càlcul percentils per any'):
        # TODO: fer que l'usuari tengui l'opció de aturar el procés (per cada 10 anys per exemple demanar si es vol continuar)
        # TODO: fer que funcioni si es vol calcular la sèrie temporal completa
        data_raw = sio.loadmat(_pathdata + r"\{}.mat".format(year), variable_names=var_names)
        # cream diccionari de dataframes
        if not full_time_series:
            df = {}
            for key in var_names:
                df[key] = pd.DataFrame(data=data_raw[key])
            # ens quedam només amb les columnes (punts espacials) d'interès
            df_punts = {}
            for key in df.keys():
                df_punts[key] = df[key].iloc[:, punts]
            # calculam els percentils
            percentils_i = {}
            for key in df_punts.keys():
                percentils_i[key] = df_punts[key].quantile(q=[0.5, 0.95, 0.99], axis=0)
            # guardam dins un dict
            percentils_res[year] = percentils_i
        elif full_time_series and var_name == 'Dp_wavedpt':
            data = data_raw['Dp_wavedpt']
            if decimals:
                data = np.round(data, decimals)
                if decimals == 0:
                    data = data.astype(int)
            if var_name not in df.keys():
                df[var_name] = data
            else:
                df[var_name] = np.concatenate([df[var_name], data], axis=0)

    # guardam sa variable percentils en format .pkl
    res = input('Vols guardar els percentils en un fitxer .pkl? (s/[n])')
    if res in ('s', 'S'):
        nom_arxiu = input('Nom de l\'arxiu ("percentils" per defecte) (sense extensió): ')
        if nom_arxiu == '':
            nom_arxiu = 'percentils'
        with open(_path + r"\pkls\{}.pkl".format(nom_arxiu), 'wb') as f:
            pickle.dump(percentils_res, f)

# COMPROVACIÓ
# crear_percentils()
