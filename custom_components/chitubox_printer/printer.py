import socket
import os
from queue import Queue

class Printer:
    def __init__(self, ip) -> None:
        self.ip = ip
        self.port = 3000
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        self.sock.settimeout(20)
        self.buffSize = 4096
        self.jobs = Queue()
        
    def __sendRecieveSingle__(self, code, buffSize=-1) -> str:
        self.sock.sendto(bytes(code, "utf-8"), (self.ip, self.port))
        if buffSize == -1:
            buffSize = self.buffSize
        output = self.sock.recv(buffSize)
        return output

    def __sendRecieveSingleNice__(self, code, buffSize=-1) -> str:
        if buffSize == -1:
            buffSize = self.buffSize
        output = self.__stripFormatting__(self.__sendRecieveSingle__(code, buffSize))
        return output

    def __getUniversal__(self, split) -> str:
        output = str(self.__sendRecieveSingle__("M99999")).split(" ")[split].split(":")[1]
        return output if output else "No Response"

    def getVer(self) -> str:
        """Returns the printer's version."""
        return self.__getUniversal__(3)
        
    def getID(self) -> str:
        """Returns Printer's UID."""
        return self.__getUniversal__(4)

    def getName(self) -> str:
        """Gets the printer's Name."""
        return self.__getUniversal__(5).split("\\")[0]

    def __stripFormatting__(self, string) -> str:
        string = (string.decode("utf-8"))
        string = string.rstrip()
        return string

    def __stripSpaceFromBack__(self, string) -> str:
        bIndex = max([i for i, ltr in enumerate(string) if ltr == "b"])
        return (string[:bIndex+1], string[bIndex+2:])

    def getCardFiles(self) -> list:
        """Returns the list of CTB files on the storage."""
        self.sock.sendto(bytes("M20", "utf-8"), (self.ip, self.port))
        output = []
        request = self.__stripFormatting__(self.sock.recv(self.buffSize))

        while request != "End file list":
            if ".ctb" in request:
                if request != "Begin file list" and self.__stripSpaceFromBack__(request)[1] != 0:
                    output.append(self.__stripSpaceFromBack__(request))

            request = self.__stripFormatting__(self.sock.recv(self.buffSize))
            
        return output
    
    def homeAxis(self) -> None:
        """Homes Z axis."""
        self.__sendRecieveSingle__("G28 Z")

    def getAxis(self) -> float:
        """Gets current Axis position."""
        pos = float(str(self.__sendRecieveSingle__("M114")).split(" ")[4].strip("Z:"))
        return pos

    def jogHard(self, distance) -> None:
        """Jogs without checking machine soft limits (not recommended)."""
        self.__sendRecieveSingle__("G0 Z" + str(distance))

    def jogSoft(self, distance) -> str:
        """Jogs after checking machine soft limits."""
        if distance < 200 or distance < 1:
            self.jogHard(distance)
            return "Complete"
        else:
            return "Distance too great or other error"

    def removeCardFile(self, filename) -> str:
        """Removes specified file from storage."""
        return str(self.__sendRecieveSingleNice__("M30 " + filename))

    def startPrinting(self, filename) -> str:
        """Starts printing from storage."""
        return self.__sendRecieveSingleNice__(f"M6030 '{filename}'")
    
    def printingStatus(self) -> str:
        """Returns if the machine is printing."""
        string = self.__sendRecieveSingleNice__("M27")
        if string == "Error:It's not printing now!":
            return "Not Printing"
        elif string.split()[0] == "SD":
            return "Printing"
        else:
            return "Not Printing"

    def printingPercent(self) -> list:
        """Returns the percentage of the print in bytes complete."""
        string = self.__sendRecieveSingleNice__("M27")
        return string.split()[3].split("/")

    def stopPrinting(self) -> str:
        """Stops current print."""
        return self.__sendRecieveSingleNice__("M33")

    def uploadFile(self, fileNameLocal, fileNameCard="") -> str:
        """Uploads file to storage."""
        if fileNameCard == "":
            fileNameCard = fileNameLocal
        
        m28 = self.__sendRecieveSingleNice__(f"M28 {fileNameCard}")
        if m28 != "ok N:0":
            return f"M28 Error: {m28}"
        
        l = os.stat(fileNameLocal).st_size
        f = open(fileNameLocal, 'rb')
        remain = l
        offs = 0
        print('Length:', l)

        while remain > 0:
            dd = f.read(1280)
            remain = remain - len(dd)
            dc = bytearray(offs.to_bytes(length=4, byteorder='little'))
            cxor = 0
            for c in dd:
                cxor = cxor ^ c
            for c in dc:
                cxor = cxor ^ c
            dc.append(cxor)
            dc.append(0x83)
            self.sock.sendto(dd + dc, (self.ip, self.port))
            s = self.sock.recv(self.buffSize)
            print(remaining, end='   \r')
        
        m4012 = self.__sendRecieveSingleNice__(f"M4012 I1 T{l}")
        if m4012.split()[0] != "ok":
            return f"Size Verify Error: {m4012}"

        return self.__sendRecieveSingleNice__("M29")

    def formatCard(self):
        """Formats storage."""
        for file in self.getCardFiles():
            self.removeCardFile(file[0])

    def close(self):
        """Close the printer connection."""
        self.sock.close()
