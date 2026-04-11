# Install Arch Linux
## Wifi
```bash
iwctl
station wlan0 connect toletum_5
```

## Update All
```bash
pacman -Syu --noconfirm
```

## Realtime
```bash
pacman -Syu --noconfirm
pacman -S linux-rt linux-rt-headers
pacman -S realtime-privileges
grub-mkconfig -o /boot/grub/grub.cfg

reboot
```

## Zram Swap
```bash
cat <<EOF > /etc/modprobe.d/zram.conf 
options zram num_devices=1
EOF

cat <<EOF > /etc/systemd/system/zram.service 
[Unit]
Description=Configurar zRAM con lzo-rle
After=multi-user.target

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStartPre=/usr/bin/modprobe zram
ExecStart=/usr/bin/sh -c 'echo lzo-rle > /sys/block/zram0/comp_algorithm'
ExecStart=/usr/bin/sh -c 'echo 4G > /sys/block/zram0/disksize'
ExecStart=/usr/bin/mkswap /dev/zram0
ExecStart=/usr/bin/swapon /dev/zram0 -p 100
ExecStop=/usr/bin/swapoff /dev/zram0

[Install]
WantedBy=multi-user.target
EOF

cat <<EOF > /etc/sysctl.d/99-swappiness.conf 
vm.swappiness=10
vm.vfs_cache_pressure=50
EOF

systemctl daemon-reload
systemctl enable --now zram.service
sysctl --system
```

## System Apps
```bash
pacman -S --needed base-devel git flatpak
```

## Yay
```bash
git clone https://aur.archlinux.org/yay-bin.git

cd yay-bin
makepkg -si
```

## Pipewire
```bash
pacman -S pipewire pipewire-pulse pipewire-alsa pipewire-jack wireplumber
```

## Create user
```bash
useradd -m -U -G wheel,audio,optical,storage,video,realtime -s /bin/bash toletum
```

```bash
visudo

%wheel ALL=(ALL:ALL) ALL
```

## RT
```bash
cat <<EOF > /etc/security/limits.d/99-audio.conf 
@realtime - rtprio 98
@realtime - memlock unlimited
EOF

cat <<EOF > /etc/security/limits.d/99-realtime-privileges.conf 
@realtime - nice -11
EOF
```

# User
```bash
systemctl --user enable --now pipewire.service pipewire-pulse.service wireplumber.service
```

# FlatPak Apps

| Aplicación | ID de Aplicación | Descripción |
| :--- | :--- | :--- |
| **TuxGuitar** | `ar.com.tuxguitar.TuxGuitar` | Editor y reproductor multipista de partituras y tablaturas. |
| **Giada** | `com.giadamusic.Giada` | Herramienta minimalista para loop station y secuencer de audio. |
| **Flatseal** | `com.github.tchx84.Flatseal` | Gestor gráfico de permisos para aplicaciones Flatpak. |
| **VMPK** | `net.sourceforge.VMPK` | Piano virtual MIDI para eventos de red o dispositivos externos. |
| **Audacity** | `org.audacityteam.Audacity` | Editor de audio profesional de código abierto y grabación. |
| **Calf** | `org.freedesktop.LinuxAudio.Plugins.Calf` | Suite de plugins de efectos y procesamiento de audio avanzado. |
| **Guitarix LV2** | `org.freedesktop.LinuxAudio.Plugins.Guitarix` | Amplificador de guitarra virtual en formato de plugin LV2. |
| **LSP** | `org.freedesktop.LinuxAudio.Plugins.LSP` | Plugins de audio de alta fidelidad para mezcla y masterización. |
| **Ratatouille** | `org.freedesktop.LinuxAudio.Plugins.Ratatouille` | Simulador de amplificadores basado en modelos neuronales. |
| **Surge Synthesizer** | `org.freedesktop.LinuxAudio.Plugins.Surge` | Potente sintetizador híbrido de código abierto. |
| **sfizz** | `org.freedesktop.LinuxAudio.Plugins.sfizz` | Reproductor de muestras compatible con el formato SFZ. |
| **SWH** | `org.freedesktop.LinuxAudio.Plugins.swh` | Colección clásica de plugins de efectos de audio LADSPA. |
| **x42Plugins** | `org.freedesktop.LinuxAudio.Plugins.x42Plugins` | Conjunto de utilidades y medidores de audio profesional. |
| **GIMP** | `org.gimp.GIMP` | Editor avanzado de imágenes y manipulación fotográfica. |
| **G'MIC** | `org.gimp.GIMP.Plugin.GMic` | Framework completo con cientos de filtros para procesado de imagen. |
| **guitarix** | `org.guitarix.Guitarix` | Amplificador de guitarra digital para sistemas Linux. |
| **Hydrogen** | `org.hydrogenmusic.Hydrogen` | Caja de ritmos avanzada basada en patrones. |
| **Firefox** | `org.mozilla.firefox` | Navegador web enfocado en la privacidad y estándares abiertos. |
| **Qsynth** | `org.rncbc.qsynth` | Interfaz gráfica para el sintetizador de software FluidSynth. |
| **Shotcut** | `org.shotcut.Shotcut` | Editor de vídeo multiplataforma gratuito y de código abierto. |
| **Surge XT** | `org.surge_synth_team.surge-xt` | Versión mejorada y moderna del sintetizador Surge. |
| **VLC** | `org.videolan.VLC` | Reproductor multimedia universal compatible con casi cualquier formato. |
| **Wine** | `org.winehq.Wine` | Capa de compatibilidad para ejecutar software de Windows en Linux. |
| **gecko-wow64** | `org.winehq.Wine.gecko-wow64` | Motor de renderizado web para aplicaciones Wine de 64 bits. |
| **mono-wow64** | `org.winehq.Wine.mono-wow64` | Implementación de .NET para ejecutar aplicaciones de Windows en Wine. |
| **Carla** | `studio.kx.carla` | Gestor de plugins de audio y rack de efectos modular. |
| **MuseScore** | `org.musescore.MuseScore` | Software profesional de notación musical y creación de partituras. |

