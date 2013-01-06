from django_assets import Bundle, register

leaflet_js = Bundle(
    'leaflet/leaflet-src.js',
    filters='jsmin',
    output='assets/leaflet.min.js'
)

leaflet_css = Bundle(
    'leaflet/leaflet.css',
    output='assets/leaflet.min.css'
)

worshipmap_js = Bundle(
    leaflet_js,
    'js/worshipmap.js',
    filters='jsmin',
    output='assets/worshipmap.min.js'
)

worshipmap_css = Bundle(
    leaflet_css,
    output='assets/worshipmap.min.css'
)

register('leaflet_js', leaflet_js)
register('leaflet_css', leaflet_css)
register('worshipmap_js', worshipmap_js)
register('worshipmap_css', worshipmap_css)
