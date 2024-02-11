# csum, cmd8500, printbuf functions copied verbatim from here:
# https://github.com/BKPrecisionCorp/BK-8500-Electronic-Load/tree/master/python

import serial

class bk8500():

    def __init__(self, com_port, debug=False):
        self.ser = serial.Serial()
        self.ser.baudrate = 19200
        self.ser.port = com_port #'COM12'
        self.ser.timeout = 1
        self.ser.open()
        self.debug = debug
        
    def csum(self, command):
        sum = 0
        for i in range(len(command)):
            sum += command[i]
        return 0xFF & sum

    def cmd8500(self, cmd):
        if (self.debug):
            print("Command: ", hex(cmd[2]))
            self.printbuff(cmd)
        self.ser.write(cmd)
        resp = self.ser.read(26)
        if (self.debug):
            # print("Resp: ")
            self.printbuff(resp)

    def printbuff(self, buff):
        r = ""
        for s in range(len(buff)):
            r += " "
            # r+=str(s)
            # r+="-"
            r += hex(buff[s]).replace('0x', '')
        print(r)

    def enable_remote(self):
        if (self.debug):
            print("Called enable_remote")
        cmd=[]
        cmd=[0]*26
        cmd[0]=0xAA
        cmd[2]=0x20
        cmd[3]=1
        cmd[25]=self.csum(cmd)
        self.cmd8500(cmd)

    def enable_input(self):
        if (self.debug):
            print("Called enable_input")
        cmd=[]
        cmd=[0]*26
        cmd[0]=0xAA
        cmd[2]=0x21
        cmd[3]=0x01
        cmd[25] = self.csum(cmd)
        self.cmd8500(cmd)

    def disable_input(self):
        if (self.debug):
            print("Called disable_input")
        cmd=[]
        cmd=[0]*26
        cmd[0]=0xAA
        cmd[2]=0x21
        cmd[3]=0x00
        cmd[25] = self.csum(cmd)
        self.cmd8500(cmd)

    def enable_cc_mode(self):
        if (self.debug):
            print("Called enable_cc_mode")
        cmd=[]
        cmd=[0]*26
        cmd[0]=0xAA
        cmd[2]=0x28 # set either CC, CV, CW or CR
        cmd[3]=0x00 # 0 is CC, 1 is CV, 2 is CW, 3 is CR
        cmd[25] = self.csum(cmd)
        self.cmd8500(cmd)

    def set_cc_mode_current(self,current): # current is in Amps
        int_val = int(current * 10000) + 1 # mult by 1000 for mA, then mult by 10 for 0.1mA steps
        list_of_bytes = list(int_val.to_bytes(4, byteorder='little'))
        if (self.debug):
            print("Called set_cc_mode_current")
        cmd=[]
        cmd=[0]*26
        cmd[0]=0xAA
        cmd[2]=0x2A
        cmd[3] = list_of_bytes[0]
        cmd[4] = list_of_bytes[1]
        cmd[5] = list_of_bytes[2]
        cmd[6] = list_of_bytes[3]
        cmd[25] = self.csum(cmd)
        self.cmd8500(cmd)
