from datetime import datetime
from fastapi import FastAPI
from typing import Dict
import uvicorn

app = FastAPI()


# ---------------------------------------

class Device:
    __macaddr: str = ""
    __count: int = 0
    __lastSeen: datetime = datetime.now()

    def __init__(self, macaddr: str = "", seencount: int = 0):
        self.__macaddr = macaddr
        self.__count = seencount
        self.__lastSeen = datetime.now()

    @property
    def mac_address(self) -> str:
        return self.__macaddr

    @property
    def count(self) -> int:
        return self.__count

    @property
    def last_seen(self) -> datetime:
        return self.__lastSeen

    @property
    def to_string(self) -> str:
        return f'MAC: {self.__macaddr}  Count: {self.__count}  LastSeen: {self.__lastSeen}'

    @property
    def to_log_format(self) -> str:
        return f'{self.__macaddr},{self.__lastSeen}'

    def mark_as_seen(self):
        self.__count += 1
        self.__lastSeen = datetime.now()
        return self

    def __str__(self):
        return self.to_string


DevDict = Dict[str, Device]

_reportCount: int = 0
_deviceList: DevDict = {}


# ---------------------------------------


def return_device_list() -> Dict[str, DevDict]:
    return {"devicelist": _deviceList}


# Getters
@app.get("/devicelist")
def devicelist() -> Dict[str, DevDict]:
    return return_device_list()


@app.get("/devicecount")
def device_count() -> Dict[str, int]:
    return {"devicecount": len(_deviceList)}


@app.get("/reportcount")
def report_count() -> Dict[str, int]:
    return {"reportcount": _reportCount}


# Setters


# Methods
@app.get("/log/{macaddr}")
def log_device(macaddr: str) -> Dict:
    global _reportCount
    _reportCount += 1

    f = open("devicelog.txt", "a")
    # Create a new object for updating the Dictionary
    if _deviceList.get(macaddr):
        new_device: Device = _deviceList[macaddr]
    else:
        new_device: Device = Device(macaddr)
    print(new_device.mark_as_seen())

    _deviceList[macaddr] = new_device

    f.write(new_device.to_log_format + '\n')
    f.close()

    return {"device_logged": macaddr, "newCount": new_device.count}


@app.get("/")
def root():
    return return_device_list()


# -------------------------------


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, log_level="info")
