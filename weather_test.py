from weatherrouting import Routing, Polar, Grib
from weatherrouting.routers.linearbestisorouter import LinearBestIsoRouter
from datetime import datetime

track = ((5.1, 38.1), (5.2, 38.4), (5.7, 38.2))
polar_obj = Polar("polar_files/first36.7.pol")