pip3 show virtualenv
pip3 show pymysql
pip3 show Flask
pip3 install virtualenv

#create databases
mysql -u root -p -D portaltest < portal0811.sql

#install virtualenv
mkdir myproject
cd myproject
#virtualenv --no-site-packages venv
#deactivate
source ../venv/bin/activate

pip3 install flask
pip3 install pymysql
pip3 install requests
pip3 install xlrd

touch ./myflasktest/myPerformance/GKJY-TEST/run_test/excel/myrule.py

