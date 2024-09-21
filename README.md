# Streamer

This is an end-to-end video streaming platform. The initial code is revised from [ringmaster](https://github.com/microsoft/ringmaster).

## Usage

### Prerequisites

The code is written for linux. To run the code, you need to install the following dependencies on ubuntu:
`sudo apt install g++ libvpx-dev libsdl2-dev`

Download the demo raw [video](https://media.xiph.org/video/derf/y4m/ice_4cif_30fps.y4m).

### Compile

Use `make` to compile the code.

### Run

- Use `build/sender 12345 ice_4cif_30fps.y4m` to start the sender.
- Use `build/receiver 127.0.0.1 12345 704 576 --fps30 --cbr 500` to request the demo video.