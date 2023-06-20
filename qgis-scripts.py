"""
/***************************************************************************
 *                                                                         *
 *   Laurent Rothuizen                                                     *
 *   Python script with various functions to add layers to a QGIS project  *                                                                      
 *   Work in Progress                                                      *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.core import (
    QgsProject, 
    QgsRasterLayer,
    QgsVectorLayer
)
import urllib.request, urllib.parse, urllib.error


def quote_wmts_url(url):
    """
    Quoten wmts url is nodig omdat qgis de query param `SERVICE=WMS` erachter plakt als je de wmts url niet quote.
    Dit vermoedelijk omdat de wmts laag wordt toegevoegd mbv de wms provider: `return QgsRasterLayer(uri, title, "wms")`.
    Wat op basis van de documentatie wel de manier is om een wmts laag toe te voegen.
    """
    parse_result = urllib.parse.urlparse(url)
    location = f"{parse_result.scheme}://{parse_result.netloc}/{parse_result.path}"
    query = parse_result.query
    query_escaped_quoted = urllib.parse.quote_plus(query)
    url = f"{location}?{query_escaped_quoted}"
    return url


# Functie die een WMS laag returned
def load_wms(
    url, crs="EPSG:28992", layername="", selected_style_name="", imgformat="image/png"
):
    uri = f"crs={crs}&layers={layername}&styles={selected_style_name}&format={imgformat}&url={url}"
    layer = QgsRasterLayer(uri, f"{layername} (WMS)", "wms")

    return layer


# Functie die een WMTS laag returned
def load_wmts(
    url,
    crs="EPSG:28992",
    tilematrixset="EPSG:28992",
    layername="",
    selected_style_name="default",
    imgformat="image/png",
):
    uri = f"tileMatrixSet={tilematrixset}&crs={crs}&layers={layername}&styles={selected_style_name}&format={imgformat}&url={quote_wmts_url(url)}"
    layer = QgsRasterLayer(uri, f"{layername} (WMTS)", "wms")

    return layer

# Functie die een WFS laag returned
def load_wfs(
    url,
    title="",
    layername="",
):
    uri = f" pagingEnabled='true' restrictToRequestBBOX='1' srsname='EPSG:28992' typename='{layername}' url='{url}' version='auto'" #EPSG:3857
    layer = QgsVectorLayer(uri, f"{title} (WFS)", "wfs")

    return layer

# Functie die een OAPIF laag returned
def load_oapif(
    url,
    title="",
    layername="",
):
    uri = f"typename='{layername}' url='{url}'"
    # uri = f" pagingEnabled='true' restrictToRequestBBOX='1' srsname='EPSG:28992' typename='{layername}' url='{url}' version='auto'"
    layer = QgsVectorLayer(uri, f"{title} (OAPIF)", "OAPIF")

    return layer


def create_layers():
    layers = []
    new_wms = load_wms(
        "https://service.pdok.nl/kadaster/bestuurlijkegebieden/wms/v1_0",
        "EPSG:3857",
        "Provinciegebied",
    )
    layers.append(new_wms)
    new_oapif = load_oapif(
        "https://test.haleconnect.de/ogcapi/datasets/simplified-addresses/",
        "SimpleAddress",
        "SimpleAddress"
    )
    layers.append(new_oapif)
    new_wfs = load_wfs(
        "https://service.pdok.nl/kadaster/bestuurlijkegebieden/wfs/v1_0",
        "Provinciegebied",
        "bestuurlijkegebieden:Provinciegebied"
    )
    layers.append(new_wfs)
    new_wmts = load_wmts(
        "https://service.pdok.nl/brt/achtergrondkaart/wmts/v2_0?request=getcapabilities&service=wmts",
        "EPSG:28992",
        "EPSG:28992",
        "pastel",
    )
    layers.append(new_wmts)
    return layers

def add_layers_to_qgis(layers):
    project_root = QgsProject.instance().layerTreeRoot()
    for group in [child for child in project_root.children() if child.nodeType() == 0]:
        if group.name() == "python_layers":
            project_root.removeChildNode(group)
    project_root.addGroup("python_layers")
    output_group = project_root.findGroup("python_layers")
    for layer in layers:
        output_group.addLayer(layer) 
    return None 

#
#
#

layer_list = create_layers()
add_layers_to_qgis(layer_list)
print('FINISHED')
    
