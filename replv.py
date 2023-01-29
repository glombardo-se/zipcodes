import re;import os;d=open('setup.py', 'r');b = d.read();b = re.sub('"1\.0\.0"', f"\"{os.environ['APPVEYOR_BUILD_RELEASE']}\"", b);d.close();d = open('setup.py', 'w+');d.write(b);

