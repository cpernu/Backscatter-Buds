
# Phone audio configuration

This software sends audio from a gnuradio audio sink to Skype and receives
audio from Skype through a gnuradio audio source. It requires some audio setup
to make this work.

These instructions were developed and tested on a computer running Ubuntu.

## PulseAudio Volume Control

Install the PulseAudio Volume Control application from the
Ubuntu software center. It provides useful information on the audio devices
and audio signals that they are manipulating.

## Configuration principles

Every audio device that is used in a gnuradio audio sink or audio source must
be declared in the `~/.asoundrc` file.

## Audio downlink setup

For the audio downlink, Skype should send audio to the default audio device.
The operating system creates a monitor device for the default audio device.
This software should get its audio from the monitor device.

Run `pactl list` and look for the name of the default audio device. On one
computer, it is `alsa_output.pci-0000_00_1b.0.analog-stereo`. The audio device
should have a corresponding monitor device. On one computer, the monitor device
name is `alsa_output.pci-0000_00_1b.0.analog-stereo.monitor`.

Edit the `~/.asoundrc` file, adding the following lines:

    pcm.skype_monitor {
        type pulse
        device [the name of the monitor device]
    }

    ctl.skype_monitor {
        type pulse
        device [the name of the monitor device]
    }

Now, the gnuradio audio source should find the `skype_monitor` device and
get audio fom Skype.

## Audio uplink setup

For the audio uplink, this software sends audio to a null sink. Skype receives
audio from the monitor of the null sink.

Create a null sink with the following command:

    pactl load-module module-null-sink sink_name=audio_rx_loopback

You may need to repeat this after the computer restarts.

Edit the `~/.asoundrc` file, adding the following lines:

    pcm.audio_rx_loopback {
        type pulse
        device audio_rx_loopback
    }

    ctl.audio_rx_loopback {
        type pulse
        device audio_rx_loopback
    }

Now, the gnuradio audio sink should find the `audio_rx_loopback` device and
transmit audio to it.

While Skype is running and a call is in progress, use PulseAudio Volume Control
to set Skype to use the "Monitor of null sink" device for input.

## Further reading

[Arch Linux Pulse Audio examples](https://wiki.archlinux.org/index.php/PulseAudio/Examples)

[gnuradio audio documentation](https://wiki.gnuradio.org/index.php/ALSAPulseAudio)
