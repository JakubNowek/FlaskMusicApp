import os
processing_folder = 'static/files/'


def func(function, *argv):
    function(argv[0], argv[1])


def low_pass(filename, data):
    print('low pass')
    file = open(processing_folder + filename, 'a')
    file.write('low pass\n')
    file.close()


def high_pass(filename, data):
    print('high pass')
    file = open(processing_folder + filename, 'a')
    file.write('high pass\n')
    file.close()


def cut(filename, data):
    print('cut')
    file = open(processing_folder + filename, 'a')
    file.write('cut\n')
    file.close()


def echo(filename, data):
    print('echo')
    delay=data['delay']
    decay=data['decay']
    file = open(processing_folder + filename, 'a')
    file.write(f'echo {delay}, {decay}\n')
    file.close()


def amp(filename, data):
    print('amplification')
    amplitude = data
    file = open(processing_folder + filename, 'a')
    file.write(f'amp {amplitude} \n')
    file.close()
