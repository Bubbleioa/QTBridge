#coding = utf-8
import configparser

cf = configparser.ConfigParser()
cf.read("config.ini", encoding = 'utf-8')

# get all sections: cf.sections()
# get section's key: cf.options('section_1')
# get section's key and value: cf.items('section_1')
def get(section, key):
    #get value from section's key
    return cf.get(section, key)

# add section's key:value - cf.set('section_1', 'key_1', 'value_1')
def addSection(section):
    cf.add_section(section)
    cf.write(open('config.ini', 'w'))

def addKey(section, key, value):
    cf.set(section, key, value)
    cf.write(open('config.ini', 'w'))

def delete(section, key, value):
    cf.remove_option(section, key)
    cf.write(open('config.ini', 'w'))