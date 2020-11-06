#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ce script convertit une trame NMEA de format décimal vers un format ASCII ( $,,,,) puis interprete les différents champs

import pynmea2
import sys
import json


def nmea_trad(nmea_frame):
    string = bytes.fromhex(nmea_frame).decode('utf-8')
    return string


def dissect(messages):
    dico = []
    for i in range(len(messages.data) - 1):
        dico.append((messages.fields[i][1], messages.data[i]))

    dico = dict(dico)
    return json.dumps(dico)


def dechiffre_hex():
    for arg in sys.argv[1:]:  # mettre un log de fichier hexa decimal

        print(arg)

        file = open(arg)
        dissect_file = open("/home/guillaume/PFE/DATA/wireshark/nmea.json", "w")
        nombre = 1

        for line in file.readlines():

            try:

                msg = pynmea2.parse(nmea_trad(line))
                dissect_file.write('{"id" : "')
                dissect_file.write(str(nombre))
                dissect_file.write('","data":')
                dissect_file.write(dissect(msg))
                dissect_file.write(',"sentence_id":"')
                dissect_file.write(nmea_trad(line)[:6])
                dissect_file.write('"}\n')
                nombre += 1

                print('{"data":', dissect(msg), ', "sentence_id":"', nmea_trad(line)[1:6],
                      '"}\n')  # affichage sur stdout pour traitement tps reel

            except pynmea2.ParseError as e:
                print('Parse error: {}'.format(e))
                continue

        dissect_file.close()


def dechiffre():
    for arg in sys.argv[1:]:  # mettre un log

        print(arg)

        file = open(arg)
        dissect_file = open(str(arg + ".json"), "w")
        nombre = 1

        for line in file.readlines():

            try:

                msg = pynmea2.parse(line)
                dissect_file.write('{"id" : "')
                dissect_file.write(str(nombre))
                dissect_file.write('","data":')
                dissect_file.write(dissect(msg))
                dissect_file.write(',"sentence_id":"')
                dissect_file.write(line[:6])
                dissect_file.write('"}\n')
                nombre += 1

                print(dissect(msg))  

            except pynmea2.ParseError as e:
                pass
                # print('Parse error: {}'.format(e))
                # continue

        dissect_file.close()


dechiffre()