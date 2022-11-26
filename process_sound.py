import os


def func(function, *argv):
    function(argv[0])


def low_pass(filename):
    print('low pass')
    file = open(f'static/files/{filename}', 'a')
    file.write('low pass\n')
    file.close()


def high_pass(filename):
    print('high pass')
    file = open(f'static/files/{filename}', 'a')
    file.write('high pass\n')
    file.close()


def cut(filename):
    print('cut')
    file = open(f'static/files/{filename}', 'a')
    file.write('cut\n')
    file.close()


def echo(filename):
    print('echo')


def amp(filename):
    print('amplification')

