# voiceprint
![License](https://img.shields.io/github/license/Raymo111/voiceprint)
![Language count](https://img.shields.io/github/languages/count/Raymo111/voiceprint)
![Top language](https://img.shields.io/github/languages/top/Raymo111/voiceprint)
![Last commit](https://img.shields.io/github/last-commit/Raymo111/voiceprint)
![GH Pages deployment](https://img.shields.io/github/deployments/Raymo111/voiceprint/github-pages?label=gh-pages%20deployment&logo=github)
![Site status](https://img.shields.io/website?down_message=offline&label=site%20status&logo=data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjA5IiBoZWlnaHQ9IjQ1MiIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayIgb3ZlcmZsb3c9ImhpZGRlbiI+PGRlZnM+PGNsaXBQYXRoIGlkPSJjbGlwMCI+PHBhdGggZD0iTTE4OCAxNzAgNzk3IDE3MCA3OTcgNjIyIDE4OCA2MjJaIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIvPjwvY2xpcFBhdGg+PC9kZWZzPjxnIGNsaXAtcGF0aD0idXJsKCNjbGlwMCkiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0xODggLTE3MCkiPjxwYXRoIGQ9Ik01NzguOTE2IDM2Ny45MzQgNjI2LjM5MyAzODUuOTI2IDU5NC40NzcgNDY5Ljk0NyA1NDcgNDUxLjk1NVpNNzAyLjQ5MyAxODIuOTUxIDcwMi43MjUgMTgzLjAzNkM3NTcuNTM5IDIwNi4zNDEgNzk2IDI2MC44OTggNzk2IDMyNC40ODYgNzk2IDQwOS4yNyA3MjcuNjI1IDQ3OCA2NDMuMjggNDc4IDYyNy40NjUgNDc4IDYxMi4yMTIgNDc1LjU4NCA1OTcuODY1IDQ3MS4wOThMNTk0LjUwOSA0NjkuODY0IDYyNi40MTggMzg1Ljg2MSA2MzAuNTY3IDM4Ny4xNjdDNjM0LjY3MyAzODguMDE5IDYzOC45MjUgMzg4LjQ2NyA2NDMuMjggMzg4LjQ2NyA2NzguMTE5IDM4OC40NjcgNzA2LjM2MiAzNTkuODIyIDcwNi4zNjIgMzI0LjQ4NiA3MDYuMzYyIDMwMS4yOTcgNjk0LjE5OSAyODAuOTg5IDY3NS45OSAyNjkuNzY4TDY3MC41ODMgMjY2Ljk2Wk02NjguNjcyIDE3MCA3MDIuNTM4IDE4Mi44MzQgNjcwLjY5NyAyNjYuNjU4IDYzNi44MzEgMjUzLjgyNFoiIGZpbGw9IiNGRjAwMDAiIGZpbGwtcnVsZT0iZXZlbm9kZCIvPjxwYXRoIGQ9Ik00ODEgMCAzNjcuMzc1IDAgMjQwLjUgMzI5LjEyMSAxMTMuNjI1IDAgMCAwIDE3MS4xOTUgNDUxIDE4MC45ODUgNDUxIDMwMC4wMTUgNDUxIDMwOS44MDUgNDUxWiIgZmlsbD0iIzAwQUEwMCIgZmlsbC1ydWxlPSJldmVub2RkIiB0cmFuc2Zvcm09Im1hdHJpeCgtMSAtOC43NDIyOGUtMDggLTguNzQyMjhlLTA4IDEgNjY5IDE3MCkiLz48L2c+PC9zdmc+&up_message=online&url=https%3A%2F%2Fvoiceprint.ml)
![Maintenance](https://img.shields.io/maintenance/yes/2022)

<img width="300px" src="docs/images/logo.svg"></img>

Voice biometric authentication PAM module for Linux

# Usage
1. Create two directories audio/ and audio_models/ in the parent directory
1. Run `./voiceprint-setup.sh` and `./install.sh`
1. Put `auth sufficient pam_voiceprint.so` in any pam files you want in `/etc/pam.d/` (i.e. `/etc/pam.d/sudo`)
1. Try it with `sudo -l` :)
