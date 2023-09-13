import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["discord"],
    "excludes": [],
    "include_files": []
}

base = None

if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable("main.py", base=base)
]

setup(
    name="OrganizaBot",
    version="1.0",
    description="Bot para auxiliar nas tarefas do trabalho.",
    options={"build_exe": build_exe_options},
    executables=executables
)
