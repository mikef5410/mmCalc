#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#

# Copyright 2018 Michael R. Ferrara

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import sys
import math
import wx
from wx import xrc
import pprint


MITlicenseText="""Copyright 2018 Michael R. Ferrara

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

class mmCalc(wx.App):
    zref = 50.0
    
    def OnInit(self):
        self.res = xrc.XmlResource('mmCalc_gui.xrc')
        self.gam1=0.0000001
        self.gam2=0.0000001
        self.init_frame()
        self.updateValues(1)
        self.updateValues(2)
        return True

    def init_frame(self):
        self.frame = self.res.LoadFrame(None, 'MismatchCalcApp')
        #self.res.InitAllHandlers()  #<--doesn't work, sigh
        self.frame.Bind(wx.EVT_TEXT_ENTER, self.vswr1Entered, id=xrc.XRCID('vswr1Text'))
        self.frame.Bind(wx.EVT_TEXT_ENTER, self.vswr2Entered, id=xrc.XRCID('vswr2Text'))
        self.frame.Bind(wx.EVT_TEXT_ENTER, self.rl1Entered, id=xrc.XRCID('rl1Text'))
        self.frame.Bind(wx.EVT_TEXT_ENTER, self.rl2Entered, id=xrc.XRCID('rl2Text'))
        self.frame.Bind(wx.EVT_TEXT_ENTER, self.Z1Entered, id=xrc.XRCID('Z1Text'))
        self.frame.Bind(wx.EVT_TEXT_ENTER, self.Z2Entered, id=xrc.XRCID('Z2Text'))
        self.frame.Bind(wx.EVT_TEXT_ENTER, self.Z0Entered, id=xrc.XRCID('Z0Text'))
        self.frame.Bind(wx.EVT_MENU, self.doQuit, id=xrc.XRCID('FileQuit'))
        self.frame.Bind(wx.EVT_MENU, self.doAbout, id=xrc.XRCID('HelpAbout'))
        self.frame.Show()
        return

    def doQuit(self, event):  # wxGlade: MyFrame.<event_handler>
        sys.exit(0)

    def doAbout(self, event):  # wxGlade: MyFrame.<event_handler>
        print "Hello"
        self.about = wx.MessageDialog(self.frame,"Mismatch Error Limits Calculator\n"+MITlicenseText,"About mmCalc",(wx.OK|wx.CENTRE))
        self.about.ShowModal()

    def vswr1Entered(self, event):  # wxGlade: MyFrame.<event_handler>
        self.vswr1=math.fabs(float(xrc.XRCCTRL(self.frame,'vswr1Text').GetValue()))
        self.gam1=self.vswr2gamma(self.vswr1)
        self.updateValues(1)
        

    def rl1Entered(self, event):  # wxGlade: MyFrame.<event_handler>
        self.rl1=float(xrc.XRCCTRL(self.frame,'rl1Text').GetValue())
        self.gam1=self.rl2gamma(self.rl1)
        self.updateValues(1)


    def Z1Entered(self, event):  # wxGlade: MyFrame.<event_handler>
        self.Z1=float(xrc.XRCCTRL(self.frame,'Z1Text').GetValue())
        self.gam1=self.z2gamma(self.Z1)
        self.updateValues(1)


    def vswr2Entered(self, event):  # wxGlade: MyFrame.<event_handler>
        self.vswr2=math.fabs(float(xrc.XRCCTRL(self.frame,'vswr2Text').GetValue()))
        self.gam2=self.vswr2gamma(self.vswr2)
        self.updateValues(2)

    def rl2Entered(self, event):  # wxGlade: MyFrame.<event_handler>
        self.rl2=float(xrc.XRCCTRL(self.frame,'rl2Text').GetValue())
        self.gam2=self.rl2gamma(self.rl2)
        self.updateValues(2)

    def Z2Entered(self, event):  # wxGlade: MyFrame.<event_handler>
        self.Z2=float(xrc.XRCCTRL(self.frame,'Z2Text').GetValue())
        self.gam2=self.z2gamma(self.Z2)
        self.updateValues(2)

    def Z0Entered(self, event):  # wxGlade: MyFrame.<event_handler>
        mmCalc.zref=float(xrc.XRCCTRL(self.frame,'Z0Text').GetValue())
        self.updateValues(1)
        self.updateValues(2)

        #print('Zo=%f' % (mmCalc.zref));
        
    def vswr2gamma(self, vswr):
        return((vswr-1.0)/(vswr+1.0))

    def gamma2vswr(self, gam):
        return(math.fabs(-1.0*(gam+1.0)/(gam-1.0)))
    
    def z2gamma(self, z):
        return((z-mmCalc.zref)/(z+mmCalc.zref))

    def gamma2z(self, gam):
        return(math.fabs(-1.0*mmCalc.zref*((gam+1.0)/(gam-1.0))))
    
    
    def gamma2rl(self, gamma):
        return(20*math.log10(gamma))

    def rl2gamma(self, rl):
        return(math.pow(10.0,(rl/20.0)))

    def updateElimits(self):
        self.amplLimP=20.0*math.log10(1.0+math.fabs(self.gam1*self.gam2))
        self.amplLimN=20.0*math.log10(1.0-math.fabs(self.gam1*self.gam2))
        self.phLim=math.degrees(math.asin(math.fabs(self.gam1*self.gam2)))

        xrc.XRCCTRL(self.frame,'mmAmplText').SetValue("%5.3f, +%5.3f dB" % (self.amplLimN,self.amplLimP))
        xrc.XRCCTRL(self.frame,'mmPhaseText').SetValue("+/- %4.1f°" % self.phLim)
        return
    
    def updateValues(self, row):
        if (row == 1):
            self.vswr1=self.gamma2vswr(self.gam1)
            xrc.XRCCTRL(self.frame,'vswr1Text').SetValue("%4.3f" % self.vswr1)

            self.rl1=self.gamma2rl(self.gam1)
            xrc.XRCCTRL(self.frame,'rl1Text').SetValue("%4.2f" % self.rl1)

            self.Z1 = self.gamma2z(self.gam1)
            xrc.XRCCTRL(self.frame,'Z1Text').SetValue("%4.1f" % self.Z1)

        if (row == 2):
            self.vswr2=self.gamma2vswr(self.gam2)
            xrc.XRCCTRL(self.frame,'vswr2Text').SetValue("%4.3f" % self.vswr2)

            self.rl2=self.gamma2rl(self.gam2)
            xrc.XRCCTRL(self.frame,'rl2Text').SetValue("%4.2f" % self.rl2)

            self.Z2 = self.gamma2z(self.gam2)
            xrc.XRCCTRL(self.frame,'Z2Text').SetValue("%4.1f" % self.Z2)

        self.updateElimits()
        return
    
# end of class mmCalc




if __name__ == '__main__':
    app = mmCalc(False)
    app.MainLoop()
