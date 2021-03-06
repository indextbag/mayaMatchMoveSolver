"""
This tool averages markers position from selected markers.
"""

import maya.cmds

import mmSolver.logger
import mmSolver.api as mmapi

import mmSolver.tools.selection.filternodes as filternodes
import mmSolver.tools.averagemarker.lib as lib

LOG = mmSolver.logger.get_logger()


def main():
    """
    Averages marker position from selected markers.
    """
    selection = maya.cmds.ls(selection=True, long=True) or []
    selected_markers = filternodes.get_marker_nodes(selection)
    if len(selected_markers) < 2:
        LOG.warning('Please select more than 1 marker')
        return

    mkr_selection = selected_markers[0]
    mkr = mmapi.Marker(node=mkr_selection)
    # getting camera from the selected marker
    cam_from_mkr = mkr.get_camera()
    mkr_name = mmapi.get_marker_name('avgMarker1')
    new_mkr = mmapi.Marker().create_node(cam=cam_from_mkr,
                                         name=mkr_name)

    new_mkr_node = new_mkr.get_node()
    bnd_name = mmapi.get_bundle_name('avgBundle1')
    new_bnd = mmapi.Bundle().create_node(name=bnd_name)
    # connecting bundle to the marker
    new_mkr.set_bundle(new_bnd)

    # getting first frame and last frame from the selected markers
    start_frame, end_frame = lib.__get_markers_start_end_frames(
                                                    selected_markers)

    # Running average from selected markers for giving frame range
    lib.__set_average_marker_position(selected_markers,
                                      start_frame,
                                      end_frame,
                                      new_mkr_node)

    maya.cmds.select(new_mkr_node)
    # dgdirty for Channel box value update
    maya.cmds.dgdirty(new_mkr_node)
    return None
