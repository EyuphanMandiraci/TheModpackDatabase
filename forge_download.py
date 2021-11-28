from wget import download
from zipfile import ZipFile
from json import loads
import minecraft_launcher_lib as mll
import threading


def download_forge_installer(version):
    global installer
    installer = f"forge-{version}-installer.jar"
    url = f"https://files.minecraftforge.net/maven/net/minecraftforge/forge/{version}/forge-{version}-installer.jar"
    download(url)



def download_forge(version):
    download_forge_installer(version)
    zf = ZipFile(installer, "r")
    with zf.open("install_profile.json", "r") as f:
        version_content = f.read()
    version_data = loads(version_content)
    forge_ver = version_data["version"]
    minecraft_ver = version_data["minecraft"]


