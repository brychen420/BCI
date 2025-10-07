from pylsl import resolve_stream
from pylsl import StreamInlet
# import numpy as np
import serial
import queue
import time

thres = 0.2  # alpha_threshold
blink_thres = 0.0
blink_bool = False
blink_counter = 0
timestamp_counter = 0
qsize = 30   # max queue size


def main():
    import argparse
    parser = argparse.ArgumentParser(description="CECNL BCI 2023 Car Demo")
    parser.add_argument("port_num", type=str,
                        help="Arduino bluetooth serial port")
    args = parser.parse_args()

    ser = serial.Serial(args.port_num, 9600, timeout=1, write_timeout=1)

    q = queue.Queue(maxsize=qsize)

    streams = resolve_stream('name', 'OpenViBE Stream1')
    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])

    while True:
        samples, timestamp = inlet.pull_chunk()
        print(samples)
        alpha_wave = samples[0]
        blink = samples[1]
        if timestamp:
            alpha_wave = alpha_wave[0]
            blink = blink[0]  # or delete this row
            # print(alpha_wave)  # find fish
            while q.qsize() >= qsize:
                _ = q.get()
            q.put(alpha_wave)

            ratio = sum(list(q.queue)) / q.qsize()

            if blink > blink_thres and not blink_bool:
                blink_counter += 1
                blink_bool = True
            elif blink > blink_thres:
                blink_bool = True
            elif blink_bool:
                blink_bool = False
                timestamp_counter = timestamp
            else:
                if timestamp-timestamp_counter > 1:  # blink gap
                    blink_counter = 0
                blink_bool = False

            if blink_counter == 3:
                print("turn")
                ser.write(b'3')  # turn right
                blink_counter = 0
            elif blink_counter > 0:
                print("stop")
                ser.write(b'0')
            elif ratio > thres and q.qsize() == qsize:
                print("move forward", ratio)
                ser.write(b'1')
            else:
                print("stop ", ratio)
                ser.write(b'0')
        time.sleep(0.2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        exit(0)
