import os, sys

dir_path = os.path.dirname(os.path.realpath(__file__)) #tests folder
dir_path = os.path.dirname(os.path.realpath(dir_path)) #marketplace folder

sys.path.append('/home/elama/dev-tools/Projects/junior-marketplace/marketplace.app/.venv/lib/python3.6/site-packages')
dir_path = os.path.dirname(os.path.realpath(dir_path)) #marketplace.app folder
sys.path.append(dir_path)


