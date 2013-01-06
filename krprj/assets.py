from django_assets import Bundle, register

base_js = Bundle(
    'jquery/jquery-1.8.3.min.js',
    'raven/raven-0.7.1.min.js',
    'raven/raven-config.js',
    'bootstrap/js/bootstrap.min.js',
    output='assets/base.min.js'
)

base_css = Bundle(
    'bootstrap/css/bootstrap.min.css',
    'bootstrap/css/bootstrap-responsive.min.css',
    output='assets/base.min.css'
)

register('base_js', base_js)
register('base_css', base_css)
