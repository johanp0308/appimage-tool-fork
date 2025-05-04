#!/usr/bin/env python3

import os
import sys
import shutil
import argparse
import stat
from pathlib import Path

def make_executable(path):
    mode = os.stat(path).st_mode
    os.chmod(path, mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)  # Permisos de ejecución

def copy_appimage(origin_path, name):
    destination_dir = Path.home() / "Applications"
    destination_dir.mkdir(exist_ok=True)  # Crear si no existe
    destination = destination_dir / f"{name.lower().replace(' ', '-')}.AppImage"  # Copiar con el nombre del icono
    shutil.copy(origin_path, destination) 
    return destination

def copy_icon(origin_path, name):
    destination_dir = Path.home() / ".local/share/icons"
    destination_dir.mkdir(exist_ok=True)
    
    # Extraer la extensión del archivo icono (por ejemplo, .png o .svg)
    icon_extension = origin_path.suffix.lower()  # `.suffix` devuelve la extensión del archivo
    destination = destination_dir / f"{name.lower().replace(' ', '-')}{icon_extension}"  # Usamos la misma extensión del icono
    
    shutil.copy(origin_path, destination) 
    return destination

def create_dot_desktop(path_appimage, name="NewAppImage", icon=None):
    desktop_dir = Path.home() / ".local/share/applications"
    desktop_dir.mkdir(parents=True, exist_ok=True)  # Crear directorios intermedios
    desktop_file = desktop_dir / f"{name.lower().replace(' ', '-')}.desktop"  # Nombre basado en el appname

    icon_path = icon if icon else "application-default-icon"  # Usar icono por defecto si no se proporciona

    content = f"""[Desktop Entry]
Name={name}
Exec="{path_appimage}"
Icon={icon_path}
Type=Application
Categories=Utility;
Terminal=false
"""
    
    with open(desktop_file, "w") as f:
        f.write(content)

    os.chmod(desktop_file, 0o755)  # Dar permisos de ejecución al archivo .desktop
    print(f"File .desktop created in: {desktop_file}")
    
    # Recargar la base de datos de los escritorios para que el sistema reconozca el nuevo .desktop
    os.system("update-desktop-database ~/.local/share/applications/")

def delete_launch_appimage(name_dot_dektop, name_icon):
    dektop_dir = Path.home() / ".local/share/applications"
    icon_dir = Path.home() / ".local/share/icons"
    
    if( (dektop_dir / (name_dot_dektop+".desktop")).exists() ):
        os.remove(dektop_dir / (name_dot_dektop+".desktop"))
        
    if( (icon_dir / (name_icon + ".*"))):
        os.remove(icon_dir / (name_icon + ".*"))
    os.system("update-desktop-database ~/.local/share/applications/")

def main():
    parser = argparse.ArgumentParser(description="AppImage Installer")
    parser.add_argument('--appimage', required=True, help='AppImage path')
    parser.add_argument('--name', help='Application name')
    parser.add_argument('--icon', help='Icon path .png o .svg')

    args = parser.parse_args()
    path_appimage = Path(args.appimage)

    if not path_appimage.exists():
        print("❌ AppImage doesn't exist")
        sys.exit(1)

    make_executable(path_appimage)

    # Utilizamos el nombre proporcionado o el nombre del archivo AppImage como nombre por defecto
    app_name = args.name or path_appimage.stem

    copy_path_appimage = copy_appimage(path_appimage, app_name)

    if args.icon:
        path_icon = Path(args.icon)
        copy_path_icon = copy_icon(path_icon, name=app_name)
    else:
        copy_path_icon = None

    create_dot_desktop(
        path_appimage=copy_path_appimage, 
        name=app_name, 
        icon=copy_path_icon if copy_path_icon else None
    )

    print("✅ AppImage installed successfully.")  

if __name__ == "__main__":
    main()
