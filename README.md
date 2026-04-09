# Install Arch Linux
## Wifi
```bash
iwctl
station wlan0 connect toletum_5
```

## Realtime
```bash
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

## Yay
```bash
pacman -S --needed base-devel git
```

## Pipewire
```bash
pacman -S pipewire pipewire-pulse pipewire-alsa pipewire-jack wireplumber
```

## Create user
```bash
useradd -m -G wheel,audio,optical,storage,video,realtime -s /bin/bash toletum
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

# AppImages Apps
