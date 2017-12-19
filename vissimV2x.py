#coding=utf-8
import v2xConfig
import httpV2x
import win32com.client
import win32api
import win32con
import os
import threading


def setSys():
    win32api.SetSystemTime(2008, 12, 0, 8, 8, 8, 8, 0)  # 修改系统时间
    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, 'SOFTWARE\\Microsoft', 0, win32con.KEY_ALL_ACCESS)
    win32api.RegDeleteKey(key, 'MS Control')
    win32api.RegCreateKey(key, 'MS Control')


if __name__ == '__main__':
    fileName = v2xConfig.fileName
    period = v2xConfig.period
    resolution = v2xConfig.resolution
    setSys()
    vissim_com = win32com.client.Dispatch("VISSIM.vissim.430")
    vissim_com.LoadNet(os.getcwd()+("\\%s.inp" % fileName))
    simulation = vissim_com.simulation
    simulation.Period = period
    simulation.Resolution = resolution
    # gr = vissim_com.Graphics
    # gr.SetWindow('NETWORK',0,0,149,375,3) #窗口大小顶，左，底，右
    # gr.SetAttValue("DISPLAY",3)     #隐藏车辆
    # simulation.BreakAt = period    #仿真断点
    # simulation.SetAttValue("SPEED", -1)  # 最大仿真速度
    # eval = vissim_com.Evaluation
    # eval.SetAttValue("TRAVELTIME", True) #激活旅行时间评价
    light = v2xConfig.light
    lightV2x = v2xConfig.lightV2x
    Vehicles = vissim_com.Net.Vehicles
    for t in range(period*resolution):
        veV2x = {veV2xKey:[] for veV2xKey in lightV2x}
        simulation.RunSingleStep()
        for veNo in range(Vehicles.Count):
            t = threading.Thread(target=httpV2x.veGet, args=())
            t.setDaemon(True)
            t.start()
            if Vehicles(veNo):
                vehicle = Vehicles(veNo)
                vehicle.SetAttValue("INTERACTION", 1)
                vehicle.SetAttValue("DESIREDSPEED", 40)
                for veV2xKey,veV2xVal in veV2x.items():         #获取通信车
                    if vehicle.AttValue("LINK") == int(veV2xKey):
                        veV2xVal.append(vehicle)
        state = None
        state = httpV2x.getState()
        #print state
        if veV2x and state:
            for veV2xKey, veV2xVal in veV2x.items():
                for vehicle in veV2xVal:
                    if state['light'][light.index(lightV2x[veV2xKey])] == 2: #判断是否红灯
                        vehicle.SetAttValue("INTERACTION", 0)         #不关闭车还会缓慢移动
                        vehicle.SetAttValue("SPEED", 0)
	
    simulation.Stop
