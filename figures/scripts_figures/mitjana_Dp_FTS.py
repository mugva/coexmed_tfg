from apendixs import *
from apendixs import _path


lat, lon, depth = lat_lon_depth()  # extreim les dades

# llegim dades
try:
    data_mean_res = llegir_pkl(_path + r"\pkls\mitjana_Dp_wavedpt_FTS.pkl")
except FileNotFoundError:
    raise FileNotFoundError('No s\'ha trobat l\'arxiu .pkl amb les dades de la mitjana de les direccions de l\'onatge')

# modificam els angles perquè vagin de 0 a 360
data_mean_res['angle'][np.where(data_mean_res['angle'] < 0)[0]] += 360

# llegim el colormap
rgb = np.loadtxt(_path + r"\figures\cmaps\cmocean_phase.rgb") / 255  # normalitzam els valors
cmocean_phase = ListedColormap(rgb)

# voldrem que la mida dels punts sigui proporcional al radi de les direccions
radi = data_mean_res['radi']

# plot

# Utilitzar LaTeX per a tots els textos del plot
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent([1., 4.5, 38.5, 40.5])
ax.add_feature(cfeature.COASTLINE.with_scale('10m'))
ax.add_feature(cfeature.LAND)

sc = ax.scatter(lon, lat, c=data_mean_res['angle'], cmap=cmocean_phase, s=10*radi, alpha=.8)

cbar = plt.colorbar(sc, ax=ax, label='Direcció de l\'onatge', orientation='horizontal', pad=0.05, aspect=40)
cbar.set_ticks([0, 90, 180, 270, 360])
cbar.set_ticklabels(['N', 'E', 'S', 'W', 'N'])

# gridlines
gl = ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.5, linestyle='--')
gl.top_labels = gl.right_labels = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
gl.xlocator = mticker.FixedLocator(range(1, 6, 1))  # adjust as per your extent
gl.ylocator = mticker.FixedLocator(range(38, 41, 1))  # adjust as per your extent

plt.show()

# guardam la figura
# fig.savefig(_path + r"\figures\pdf\mitjana_Dp_FTS.pdf", bbox_inches='tight')
# fig.savefig(_path + r"\figures\png\mitjana_Dp_FTS.png", bbox_inches='tight')
