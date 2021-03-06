/*
 * Copyright (C) 2018, 2019 David Cattermole.
 *
 * This file is part of mmSolver.
 *
 * mmSolver is free software: you can redistribute it and/or modify it
 * under the terms of the GNU Lesser General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * mmSolver is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with mmSolver.  If not, see <https://www.gnu.org/licenses/>.
 * ====================================================================
 *
 * Uses Non-Linear Least Squares algorithm to
 * calculate attribute values based on 2D-to-3D error measurements
 * through a pinhole camera.
 */


#ifndef MAYA_MM_SOLVER_H
#define MAYA_MM_SOLVER_H

// STL
#include <string>  // string
#include <vector>  // vector
#include <map>     // map
#include <utility> // pair

// Utils
#include <utilities/debugUtils.h>

// Maya
#include <maya/MPoint.h>
#include <maya/MStringArray.h>
#include <maya/MAnimCurveChange.h>
#include <maya/MDGModifier.h>
#include <maya/MComputation.h>

// MM Solver
#include <Camera.h>
#include <Marker.h>
#include <Bundle.h>
#include <Attr.h>

// The different solver types to choose from:

// Dense LM solver using 'levmar',
#define SOLVER_TYPE_LEVMAR 0
#define SOLVER_TYPE_LEVMAR_NAME "levmar"

// Dense LM solver using 'cminpack' library.
#define SOLVER_TYPE_CMINPACK_LM 1
#define SOLVER_TYPE_CMINPACK_LM_NAME "cminpack_lm"

// The default solver to use, if all solvers are available.
#define SOLVER_TYPE_DEFAULT_VALUE SOLVER_TYPE_CMINPACK_LM

// Enable the Maya profiling data collection.
#define MAYA_PROFILE 1

// The number of errors that are measured per-marker.  
//
// This can be a value of 2 or 3. 3 was used in the past with
// success, but tests now prove 2 to reduce error with less
// iterations, and is significantly faster overall.
#define ERRORS_PER_MARKER 2


#define CMD_RESULT_SPLIT_CHAR "#"


typedef std::vector<std::vector<bool> > BoolList2D;
typedef std::pair<int, int> IndexPair;
typedef std::vector<std::pair<int, int> > IndexPairList;
typedef std::pair<int, std::string> SolverTypePair;


inline
double distance_2d(MPoint a, MPoint b) {
    double dx = (a.x - b.x);
    double dy = (a.y - b.y);
    return sqrt((dx * dx) + (dy * dy));
}

std::vector<SolverTypePair> getSolverTypes();

SolverTypePair getSolverTypeDefault();

int countUpNumberOfErrors(MarkerPtrList markerList,
                          MTimeArray frameList,
                          MarkerPtrList &validMarkerList,
                          std::vector<MPoint> &markerPosList,
                          std::vector<double> &markerWeightList,
                          IndexPairList &errorToMarkerList,
                          MStatus &status);

int countUpNumberOfUnknownParameters(AttrPtrList attrList,
                                     MTimeArray frameList,
                                     AttrPtrList &camStaticAttrList,
                                     AttrPtrList &camAnimAttrList,
                                     AttrPtrList &staticAttrList,
                                     AttrPtrList &animAttrList,
                                     IndexPairList &paramToAttrList,
                                     MStatus &status);

void findErrorToUnknownRelationship(MarkerPtrList markerList,
                                    AttrPtrList attrList,
                                    MTimeArray frameList,
                                    int numParameters,
                                    int numErrors,
                                    IndexPairList paramToAttrList,
                                    IndexPairList errorToMarkerList,
                                    BoolList2D &markerToAttrMapping,
                                    BoolList2D &errorToParamMapping,
                                    MStatus &status);

bool solve(int iterMax,
           double tau,
           double eps1,
           double eps2,
           double eps3,
           double delta,
           int autoDiffType,
           int autoParamScale,
           int solverType,
           CameraPtrList cameraList,
           MarkerPtrList markerList,
           BundlePtrList bundleList,
           AttrPtrList attrList,
           MTimeArray frameList,
           MDGModifier &dgmod,
           MAnimCurveChange &curveChange,
           MComputation &computation,
           MString &debugFile,
           bool verbose,
           MStringArray &outResult);

#endif // MAYA_MM_SOLVER_H
