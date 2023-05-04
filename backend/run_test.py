#!/usr/bin/env python3
import getopt
import os
import sys

opts, args = getopt.getopt(sys.argv[1:], "cm:", ["coverage=", "module="])

is_coverage = False
test_module = ""
setting = "oj.settings"

for opt, arg in opts:
    if opt in ["-c", "--coverage"]:
        is_coverage = True
    if opt in ["-m", "--module"]:
        test_module = arg

print(f"Coverage: {is_coverage}")
print(f"Module: {(test_module if test_module else 'All')}")

print("running flake8...")
if os.system("flake8 --statistics --config .flake8 ."):
    exit()

ret = os.system(f'coverage run --include="$PWD/*" manage.py test {test_module} --settings={setting}')

if not ret and is_coverage:
    os.system('echo "\n----------------------------------------------------------"')
    os.system('echo "🌎 Open http://localhost:9000 to check coverage result."')
    os.system('echo "✋ Press Ctrl + C to stop serving.\n"')
    os.system("coverage html && npx --yes http-server htmlcov -s -p 9000")
