from apendixs import *
from apendixs import _path

lat, lon, depth = lat_lon_depth()  # extreim les dades

# ara llegirem el colormap que volem
rgb = np.loadtxt(_path + r"\figures\cmaps\cmocean_deep.rgb") / 255  # normalitzam els valors
cmocean_deep = ListedColormap(rgb)

# plot

# Utilitzar LaTeX per a tots els textos del plot
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': ccrs.PlateCarree()})

ax.set_extent([1., 4.5, 38.5, 40.5])
ax.add_feature(cfeature.COASTLINE.with_scale('10m'))  # resolucions: 10m, 50m, 110m
ax.add_feature(cfeature.LAND)

sc = ax.scatter(lon, lat, c=depth, cmap=cmocean_deep, s=5)

cbar = plt.colorbar(sc, ax=ax, label='Profunditat [m]', orientation='horizontal', pad=0.05, aspect=40)

# gridlines
gl = ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.5, linestyle='--')
gl.top_labels = gl.right_labels = False
gl.xformatter = LONGITUDE_FORMATTER
gl.yformatter = LATITUDE_FORMATTER
gl.xlocator = mticker.FixedLocator(range(1, 6, 1))  # adjust as per your extent
gl.ylocator = mticker.FixedLocator(range(38, 41, 1))  # adjust as per your extent

# zoom a platja de Muro
ax_inset = plt.axes([0.72, 0.3, 0.15, 0.15], projection=ccrs.PlateCarree())
ax_inset.set_extent([3.1, 3.4, 39.7, 40])
ax_inset.add_feature(cfeature.COASTLINE.with_scale('10m'))
ax_inset.add_feature(cfeature.LAND)
sc_inset = ax_inset.scatter(lon, lat, c=depth, cmap=cmocean_deep, s=7)
mark_inset(ax, ax_inset, loc1=1, loc2=3, fc="none", ec=".5", alpha=.4, linestyle='--')

# gridlins a l'inset
gl_inset = ax_inset.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.5, linestyle='--')
gl_inset.top_labels = gl_inset.right_labels = False
gl_inset.xformatter = LONGITUDE_FORMATTER
gl_inset.yformatter = LATITUDE_FORMATTER
gl_inset.xlocator = mticker.FixedLocator(np.arange(3.1, 3.6, 0.1))  # adjust as per your extent
gl_inset.ylocator = mticker.FixedLocator(np.arange(39.75, 40, 0.1))  # adjust as per your extent

# zoom al pas entre Eivissa i Formentera
ax_inset2 = plt.axes([0.2, 0.5, 0.15, 0.15], projection=ccrs.PlateCarree())
ax_inset2.set_extent([1.35, 1.5, 38.7, 38.9])
ax_inset2.add_feature(cfeature.COASTLINE.with_scale('10m'))
ax_inset2.add_feature(cfeature.LAND)
sc_inset2 = ax_inset2.scatter(lon, lat, c=depth, cmap=cmocean_deep, s=7)
mark_inset(ax, ax_inset2, loc1=2, loc2=4, fc="none", ec=".5", alpha=.4, linestyle='--')

# gridlins a l'inset2
gl_inset2 = ax_inset2.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.5, linestyle='--')
gl_inset2.top_labels = gl_inset2.right_labels = False
gl_inset2.xformatter = LONGITUDE_FORMATTER
gl_inset2.yformatter = LATITUDE_FORMATTER
gl_inset2.xlocator = mticker.FixedLocator([1.38, 1.46])  # adjust as per your extent
gl_inset2.ylocator = mticker.FixedLocator([38.75, 38.85])  # adjust as per your extent

plt.show()

# guardam la figura
# fig.savefig(_path + r"\figures\pdf\batimetria_malla.pdf", bbox_inches='tight')
# fig.savefig(_path + r"\figures\png\batimetria_malla.png", bbox_inches='tight')
