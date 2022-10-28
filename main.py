import os
from configparser import ConfigParser


def main():
    title_id_dict = {
        "0100000000010000": "your theme",
        "0100000000000000": "fs",
        "0100000000000001": "ldr",
        "0100000000000002": "ncm",
        "0100000000000003": "pm",
        "0100000000000004": "sm",
        "0100000000000005": "boot",
        "0100000000000006": "usb",
        "0100000000000007": "tma.stub/htc.stub",
        "0100000000000008": "boot2",
        "0100000000000009": "settings",
        "010000000000000A": "Bus",
        "010000000000000B": "bluetooth",
        "010000000000000C": "bcat",
        "010000000000000D": "dmnt",
        "010000000000000E": "friends",
        "010000000000000F": "nifm",
        "0100000000000010": "ptm",
        "0100000000000011": "shell",
        "0100000000000012": "bsdsockets",
        "0100000000000013": "hid",
        "0100000000000014": "audio",
        "0100000000000015": "LogManager",
        "0100000000000016": "wlan",
        "0100000000000017": "cs",
        "0100000000000018": "ldn",
        "0100000000000019": "nvservices",
        "010000000000001A": "pcv",
        "010000000000001B": "ppc/capmtp",
        "010000000000001C": "nvnflinger",
        "010000000000001D": "pcie/pcie.withoutHb",
        "010000000000001E": "account",
        "010000000000001F": "ns",
        "0100000000000020": "nfc",
        "0100000000000021": "psc",
        "0100000000000022": "capsrv",
        "0100000000000023": "am",
        "0100000000000024": "ssl",
        "0100000000000025": "nim",
        "0100000000000026": "cec",
        "0100000000000027": "tspm",
        "0100000000000028": "spl",
        "0100000000000029": "lbl",
        "010000000000002A": "btm",
        "010000000000002B": "erpt",
        "010000000000002C": "time",
        "010000000000002D": "vi",
        "010000000000002E": "pctl",
        "010000000000002F": "npns",
        "0100000000000030": "eupld",
        "0100000000000031": "arp/glue",
        "0100000000000032": "eclct",
        "0100000000000033": "es",
        "0100000000000034": "fatal",
        "0100000000000035": "grc",
        "0100000000000036": "creport",
        "0100000000000037": "ro",
        "0100000000000038": "profiler",
        "0100000000000039": "sdb",
        "010000000000003A": "migration",
        "010000000000003B": "jit",
        "010000000000003C": "jpegdec",
        "010000000000003D": "safemode",
        "010000000000003E": "olsc",
        "010000000000003F": "dt",
        "0100000000000040": "nd",
        "0100000000000041": "ngct",
        "0100000000000042": "pgl",
        "0100000000000045": "omm",
        "0100000000000046": "eth",
        # homebrew
        "0000000000534C56": "SaltyNX",
        "00FF0000000002AA": "BootSoundNX",
        "00FF0000636C6BF2": "nx-reader",
        "00FF0000636C6BFF": "sys-clk",
        "00FF00006D7470FF": "mtp-server-nx",
        "00FF0000A53BB665": "SysDVR",
        "00FF747765616BFF": "switch-sys-tweak",
        "0100000000000052": "switch-nfp-mitm",
        "0100000000000081": "nx-btred",
        "0100000000000352": "emuiibo",
        "0100000000000464": "SwitchPresence",
        "0100000000000523": "aoc-mitm",
        "0100000000000901": "OJDS-NX",
        "0100000000000BED": "vax",
        "0100000000000BEF": "fsp-usb",
        "0100000000000dad": "nx_overlay",
        "0100000000000f12": "Fizeau",
        "0100000000000faf": "hid-mitm/hid-mitm-plus",
        "0100000000006480": "twili",
        "0100000000007200": "ilia",
        "010000000000bd00": "MissionControl",
        "010000000000C235": "Freebird",
        "010000000000f00f": "dvdnx",
        "010000000000FFAB": "usb-mitm",
        "01000000001ED1ED": "maydel",
        "0532232232232000": "NX-input-recorder",
        "054e4f4558454000": "noexs",
        "2200000000000100": "SplitNX",
        "4100000000000324": "sys-http",
        "4200000000000000": "sys-tune/sys-audioplayer",
        "420000000000000E": "sys-ftpd/sys-ftpd-light",
        "420000000000000F": "SlideNX",
        "4200000000000010": "ldn_mitm",
        "4200000000000811": "bitmap-printer",
        "4200000000000BA6": "BTSounds",
        "4200000000000BAC": "SwiTAS",
        "4200000000000FFF": "sys-triplayer",
        "420000000007E51A": "nx-ovlloader",
        "4200000000474442": "sys-gdbstub",
        "4200000000696969": "sys-logger",
        "4200000AF1E8DA89": "ControllerSaver",
        "42000062616B6101": "sys-screenuploader",
        "4200736372697074": "sys-script",
        "4206900000000012": "sfdnsres_mitm",
        "430000000000000A": "sys-netcheat",
        "430000000000000B": "sys-botbase",
        "430000000000000C": "sys-botbaseplus",
        "43000000000000FF": "nxsh",
        "4300000000000909": "NXGallery",
        "5600000000000000": "NXCord",
        "690000000000000D": "sys-con"
    }

    config = ConfigParser()
    config.read('config.ini')
    path = config.get('config', 'path')
    allow_user_input = config.getboolean('config', 'allow_user_input')
    allow_path_input = config.getboolean('config', 'allow_path_input')
    ids = []
    if allow_path_input:
        ids.extend([name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))])
    if allow_user_input:
        ids.extend(get_user_input())
    if not ids:
        print("allow at least one input")
        return

    for folder_name in ids:
        try:
            print(f"-> \"{title_id_dict[folder_name]}\" is the Name of \"{folder_name}\"")
        except KeyError:
            print(f"-> There is no known Name for \"{folder_name}\"")


def get_user_input():
    input_list = []
    print("Enter file names one per line, leave empty to proceed")
    while True:
        user_input = input()
        if user_input:
            input_list.append(user_input)
        else:
            break
    return input_list


if __name__ == '__main__':
    main()
