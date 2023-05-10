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

import os
import math
from anybase import assertion, convert
from pathlib import Path

from catharsys.config.cls_project import CProjectConfig
import catharsys.util.config as cathcfg
import catharsys.util.file as cathfile
import catharsys.util.path as cathpath
from catharsys.plugins.std.blender.util.action import GetRenderFolder
from catharsys.action.util import GetParentConfigTargetPath


os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"
import cv2


class CExample:
    """This actions example loads images rendered in a previous step and saves them
    again as jpgs.
    """

    # The project configuration
    xPrjCfg: CProjectConfig = None
    dicConfig: dict = None
    dicData: dict = None

    # Define expected config types.
    # These DTIs can be chosen arbitrarily, but they should start with
    # '/catharsys/' and you have to ensure that there are no name conflicts.

    # This config is just a string value, giving the render output to be used.
    # This is typically 'Image' but depends on the compositor settings of the render.
    # Since there can be multiple outputs from a single render, this needs to
    # be specified explicitly.
    sImgTypeDti: str = "/catharsys/_ext_/example/input-id:1"

    # This config will be a json file with additional settings for this action.
    sExampleDti: str = "/catharsys/_ext_/example/data:1"

    sPathTrgMain: str = None
    pathSrcMain: Path = None
    dicPathTrgAct: dict = None
    dicActDtiToName: dict = None
    lActions: list = None
    iFrameFirst: int = None
    iFrameLast: int = None
    iFrameStep: int = None
    bDoProcess: bool = None
    bDoOverwrite: bool = None
    iDoProcess: int = None
    iDoOverwrite: int = None

    ################################################################################
    def __init__(self):
        pass

    # enddef

    ################################################################################
    def Process(self, _xPrjCfg: CProjectConfig, _dicCfg: dict, **kwargs):
        assertion.FuncArgTypes()

        print("\n==============================")
        print("Start Processing Example Action\n")

        sWhere: str = "example action configuration"
        self.xPrjCfg = _xPrjCfg

        ##################################################################################
        # Get the current configuration
        self.dicConfig = cathcfg.GetDictValue(_dicCfg, "mConfig", dict, sWhere=sWhere)
        self.dicData = cathcfg.GetDictValue(self.dicConfig, "mData", dict, sWhere=sWhere)

        ##################################################################################
        # Load set of parameters from given configuration into this class
        cathcfg.StoreDictValuesInObject(
            self,
            _dicCfg,
            [
                ("sPathTrgMain", str),
                ("dicPathTrgAct", dict),
                ("dicActDtiToName", dict),
                ("lActions", list),
                ("iFrameFirst", int, 0),
                ("iFrameLast", int, 0),
                ("iFrameStep", int, 1),
                ("iDoProcess", int, 1),
                ("bDoProcess", bool, True),
                ("iDoOverwrite", int, 1),
                ("bDoOverwrite", bool, True),
            ],
            sWhere="action configuration",
        )

        ##################################################################################
        # Can use these flags to enable/disable processing and image overwrite
        self.bDoProcess = self.bDoProcess and (self.iDoProcess != 0)
        self.bDoOverwrite = self.bDoOverwrite and (self.iDoOverwrite != 0)

        ##################################################################################
        # Extract the example configuration data from the whole config.
        lExampleData = cathcfg.GetDataBlocksOfType(self.dicData, self.sExampleDti)
        if len(lExampleData) == 0:
            raise Exception("No example configuration of type compatible to '{0}' given.".format(self.sExampleDti))
        # endif

        # Here we expect that there is only a single instance of the configuration data.
        # However, in principle there could be any number of configurations of the same type
        # included in the combined job configuration.
        dicExample: dict = lExampleData[0]

        ##################################################################################
        # Obtain main source path from the parent action.
        self.pathSrcMain = GetParentConfigTargetPath(_dicCfg)

        # Get the image render source path from the current configuration settings
        dicImgFolder, sImageType = GetRenderFolder(self.xPrjCfg, _dicCfg, self.sImgTypeDti)
        sFolderImgSrc = dicImgFolder.get("sFolder")
        sFileExtImgSrc = dicImgFolder.get("sFileExt")
        pathImageSrc: Path = self.pathSrcMain / sFolderImgSrc

        if not pathImageSrc.exists():
            raise RuntimeError(
                f"Source image path for image type '{sImageType}' does not exist: {(pathImageSrc.as_posix())}"
            )
        # endif

        ##################################################################################
        # Create target path for this action
        # NOTE: You can use the automatically generated target path from self.sPathTrgMain,
        #       or you can define your own target path, as is shown here.
        #       However, if you define your own path, any action that depends on this one
        #       cannot use the automatic path generation to find the output images.
        pathImageTrg: Path = self.pathSrcMain / "pyact" / sImageType
        pathImageTrg.mkdir(parents=True, exist_ok=True)

        ##################################################################################
        # Print current config values
        print(f"Main project path: {(_xPrjCfg.pathMain.as_posix())}")
        print(f"Image source path: {(pathImageSrc.relative_to(_xPrjCfg.pathMain).as_posix())}")
        print(f"Generated main path: {(Path(self.sPathTrgMain).relative_to(_xPrjCfg.pathMain).as_posix())}")
        print(
            f"Custom target path for image type '{sImageType}': {(pathImageTrg.relative_to(_xPrjCfg.pathMain).as_posix())}"
        )

        # Use the conversion functions from the module anybase.convert to read values
        # from dictionaries. They automatically convert the dictionary value types
        # to the expected output type and do proper error reporting.
        iExValue: int = convert.DictElementToInt(dicExample, "iValue", iDefault=0)
        print(f"Value from example config: {iExValue}")

        ##################################################################################
        # Loop over all frames
        print("")

        iTrgFrame: int = self.iFrameFirst
        iTrgFrameIdx: int = 0
        iTrgFrameCnt: int = int(math.floor((self.iFrameLast - self.iFrameFirst) / self.iFrameStep)) + 1
        print(f"Processing {iTrgFrameCnt} frame(s).")

        while iTrgFrame <= self.iFrameLast:
            print(f"\nStart processing frame {iTrgFrame}...", flush=True)

            # Create name of file for current frame
            sFrameName: str = "Frame_{0:04d}".format(iTrgFrame)
            sFileImgSrc: str = f"{sFrameName}{sFileExtImgSrc}"

            pathImgSrcFile: Path = pathImageSrc / sFileImgSrc
            if not pathImgSrcFile.exists():
                print(f"Frame '{sFileImgSrc}' does not exist. Skipping...")

            else:
                # The imread options are needed for loading OpenEXR files with floating point values.
                imgSrcImg = cv2.imread(
                    pathImgSrcFile.as_posix(), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH | cv2.IMREAD_UNCHANGED
                )

                sFileImgTrg: str = f"{sFrameName}.jpg"
                pathImgTrgFile: Path = pathImageTrg / sFileImgTrg
                if self.bDoOverwrite is False and pathImgTrgFile.exists():
                    print(f"Skipping image file as it already exists: {(pathImgTrgFile.as_posix())}")

                else:
                    print(f"Writing image to: {(pathImgTrgFile.as_posix())}")

                    if self.bDoProcess:
                        # TODO: Do your own processing of the source image

                        cv2.imwrite(pathImgTrgFile.as_posix(), imgSrcImg)
                    # endif
                # endif
            # endif

            iTrgFrame += self.iFrameStep
            iTrgFrameIdx += 1
        # endwhile

    # enddef Process()


# endclass
