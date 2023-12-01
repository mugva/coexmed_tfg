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


def round_list(l):
    for i, v in enumerate(l):
        l[i] = round(v)
    return l


def polar_twin(ax):
    ax2 = ax.figure.add_axes(ax.get_position(), projection='polar',
                             label='twin', frameon=False,
                             theta_direction=ax.get_theta_direction(),
                             theta_offset=ax.get_theta_offset())
    ax2.xaxis.set_visible(False)
    # There should be a method for this, but there isn't... Pull request?
    ax2._r_label_position._t = (22.5 + 180, 0.0)
    ax2._r_label_position.invalidate()
    # Ensure that original axes tick labels are on top of plots in twinned axes
    for label in ax.get_yticklabels():
        ax.figure.texts.append(label)
    return ax2
