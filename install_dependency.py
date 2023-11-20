#!/usr/bin/env python3

import sys
import subprocess

def main():
    package_list = ["numpy", "pandas", "matplotlib", "plotly", "python-dotenv", "customtkinter", "scikit-learn", "networkx", "openai"]
    for package_name in package_list:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])




if __name__ == "__main__":
    main()