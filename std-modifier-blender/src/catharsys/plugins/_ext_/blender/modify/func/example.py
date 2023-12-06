#!/usr/bin/env python3
# -*- coding:utf-8 -*-
###
# File: \action-python\src\catharsys\plugins\_ext_\python\actions\lib\cls_example.py
# Created Date: Friday, November 25th 2022, 9:50:55 am
# Author: Christian Perwass (CR/AEC5)
# <LICENSE id="Apache-2.0">
#
#   Image-Render Standard Actions module
#   Copyright 2022 Robert Bosch GmbH and its subsidiaries
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# </LICENSE>
###


import bpy
import mathutils

# import math
# from anyblend import ops_object as anyops
from anyblend import viewlayer as anyvl
from anybase import convert


############################################################################################
def _Metric2BlenderScale(_sUnit: str):
    dMeterPerUnit = 1.0
    if _sUnit == "m":
        dMeterPerUnit = 1.0
    elif _sUnit == "mm":
        dMeterPerUnit = 1e-3
    elif _sUnit == "um":
        dMeterPerUnit = 1e-6
    elif _sUnit == "km":
        dMeterPerUnit = 1e3
    else:
        raise Exception("Unkown unit '{0}'.".format(_sUnit))
    # endif

    dScale = dMeterPerUnit / bpy.context.scene.unit_settings.scale_length
    return dScale


# enddef


############################################################################################
# This is the actual modifier code that is called.
#
# _objX: the Blender object instance, this modifier is applied to
# _dicMod: the configuration dictionary for this modifier
#          For your own modifier, the dictionary '_dicMod' can contain anything you like.


def Example(_objX, _dicMod, **kwargs):
    sUnit: str = convert.DictElementToString(_dicMod, "sUnit", "m")
    lPos: list[float] = convert.DictElementToFloatList(_dicMod, "lPosition", iLen=3)

    dScale = _Metric2BlenderScale(sUnit)

    # Convert to Blender units
    lPos_bu = [dScale * x for x in lPos]

    # Set object location
    _objX.location = mathutils.Vector(lPos_bu)

    # Update the view layer, so that the object's world matrix is updated.
    # This is important if modifiers following this one, rely on the
    # object's location.
    anyvl.Update()

    return None


# enddef
