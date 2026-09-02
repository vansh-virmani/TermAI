import platform
import os

def get_os():

    return platform.system()




def get_shell():
    os_name=platform.system()
    if os_name == "Windows":
        if os.environ.get("PSModulePath"):
            return "PowerShell"
        return "CMD"
    shell=os.environ.get("SHELL")

    if shell:
        return shell.split("/")[-1]
    return "Unknown"
    



   