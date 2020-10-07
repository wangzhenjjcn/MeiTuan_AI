#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# By Wangzhen@2016.05
# Last Version : 2020-07-04V6

import sys
import configparser
import codecs

class Config:
    def __init__(self, path):
        self.path = path
        self.removeBom(self.path)
        self.cf = configparser.ConfigParser()
        self.cf.read(self.path,encoding='utf-8-sig')

    def get(self, field, key):
        result = ''
        try:
            result = self.cf.get(field, key)
        except:
            result = ''
        return result

    def set(self, filed, key, value):
        try:
            self.cf.set(field, key, value)
            self.cf.write(open(self.path, 'w+',encoding='utf-8-sig'))
        except:
            return False
        return True

    def removeBom(self,file):
        BOM = b'\xef\xbb\xbf'
        existBom = lambda s: True if s==BOM else False
        f = open(file, 'rb')
        if existBom( f.read(3) ):
            fbody = f.read()
            # f.close()
            with open(file, 'wb') as f:
                f.write(fbody)
        f.close()



def read_config(config_file_path, field, key):
    cf = configparser.ConfigParser()
    try:
        remove_Bom(config_file_path)
        cf.read(config_file_path,encoding='utf-8-sig')
        if field in cf:
            result = cf[field][key]
        else:
            
            return ''
    except configparser.Error as e1:
        print("read_config err: =====1=====")
        print(e1)
        return ''
    except Exception as e2:
        print("read_config err: ======2====")
        print(e2)
        return ''
    return result



def read_config_init(config_file_path, field, key, defaultValueValue):
    cf = configparser.ConfigParser()
    try:
        remove_Bom(config_file_path)
        cf.read(config_file_path,encoding='utf-8-sig')
        if field in cf:
            result = cf[field][key]
            if result == "" or result == None:
                write_config(config_file_path, field, key, defaultValueValue)
                print("key:%s,field:%s,none"%(key,field))
                return defaultValueValue
            else:
                print("key:%s,field:%s,in"%(key,field))
        else:
            print("key:%s,field:%s,none"%(key,field))
            write_config(config_file_path, field, key, defaultValueValue)
            return defaultValueValue
    except configparser.Error as e1:
        print("read_config err: =====1=====")
        write_config(config_file_path, field, key, defaultValueValue)
        print("key:%s,field:%s,none"%(key,field))
        print(e1)
        return defaultValueValue
    except Exception as e2:
        print("read_config err: ======2====")
        print(e2)
        write_config(config_file_path, field, key, defaultValueValue)
        print("key:%s,field:%s,none"%(key,field))
        return defaultValueValue
    return result

def read_configs(config_file_path, field):
    result=[]
    cf = configparser.ConfigParser()
    try:
        remove_Bom(config_file_path)
        cf.read(config_file_path,encoding='utf-8-sig')
        if field in cf:
            result = cf[field]
        else:
            return []
    except configparser.Error as e1:
        print("read_config err: =====1=====")
        print(e1)
        return []
    except Exception as e2:
        print("read_config err: ======2====")
        print(e2)
        return []
    return result

def write_config(config_file_path, field, key, value):
    cf = configparser.ConfigParser()
    try:
        remove_Bom(config_file_path)
        cf.read(config_file_path,encoding='utf-8-sig')
        if field not in cf:
            cf.add_section(field)
        cf[field][key] = value
        cf.write(open(config_file_path, 'w+', encoding='utf-8-sig'))
    except configparser.Error as e:
        print(e)
        return False
    return True

def remove_Bom(file):
    try:
        BOM = b'\xef\xbb\xbf'
        existBom = lambda s: True if s==BOM else False
        f = open(file, 'rb')
        if existBom( f.read(3) ):
            fbody = f.read()
            with open(file, 'wb') as f:
                f.write(fbody)
        f.close()
    except Exception as e12:
        print(e12)
    finally:
        f.close()
     

if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit(1)

    config_file_path = sys.argv[1]
    field = sys.argv[2]
    key = sys.argv[3]
    if len(sys.argv) == 4:
        print(read_config(config_file_path, field, key))
    else:
        value = sys.argv[4]
        write_config(config_file_path, field, key, value)
 
def str2Bool(str):
    if str==None or str=="":
        return False
    return str.lower() in ("yes","true","t","1")