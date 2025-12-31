"""
Main module for geogee geopackage.

This module provides helper functions and an interactive Map class
built on top of ipyleaflet.
"""

import os
import json
import ee
import shapefile
import ipyleaflet
from .common import ee_initialize
from .utils import random_string
from ipyleaflet import (
    FullScreenControl,
    LayersControl,
    DrawControl,
    MeasureControl,
    ScaleControl,
    TileLayer,
)

# ---------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------

def shp_to_geojson(in_shp, out_geojson=None):
    """Converts a shapefile to GeoJSON."""

    in_shp = os.path.abspath(in_shp)

    if not os.path.exists(in_shp):
        raise FileNotFoundError("The provided shapefile could not be found.")

    sf = shapefile.Reader(in_shp)
    geojson = sf.__geo_interface__

    if out_geojson is None:
        return geojson

    out_geojson = os.path.abspath(out_geojson)
    os.makedirs(os.path.dirname(out_geojson), exist_ok=True)

    with open(out_geojson, "w") as f:
        json.dump(geojson, f)

    return geojson


# ---------------------------------------------------------------------
# Map class
# ---------------------------------------------------------------------

class Map(ipyleaflet.Map):
    """Interactive map based on ipyleaflet."""

    def __init__(self, **kwargs):
        kwargs.setdefault("center", [40, -100])
        kwargs.setdefault("zoom", 4)
        kwargs.setdefault("scroll_wheel_zoom", True)

        super().__init__(**kwargs)

        self.layout.height = kwargs.get("height", "500px")

        self.add_control(FullScreenControl())
        self.add_control(LayersControl(position="topright"))
        self.add_control(DrawControl(position="topleft"))
        self.add_control(MeasureControl())
        self.add_control(ScaleControl(position="bottomleft"))

        google_map = kwargs.get("google_map", "ROADMAP")

        if google_map == "HYBRID":
            url = "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}"
            name = "Google Satellite"
        else:
            url = "https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}"
            name = "Google Maps"

        self.add_layer(TileLayer(url=url, attribution="Google", name=name))

    # -----------------------------------------------------------------

    def add_geojson(self, in_geojson, style=None, layer_name="Untitled"):
        """Adds a GeoJSON layer to the map."""

        if layer_name == "Untitled":
            layer_name = f"Untitled_{random_string()}"

        if isinstance(in_geojson, str):
            if not os.path.exists(in_geojson):
                raise FileNotFoundError("GeoJSON file not found.")
            with open(in_geojson) as f:
                data = json.load(f)
        elif isinstance(in_geojson, dict):
            data = in_geojson
        else:
            raise TypeError("GeoJSON must be a file path or dict.")

        if style is None:
            style = {
                "stroke": True,
                "color": "#000000",
                "weight": 2,
                "opacity": 1,
                "fill": True,
                "fillColor": "#0000ff",
                "fillOpacity": 0.4,
            }

        self.add_layer(
            ipyleaflet.GeoJSON(data=data, style=style, name=layer_name)
        )

    # -----------------------------------------------------------------

    def add_shapefile(self, in_shp, style=None, layer_name="Untitled"):
        """Adds a shapefile layer to the map."""
        geojson = shp_to_geojson(in_shp)
        self.add_geojson(geojson, style=style, layer_name=layer_name)

    # -----------------------------------------------------------------

    def add_ee_layer(self, ee_object, vis_params={}, name=None, shown=True, opacity=1.0):
        """Adds an Earth Engine layer to the map."""
        layer = self.ee_tile_layer(
            ee_object, vis_params, name, shown, opacity
        )
        self.add_layer(layer)

    addLayer = add_ee_layer  # Earth Engine style alias

    # -----------------------------------------------------------------

    def ee_tile_layer(
        self, ee_object, vis_params={}, name="Layer untitled", shown=True, opacity=1.0
    ):
        """Converts an Earth Engine object to an ipyleaflet TileLayer."""

        if not isinstance(
            ee_object,
            (
                ee.Image,
                ee.ImageCollection,
                ee.Feature,
                ee.FeatureCollection,
                ee.Geometry,
            ),
        ):
            raise AttributeError(
                "ee_object must be an Earth Engine Image, Feature, or Collection."
            )

        if isinstance(ee_object, ee.ImageCollection):
            ee_object = ee_object.mosaic()

        map_id = ee_object.getMapId(vis_params)
        tile_url = map_id["tile_fetcher"].url_format

        tile_layer = TileLayer(
            url=tile_url,
            name=name,
            opacity=opacity,
            visible=shown,
            attribution="Google Earth Engine",
        )

        return tile_layer

    # -----------------------------------------------------------------
