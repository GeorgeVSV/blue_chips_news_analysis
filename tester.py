from configparser import ConfigParser
import re

conf = ConfigParser()
conf.read('config/cnf.ini')
#print(conf['website_url']['usr_agent'])


print(re.sub(r',.*', "", 'Polymetal, облигация'))