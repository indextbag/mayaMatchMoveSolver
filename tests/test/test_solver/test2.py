"""
Semi-Complex hierarchy and object-space utilising solve.
"""

import time
import unittest

try:
    import maya.standalone
    maya.standalone.initialize()
except RuntimeError:
    pass
import maya.cmds


import test.test_solver.solverutils as solverUtils


# @unittest.skip
class TestSolver2(solverUtils.SolverTestCase):

    def test_init(self):
        cam_tfm = maya.cmds.createNode('transform', name='cam_tfm')
        cam_shp = maya.cmds.createNode('camera', name='cam_shp', parent=cam_tfm)
        maya.cmds.setAttr(cam_tfm + '.tx', -1.0)
        maya.cmds.setAttr(cam_tfm + '.ty',  1.0)
        maya.cmds.setAttr(cam_tfm + '.tz', -5.0)

        group_tfm = maya.cmds.createNode('transform', name='group_tfm')
        bundle1_tfm = maya.cmds.createNode('transform', name='bundle1_tfm', parent=group_tfm)
        bundle1_shp = maya.cmds.createNode('locator', name='bundle1_shp', parent=bundle1_tfm)
        bundle2_tfm = maya.cmds.createNode('transform', name='bundle2_tfm', parent=group_tfm)
        bundle2_shp = maya.cmds.createNode('locator', name='bundle2_shp', parent=bundle2_tfm)
        maya.cmds.setAttr(bundle1_tfm + '.tx', 10.0)
        maya.cmds.setAttr(bundle2_tfm + '.tx', -10.0)
        maya.cmds.setAttr(group_tfm + '.ry', 45.0)
        maya.cmds.setAttr(group_tfm + '.tz', -35.0)

        marker1_tfm = maya.cmds.createNode('transform', name='marker1_tfm', parent=cam_tfm)
        marker1_shp = maya.cmds.createNode('locator', name='marker1_shp', parent=marker1_tfm)
        maya.cmds.setAttr(marker1_tfm + '.tx', -2.5)
        maya.cmds.setAttr(marker1_tfm + '.ty', 1.3)
        maya.cmds.setAttr(marker1_tfm + '.tz', -10)

        marker2_tfm = maya.cmds.createNode('transform', name='marker2_tfm', parent=cam_tfm)
        marker2_shp = maya.cmds.createNode('locator', name='marker2_shp', parent=marker2_tfm)
        maya.cmds.setAttr(marker2_tfm + '.tx', 2.5)
        maya.cmds.setAttr(marker2_tfm + '.ty', -0.8)
        maya.cmds.setAttr(marker2_tfm + '.tz', -6.0)

        cameras = (
            (cam_tfm, cam_shp),
        )
        markers = (
            (marker1_tfm, cam_shp, bundle1_tfm),
            (marker2_tfm, cam_shp, bundle2_tfm),
        )
        node_attrs = [
            (group_tfm + '.tx', 'None', 'None'),
            (group_tfm + '.ty', 'None', 'None'),
            (group_tfm + '.tz', 'None', 'None'),
            (group_tfm + '.sx', 'None', 'None'),
            (group_tfm + '.ry', 'None', 'None'),
            (group_tfm + '.rz', 'None', 'None'),
        ]
        frames = [
            (1),
        ]

        # save the output
        path = self.get_data_path('solver_test2_before.ma')
        maya.cmds.file(rename=path)
        maya.cmds.file(save=True, type='mayaAscii', force=True)

        # Run solver, with more attributes than markers; We expect an error.
        s = time.time()
        result = maya.cmds.mmSolver(
            camera=cameras,
            marker=markers,
            attr=node_attrs,
            iterations=1000,
            frame=frames,
            verbose=True,
        )
        e = time.time()
        print 'total time:', e - s
        self.assertEqual(result[0], 'success=0')

        # Run solver! (with less attributes)
        node_attrs = [
            (group_tfm + '.tx', 'None', 'None'),
            (group_tfm + '.ty', 'None', 'None'),
            (group_tfm + '.sx', 'None', 'None'),
            (group_tfm + '.rz', 'None', 'None'),
        ]
        s = time.time()
        result = maya.cmds.mmSolver(
            camera=cameras,
            marker=markers,
            attr=node_attrs,
            iterations=1000,
            frame=frames,
            verbose=True,
        )
        e = time.time()
        print 'total time:', e - s

        # save the output
        path = self.get_data_path('solver_test2_after.ma')
        maya.cmds.file(rename=path)
        maya.cmds.file(save=True, type='mayaAscii', force=True)
        
        # Ensure the values are correct
        self.assertEqual(result[0], 'success=1')


if __name__ == '__main__':
    prog = unittest.main()
