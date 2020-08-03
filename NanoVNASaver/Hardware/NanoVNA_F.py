#  NanoVNASaver
#
#  A python program to view and export Touchstone data from a NanoVNA
#  Copyright (C) 2019, 2020  Rune B. Broberg
#  Copyright (C) 2020 NanoVNA-Saver Authors
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
import logging

import serial
import numpy as np
from PyQt5 import QtGui

from NanoVNASaver.Hardware.NanoVNA import NanoVNA

logger = logging.getLogger(__name__)


class NanoVNA_F(NanoVNA):
    name = "NanoVNA-F"
    screenwidth = 800
    screenheight = 480

    def getScreenshot(self) -> QtGui.QPixmap:
        logger.debug("Capturing screenshot...")
        if not self.connected():
            return QtGui.QPixmap()
        try:
            rgba_array = self._capture_data()
            unwrapped_array = np.empty(
                self.screenwidth*self.screenheight,
                dtype=np.uint32)
            for y in range(self.screenheight // 2):
                for x in range(self.screenwidth // 2):
                    unwrapped_array[
                        2 * x + 2 * y * self.screenwidth
                    ] = rgba_array[x + y * self.screenwidth]
                    unwrapped_array[
                        (2 * x) + 1 + 2 * y * self.screenwidth
                    ] = rgba_array[
                        x + (self.screenheight//2 + y) * self.screenwidth
                    ]
                    unwrapped_array[
                        2 * x + (2 * y + 1) * self.screenwidth
                    ] = rgba_array[
                        x + self.screenwidth // 2 + y * self.screenwidth
                    ]
                    unwrapped_array[
                        (2 * x) + 1 + (2 * y + 1) * self.screenwidth
                    ] = rgba_array[
                        x + self.screenwidth // 2 +
                        (self.screenheight//2 + y) * self.screenwidth
                    ]

            image = QtGui.QImage(
                unwrapped_array,
                self.screenwidth, self.screenheight,
                QtGui.QImage.Format_ARGB32)
            logger.debug("Captured screenshot")
            return QtGui.QPixmap(image)
        except serial.SerialException as exc:
            logger.exception("Exception while capturing screenshot: %s", exc)
        return QtGui.QPixmap()
