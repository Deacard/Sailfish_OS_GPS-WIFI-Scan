#!/usr/bin/env python

import dbus
import subprocess
import gi.repository.GObject as gobject
import dbus.mainloop.glib as glib

glib.DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus() 

lastime = 0
count = 0
data = ''

def gpsprint(fields, timestamp, lat, lon, alt, acc):
    global lastime
    global count
    global data
    if timestamp > lastime:
        lastime = timestamp
        count += 1
        if count % 10 == 0:
            data_gps = '%d,%f,%f,' % (timestamp, lat, lon)

            output = subprocess.Popen(['wpa_cli', '-i', 'wlan0', 'scan'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            output = subprocess.Popen(['wpa_cli', '-i', 'wlan0', 'scan_results'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout, stderr = output.communicate()
            del(stderr)
            read_file = stdout.decode('utf8')

            a = read_file.replace('\t', ',')
            a = a + data_gps
            a = a.split('\n')[1:-1]

            for line in a:
                data = data + data_gps + str(line) + '\n'

            print(data)

bus.add_signal_receiver(gpsprint, 'PositionChanged', 'org.freedesktop.Geoclue.Position')

loop = gobject.MainLoop()
loop.run()


