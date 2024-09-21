CXX = g++
CXXFLAGS = -I src/app -I src/util -I src/video
CXXFLAGS_SDL = -I /usr/include/SDL2 -D_REENTRANT
# CXXFLAGS_SDL = $(shell pkg-config --cflags vpx sdl2)
LDFLAGS_VPX = -lvpx -lm
LDFLAGS_SDL = -lSDL2
# LDFLAGS = $(shell pkg-config --libs vpx sdl2)

SRC_RECEIVER = src/app/video_receiver.cc\
src/util/conversion.cc\
src/util/udp_socket.cc\
src/util/socket.cc\
src/video/sdl.cc\
src/app/protocol.cc\
src/app/decoder.cc\
src/util/address.cc\
src/util/file_descriptor.cc\
src/util/timestamp.cc\
src/video/image.cc\
src/util/serialization.cc

SRC_SENDER = src/app/video_sender.cc\
src/util/conversion.cc\
src/util/timerfd.cc\
src/util/file_descriptor.cc\
src/util/udp_socket.cc\
src/util/socket.cc\
src/util/address.cc\
src/util/poller.cc\
src/video/yuv4mpeg.cc\
src/util/split.cc\
src/app/encoder.cc\
src/video/image.cc\
src/app/protocol.cc\
src/util/serialization.cc\
src/util/timestamp.cc

all: sender receiver

sender: $(SRC_SENDER)
	$(CXX) $(SRC_SENDER) -o build/sender $(CXXFLAGS) $(LDFLAGS_VPX)

receiver: $(SRC_RECEIVER)
	$(CXX) $(SRC_RECEIVER) -o build/receiver $(CXXFLAGS) $(CXXFLAGS_SDL) $(LDFLAGS_VPX) $(LDFLAGS_SDL)

clean:
	rm build/sender build/receiver