```bash
flatpak install flathub ar.com.tuxguitar.TuxGuitar -y
flatpak install flathub com.giadamusic.Giada -y
flatpak install flathub com.github.tchx84.Flatseal -y
flatpak install flathub net.sourceforge.VMPK -y
flatpak install flathub org.audacityteam.Audacity -y
flatpak install flathub org.freedesktop.LinuxAudio.Plugins.Calf -y
flatpak install flathub org.freedesktop.LinuxAudio.Plugins.Guitarix -y
flatpak install flathub org.freedesktop.LinuxAudio.Plugins.LSP -y
flatpak install flathub org.freedesktop.LinuxAudio.Plugins.Ratatouille -y
flatpak install flathub org.freedesktop.LinuxAudio.Plugins.Surge -y
flatpak install flathub org.freedesktop.LinuxAudio.Plugins.sfizz -y
flatpak install flathub org.freedesktop.LinuxAudio.Plugins.swh -y
flatpak install flathub org.freedesktop.LinuxAudio.Plugins.x42Plugins -y
flatpak install flathub org.gimp.GIMP -y
flatpak install flathub org.gimp.GIMP.Plugin.GMic -y
flatpak install flathub org.guitarix.Guitarix -y
flatpak install flathub org.hydrogenmusic.Hydrogen -y
flatpak install flathub org.mozilla.firefox -y
flatpak install flathub org.rncbc.qsynth -y
flatpak install flathub org.shotcut.Shotcut -y
flatpak install flathub org.surge_synth_team.surge-xt -y
flatpak install flathub org.videolan.VLC -y
flatpak install flathub org.winehq.Wine -y
flatpak install flathub org.winehq.Wine.gecko-wow64 -y
flatpak install flathub org.winehq.Wine.mono-wow64 -y
flatpak install flathub studio.kx.carla -y
flatpak install flathub org.musescore.MuseScore -y
```

# YAY
| Aplicación | Descripción |
| :--- | :--- |
| **Appimagelauncher** | Herramienta que integra archivos AppImage |
| **Iwgtk** | gestionar redes Wi-Fi |


# AppImages Apps
| Aplicación | Descripción |
| :--- | :--- |
| **AnthemScore** | Software de transcripción de audio a partituras basado en **IA**. |
| **LMMS** | Estación de trabajo de audio digital (**DAW**) para producción musical. |
| **MusE** | Secuenciador de audio y **MIDI** con capacidades de grabación. |

```bash
python -m venv venv
./venv/bin/pip install -r requirements.txt
./update_gh.sh
```
