'''
spektrum.py - Support for Spketrum R/C transmitters.

    Copyright (C) 2014 Simon D. Levy

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as 
    published by the Free Software Foundation, either version 3 of the 
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

'''

from quadstick.rc import RC

class DX8(RC):
    '''
    Class for Spektrum DX8 transmitter used with Wailly PPM->USB cable.
    '''

    def __init__(self, jsid=0, hidden=False, sound=False):
        '''
        Creates a new DX8 object.
        '''
        RC.__init__(self, 'Spektrum', jsid, hidden, sound)

        # Default to Linux 
        self.pitch_axis  = 2
        self.roll_axis   = 1
        self.yaw_axis    = 5
        self.throttle_axis  = 0
        self.switch_axis = 3

        if self.platform == 'Windows':
            self.yaw_axis    = 3
            self.switch_axis = 5

        elif self.platform == 'Darwin':
            self.pitch_axis  = 0
            self.roll_axis   = 3
            self.yaw_axis    = 1
            self.throttle_axis  = 2
            self.switch_axis = 4

        self.pitch_sign = -1
        self.roll_sign  = +1
        self.yaw_sign   = -1

    def poll(self):
        '''
        Polls the Spektrum R/C transmitter.

        Controls are Mode 2 (Left stick throttle / yaw; Right stick pitch / roll).

        Flap/Gyro switch controls altitude-hold / position-hold -- takeoff with it down, then:

            Down   : No hold
            Middle : Altitude hold
            Up     : Altitude & position hold

        AUX 3 dial controls autopilot: takeoff at extreme clockwise, then turn to 12:00 for autopilot.

        Returns demands (pitch, roll, yaw, throttle) and switches (pos-hold, alt-hold, autopilot).
        '''

        return RC._poll(self)

    def _convert_axis(self, index, value):

        return value / (.66 if value < 0 else 0.67)
 
    def _get_alt_hold_request(self):

        return RC._get_axis(self, self.switch_axis) <= 0

    def _get_pos_hold_request(self):
     
        return RC._get_axis(self, self.switch_axis) < 0

    def _get_autopilot(self):

        # This is actually the AUX 3 dial: must be in 12:00 position for autopilot
        return (RC._get_button(self, 10) and not RC._get_button(self, 11))