from apendixs import *
from apendixs import _path, _pathdata


lat, lon, depth = lat_lon_depth()

# llegim dades
try:
    percentils_Hs_wavedpt_FTS = llegir_pkl(_path + r"\pkls\percentils_Hs_wavedpt_FTS.pkl")
except FileNotFoundError:
    raise FileNotFoundError('No s\'ha trobat l\'arxiu .pkl amb les dades dels percentils de l\'altura de l\'onatge')

# llegim el colormap
rgb = np.loadtxt(_path + r"\figures\cmaps\GMT_haxby.rgb")
gmt_haxby = ListedColormap(rgb)

#%% plot simple

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent([1., 4.5, 38.5, 40.5])
ax.add_feature(cfeature.COASTLINE.with_scale('10m'))
ax.add_feature(cfeature.LAND)

sc = ax.scatter(lon, lat, c=percentils_Hs_wavedpt_FTS.loc[0.5], cmap=gmt_haxby, s=10)

cbar = plt.colorbar(sc, ax=ax, label='Mediana de l\'altura de l\'onatge [m]', orientation='horizontal', pad=0.05, aspect=40)

# gridlines
gl = ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.5, linestyle='--')
gl.top_labels = gl.right_labels = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
gl.xlocator = mticker.FixedLocator(range(1, 6, 1))  # adjust as per your extent
gl.ylocator = mticker.FixedLocator(range(38, 41, 1))  # adjust as per your extent

plt.show()


#%% plot triple

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

fig, axs = plt.subplots(3, 1, figsize=(10, 25), subplot_kw={'projection': ccrs.PlateCarree()})

for i, ax in enumerate(axs):
    ax.set_extent([1., 4.5, 38.5, 40.5])
    ax.add_feature(cfeature.COASTLINE.with_scale('10m'))
    ax.add_feature(cfeature.LAND)

    sc = ax.scatter(lon, lat, c=percentils_Hs_wavedpt_FTS.loc[percentils_Hs_wavedpt_FTS.index[i]], cmap=gmt_haxby, s=10,
                    alpha=1)

    cbar = plt.colorbar(sc, ax=ax,
                        label=f'Percentil {percentils_Hs_wavedpt_FTS.index[i]} de l\'altura de l\'onatge [m]',
                        orientation='horizontal', pad=0.05, aspect=40)

    # gridlines
    gl = ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = gl.right_labels = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlocator = mticker.FixedLocator(range(1, 6, 1))  # adjust as per your extent
    gl.ylocator = mticker.FixedLocator(range(38, 41, 1))  # adjust as per your extent

plt.show()

# save the plot
# fig.savefig(_path + r"\figures\pdf\percentils_Hs_FTS.pdf", bbox_inches='tight')
# fig.savefig(_path + r"\figures\png\percentils_Hs_FTS.png", bbox_inches='tight')
