import numpy as np


def reforma(data: dict, keys=None) -> dict:
    """
    Reforma els arrays de les variables de data per tal que tinguin una única dimensió
    :param data: dict amb les variables a reformar
    :param keys: keys del dict data que es volen reformar (si no s'indica, es reformen totes. Must be iterable)
    :return: dict amb les variables reformades
    """
    if keys is None:
        keys = data.keys()

    for key in keys:
        data[key] = np.reshape(data[key], -1)  # -1 indica que es calculi automàticament la dimensió
    return data


def llegir_pkl(path: str) -> dict:
    """
    Llegeix arxius en un fitxer .pkl
    :param path: path del fitxer .pkl
    :return: dict
    """
    import pickle
    with open(path, 'rb') as f:
        data = pickle.load(f)
    return data
