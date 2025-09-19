import logging, logging.handlers
from simconnect_mobiflight import SimConnectMobiFlight
from mobiflight_variable_requests import MobiFlightVariableRequests
from time import sleep
import sys

def setupLogging(logFileName):
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.DEBUG)
    fileHandler = logging.handlers.RotatingFileHandler(logFileName, maxBytes=2000000, backupCount=7)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

# MAIN
setupLogging("SimConnectMobiFlight.log")
sm = SimConnectMobiFlight()
vr = MobiFlightVariableRequests(sm)
vr.clear_sim_variables()

# Example write variable
vr.set("(L:S_OH_ELEC_EXT_PWR) ++ (>L:S_OH_ELEC_EXT_PWR)")

vr.ping()
vr.get_version()

try:
    with open("lvars.txt") as file:
        lines = [line.rstrip() for line in file]
    vr.set_lvars_list(lines)
except FileNotFoundError:
    logging.info("cannot find file")    
vr.list_sim_variables()
wait_counter = 0
while wait_counter < 50: # wait max 500ms
    if not vr.lvars_list_end: # wait max 500ms
        sleep(0.01) # wait 10ms
        wait_counter = wait_counter + 1
    else:
        break 
    
fout = open("lvars.txt", "w")
unique_list = list(set(vr.lvars_list))
unique_list.sort()
for lvar in unique_list:
    fout.write(lvar+"\n")

while True:
    #alt_ground = vr.get("(A:GROUND ALTITUDE,Meters)")
    #alt_plane = vr.get("(A:PLANE ALTITUDE,Feet)")
    # FlyByWire A320
    ap1 = vr.get("(L:S_OH_ELEC_EXT_PWR)")
    #hdg = vr.get("(L:A32NX_AUTOPILOT_HEADING_SELECTED)")
    #mode = vr.get("(L:A32NX_FMA_LATERAL_MODE)")
    #continue
    if vr.lvars_list_end:
        for rpn in vr.lvars_list:
            rpnstr = "(L:" + rpn + ")"
            logging.info("%s", rpnstr)
            t = vr.get(rpnstr)
    sleep(1)