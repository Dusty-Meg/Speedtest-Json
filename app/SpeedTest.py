import subprocess
import json
import datetime
import os


def bytes_to_bits(bytes_per_sec):
    return bytes_per_sec * 8


def bits_to_megabits(bits_per_sec):
    megabits = round(bits_per_sec * (10**-6), 2)
    return str(megabits) + " Mb/s"


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True


def test():
    timeout = int(os.environ.get('SPEEDTEST_TIMEOUT', 90))

    cmd = ["speedtest", "--format=json-pretty", "--progress=no",
           "--accept-license", "--accept-gdpr"]
    try:
        output = subprocess.check_output(cmd, timeout=timeout)
    except subprocess.CalledProcessError as e:
        output = e.output
        if not is_json(output):
            if len(output) > 0:
                print('Speedtest CLI Error occurred that' +
                      'was not in JSON format')
                print(output)
            return (0, 0, 0, 0, 0, 0)
    except subprocess.TimeoutExpired:
        print('Speedtest CLI process took too long to complete ' +
              'and was killed.')
        return (0, 0, 0, 0, 0, 0)

    if is_json(output):
        data = json.loads(output)
        if "error" in data:
            # Socket error
            print('Something went wrong')
            print(data['error'])
            return (0, 0, 0, 0, 0, 0)  # Return all data as 0
        if "type" in data:
            if data['type'] == 'log':
                print(str(data["timestamp"]) + " - " + str(data["message"]))
            if data['type'] == 'result':
                actual_server = int(data['server']['id'])
                actual_jitter = data['ping']['jitter']
                actual_ping = data['ping']['latency']
                download = bytes_to_bits(data['download']['bandwidth'])
                upload = bytes_to_bits(data['upload']['bandwidth'])
                return (actual_server, actual_jitter,
                        actual_ping, download, upload, 1)
