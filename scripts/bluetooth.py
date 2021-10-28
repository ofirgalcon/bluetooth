#!/usr/bin/python

import subprocess
import os
import plistlib
import sys
import re

def get_bluetooth_info():

    '''Uses system profiler to get memory info for this machine.'''
    cmd = ['/usr/sbin/system_profiler', 'SPBluetoothDataType', '-xml']
    proc = subprocess.Popen(cmd, shell=False, bufsize=-1,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (output, unused_error) = proc.communicate()
    try:
        plist = plistlib.readPlistFromString(output)
        # system_profiler xml is an array
        sp_dict = plist[0]
        items = sp_dict['_items'][0]
        return (items)
    except Exception:
        return {}

def flatten_bluetooth_info(obj):
    '''Un-nest bluetooth information, return array with objects with relevant keys'''
    out = []
    i = 0

    # Check if there is Bluetooth hardware
    try:
        # Check if we're running macOS 12+
        if 'controller_properties' in obj.keys() and 'devices_list' in obj.keys():
            obj_device = obj['devices_list']
        elif 'controller_properties' in obj.keys() and 'devices_list' not in obj.keys():
            obj_device = [{'blank_item':'blank_item'}]
        else:
            obj['device_title']
            obj_device = obj['device_title']
    except:
        try:
            obj['local_device_title']
            obj_device = [{'blank_item':'blank_item'}]
        except:
            return [{'power':-1}]


    for bt_device in obj_device:
        for item in bt_device:
            device = {}
            for item_att in bt_device[item]:

                # Set name of device
                if item is not 'blank_item':
                    device['device_name'] = item

                if i == 0:
                    # We only want the first Bluetooth device to have all the extra controller info
                    i = 1

                    # Apple changed Bluetooth reporting in macOS 12
                    if 'apple_bluetooth_version' in obj.keys():
                        device['apple_bluetooth_version'] = obj['apple_bluetooth_version']
                        obj_local = obj['local_device_title']
                    else:
                        obj_local = obj['controller_properties']

                    for item_local in obj_local:
                        if item_local == 'general_address' or item_local == 'controller_address':
                            print(obj_local[item_local])
                            if obj_local[item_local] != 'NULL':
                                device['machine_address'] = obj_local[item_local]
                        elif item_local == 'general_autoseek_keyboard' or item_local == 'controller_autoSeekKeyboard':
                            device['autoseek_keyboard'] = to_bool(obj_local[item_local])
                        elif item_local == 'general_autoseek_pointing' or item_local == 'controller_autoSeekPointing':
                            device['autoseek_pointing'] = to_bool(obj_local[item_local])
                        elif item_local == 'general_connectable' or item_local == 'controller_connectable':
                            device['connectable'] = to_bool(obj_local[item_local])
                        elif item_local == 'general_discoverable' or item_local == 'device_discoverable' or item_local == 'controller_discoverable':
                            device['discoverable'] = to_bool(obj_local[item_local])
                        elif item_local == 'general_hardware_transport' or item_local == 'controller_transport':
                            device['hardware_transport'] = obj_local[item_local]
                        elif item_local == 'general_name':
                            device['machine_name'] = obj_local[item_local]

                        elif item_local == 'general_power' or item_local == 'device_power' or item_local == 'controller_state':
                            device['power'] = to_bool(obj_local[item_local])

                        elif item_local == 'general_remoteWake' or item_local == 'controller_remoteWake':
                            device['remotewake'] = to_bool(obj_local[item_local])
                        elif item_local == 'general_supports_handoff' or item_local == 'controller_supportHandoff':
                            device['supports_handoff'] = to_bool(obj_local[item_local])
                        elif item_local == 'general_supports_instantHotspot' or item_local == 'controller_supportInstHotSpot':
                            device['supports_instanthotspot'] = to_bool(obj_local[item_local])
                        elif item_local == 'general_supports_airDrop':
                            device['supports_airdrop'] = to_bool(obj_local[item_local])
                        elif item_local == 'general_supports_lowEnergy' or item_local == 'controller_supportLE':
                            device['supports_lowenergy'] = to_bool(obj_local[item_local])

                        elif item_local == 'general_vendorID' or item_local == 'controller_vendorID':
                            device['vendor_id'] = obj_local[item_local]


                if item_att == 'device_addr' or item_att == 'device_address':
                    device['device_address'] = bt_device[item][item_att]
                elif item_att == 'device_RSSI' or item_att == 'device_rssi':
                    device['rssi'] = bt_device[item][item_att]
                elif item_att == 'device_batteryPercent' or item_att == 'device_batteryLevelMain':
                    device['batterypercent'] = re.sub('[^0-9-]','',bt_device[item][item_att])

                elif item_att == 'device_isNormallyConnectable':
                    device['isnormallyconnectable'] = to_bool(bt_device[item][item_att])
                elif item_att == 'device_isconfigured' or item_att == 'device_configured':
                    device['isconfigured'] = to_bool(bt_device[item][item_att])
                elif item_att == 'device_isconnected' or item_att == 'device_connected':
                    device['isconnected'] = to_bool(bt_device[item][item_att])
                elif item_att == 'device_ispaired' or item_att == 'device_paired':
                    device['ispaired'] = to_bool(bt_device[item][item_att])

                elif item_att == 'device_manufacturer':
                    device['manufacturer'] = bt_device[item][item_att]
                elif item_att == 'device_majorClassOfDevice_string' or item_att == 'device_majorType':
                    device['majorclass'] = bt_device[item][item_att]
                elif item_att == 'device_minorClassOfDevice_string' or item_att == 'device_minorType':
                    device['minorclass'] = bt_device[item][item_att]
                elif item_att == 'device_services' and " < " in bt_device[item][item_att]:
                    device['services'] = bt_device[item][item_att].split(" < ")[1].split(" >")[0]
                elif item_att == 'device_services' and " < " not in bt_device[item][item_att]:
                    device['services'] = bt_device[item][item_att]

            out.append(device)
    return out

def to_bool(s):
    if s == "attrib_Yes" or s == "attrib_On" or s == "attrib_on"  or s == "attrib_yes" or s == "Yes":
        return 1
    else:
        return 0

def main():
    """Main"""

    # Set the encoding
    # The "ugly hack" :P 
    reload(sys)  
    sys.setdefaultencoding('utf8')

    # Get results
    result = dict()
    result = flatten_bluetooth_info(get_bluetooth_info())

    # Write memory results to cache
    cachedir = '%s/cache' % os.path.dirname(os.path.realpath(__file__))
    output_plist = os.path.join(cachedir, 'bluetoothinfo.plist')
    plistlib.writePlist(result, output_plist)
    # print plistlib.writePlistToString(result)

if __name__ == "__main__":
    main()
