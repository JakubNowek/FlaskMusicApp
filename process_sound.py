import os
processing_folder = 'static/files/'


def func(function, *argv):
    function(argv[0], argv[1])


def low_pass(filename, data):
    print('low pass')
    file = open(processing_folder + filename, 'a')
    # funkcja coś robi
    file.write('low pass\n')
    # koniec akcji funkcji - zamykam plik #
    file.close()


def high_pass(filename, data):
    print('high pass')
    file = open(processing_folder + filename, 'a')
    # funkcja coś robi
    file.write('high pass\n')
    # koniec akcji funkcji - zamykam plik #
    file.close()


def cut(filename, data):
    print('cut')
    file = open(processing_folder + filename, 'a')
    # funkcja coś robi
    file.write('cut\n')
    # koniec akcji funkcji - zamykam plik #
    file.close()


def echo(filename, data):
    print('echo')
    delay=data['delay']
    decay=data['decay']
    file = open(processing_folder + filename, 'a')
    # funkcja coś robi
    file.write(f'echo {delay}, {decay}\n')
    # koniec akcji funkcji - zamykam plik #
    file.close()


# noinspection GrazieInspection
def amp(filename, data):
    print('amplification')
    amplitude = data
    file = open(processing_folder + filename, 'a')
    # funkcja coś robi
    file.write(f'amp {amplitude} \n')
    # koniec akcji funkcji - zamykam plik #
    file.close()
