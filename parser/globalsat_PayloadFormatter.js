// NOTE: This is pretty much a translation of tanupoo's Python parser for the GlobalSat into JS.
// No guarantee this works perfectly.
// You can find the original Python parser here:
// Repo: https://github.com/tanupoo/lorawan-ssas
// Code file: https://github.com/tanupoo/lorawan-ssas/blob/master/parsers/parser_globalsat_lt500.py
// Original license:
// MIT License
//
// Copyright (c) 2017 Shoichi Sakane
//
// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:
//
// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

function byteToHex(byte) {
    return ('0' + (byte & 0xFF).toString(16)).slice(-2);
}

function parseNumber(bytes, isLittleEndian) {
    function padArrayToFourBytes(bytes, isLittleEndian) {
        const paddedArray = new Uint8Array(4);
        const offset = isLittleEndian ? 0 : 4 - bytes.length
        paddedArray.set(bytes, offset);
        return paddedArray;
    }

    const byteArray = padArrayToFourBytes(bytes);
    const dataView = new DataView(byteArray.buffer);
    const intValue = dataView.getUint32(0, isLittleEndian);
    return intValue;
}

function parseHex(bytes) {
    let hexString = '';
    for (let i = 0; i < bytes.length; i++) {
        hexString += byteToHex(bytes[i]);
    }
    return hexString;
}

function parseGCV(data) {
    return parseNumber(data, true) / 1000000;
}

function parseB5to7(data) {
    return parseNumber(data, false) >> 5;
}

function parseB0to4(data) {
    return parseNumber(data, false) & 31;
}

function parse_track_rep(bytes) {
    if (bytes.length == 17) {
        return {
            "version": parseNumber(bytes.slice(0, 1), false),
            "command_id": parseNumber(bytes.slice(1, 3), false),
            "lon": parseGCV(bytes.slice(3, 7)),
            "lat": parseGCV(bytes.slice(7, 11)),
            "gps_fix": parseB5to7(bytes.slice(11, 12)),
            "report_type": parseB0to4(bytes.slice(11, 12)),
            "batt": parseNumber(bytes.slice(12, 13), false),
            "timestamp": parseNumber(bytes.slice(13, 17), true),
        }
    }
    else {
        return false
    }
}

function parse_track_rep_short(bytes) {
    if (bytes.length == 11) {
        return {
            "version": parseNumber(bytes.slice(0, 1), false),
            "command_id": parseNumber(bytes.slice(1, 2), false),
            "lon": parseGCV(bytes.slice(2, 6)),
            "lat": parseGCV(bytes.slice(6, 10)),
            "gps_fix": parseB5to7(bytes.slice(10, 11)),
            "report_type": parseB0to4(bytes.slice(10, 11)),
        }
    } else {
        return false
    }
}

function parse_help_rep(bytes) {
    if (bytes.length == 17) {
        return {
            "version": parseNumber(bytes.slice(0, 1), false),
            "command_id": parseNumber(bytes.slice(1, 3), false),
            "lon": parseGCV(bytes.slice(3, 7)),
            "lat": parseGCV(bytes.slice(7, 11)),
            "gps_fix": parseB5to7(bytes.slice(11, 12)),
            "alarm_type": parseB0to4(bytes.slice(11, 12)),
            "batt": parseNumber(bytes.slice(12, 13), false),
            "timestamp": parseNumber(bytes.slice(13, 17), true),
        }
    }
    else {
        return false
    }
}

function parse_help_rep_short(bytes) {
    if (bytes.length == 11) {
        return {
            "version": parseNumber(bytes.slice(0, 1), false),
            "command_id": parseNumber(bytes.slice(1, 2), false),
            "lon": parseGCV(bytes.slice(2, 6)),
            "lat": parseGCV(bytes.slice(6, 10)),
            "gps_fix": parseB5to7(bytes.slice(10, 11)),
            "alarm_type": parseB0to4(bytes.slice(10, 11)),
        }
    }
    else {
        return false
    }
}

function parse_beacon_track_rep(bytes) {
    if (bytes.length == 27) {
        return {
            "version": parseNumber(bytes.slice(0, 1), false),
            "command_id": parseNumber(bytes.slice(1, 3), false),
            "beacon_id": parseHex(bytes.slice(3, 23)),
            "beacon_type": parseB5to7(bytes.slice(23, 24)),
            "report_type": parseB0to4(bytes.slice(23, 24)),
            "rssi": parseNumber(bytes.slice(24, 25), false),
            "tx_power": parseNumber(bytes.slice(25, 26), false),
            "batt": parseNumber(bytes.slice(26, 27), false),
        }
    }
    else {
        return false
    }
}

function parse_beacon_help_rep(bytes) {
    if (bytes.length == 27) {
        return {
            "version": parseNumber(bytes.slice(0, 1), false),
            "command_id": parseNumber(bytes.slice(1, 3), false),
            "beacon_id": parseHex(bytes.slice(3, 23)),
            "beacon_type": parseB5to7(bytes.slice(23, 24)),
            "alarm_type": parseB0to4(bytes.slice(23, 24)),
            "rssi": parseNumber(bytes.slice(24, 25), false),
            "tx_power": parseNumber(bytes.slice(25, 26), false),
            "batt": parseNumber(bytes.slice(26, 27), false),
        }
    } else {
        return false
    }
}

function parse_command(bytes) {
    if (bytes.length == 9) {
        cmd = bytes[3]
        if (cmd & 0x01) {
            return {
                "version": parseNumber(bytes.slice(0, 1), false),
                "command_id": parseNumber(bytes.slice(1, 3), false),
                "command_type": parseHex(bytes.slice(3, 4)),
                "gps_interval": parseNumber(bytes.slice(7, 9), false),
            }
        } else if (cmd & 0x02) {
            return {
                "version": parseNumber(bytes.slice(0, 1), false),
                "command_id": parseNumber(bytes.slice(1, 3), false),
                "command_type": parseHex(bytes.slice(3, 4)),
                "report_interval": parseNumber(bytes.slice(5, 7), false),
            }
        } else if (cmd & 0x04) {
            return {
                "version": parseNumber(bytes.slice(0, 1), false),
                "command_id": parseNumber(bytes.slice(1, 3), false),
                "command_type": parseHex(bytes.slice(3, 4)),
                "moving_interval": parseNumber(bytes.slice(5, 7), false),
                "static_interval": parseNumber(bytes.slice(7, 9), false),
            }
        } else {
            return false
        }
    }
}

function parse_dismiss_help_rep(bytes) {
    if (bytes.length == 12) {
        return {
            "version": parseNumber(bytes.slice(0, 1), false),
            "command_id": parseNumber(bytes.slice(1, 3), false),
            "stop_help_rep": parseNumber(bytes.slice(11, 12), false),
        }
    } else {
        return false
    }
}

function parse_set_device(bytes) {
    if (bytes.slice(-2).toString(16) === "0d0a") {
        const cmdLen = bytes[3]
        return {
            "version": parseNumber(bytes.slice(0, 1), false),
            "command_id": parseNumber(bytes.slice(1, 3), false),
            "length": parseNumber(bytes.slice(3, 4), false),
            "command": parseHex(bytes.slice(4, 4 + cmdLen))
        }
    } else {
        return false
    }
}

// input has the following structure:
// {
//   "bytes": [1, 2, 3], // FRMPayload (byte array)
//   "fPort": 1
// }
function decodeUplink(input) {
    let bytes = input.bytes
    let protocolVersion = bytes[0]
    let data = {}
    let errors = []

    if (protocolVersion == 0x0C) {
        commands = {
            "1002": parse_track_rep,
            "0b00": parse_help_rep,
            "1302": parse_beacon_track_rep,
            "0700": parse_beacon_help_rep,
            "0600": parse_command,
            "1102": parse_dismiss_help_rep,
            "0800": parse_set_device,
        }
        commandId = byteToHex(bytes[1]) + byteToHex(bytes[2])
        if (commandId in commands) {
            data = commands[commandId](bytes)
        } else {
            errors.push("Unknown command ID")
        }
    } else if (protocolVersion == 0x80) {
        shortCommandId = bytes[1]
        if (shortCommandId == 0x83) {
            data = parse_track_rep_short(bytes)
        } else if (shortCommandId == 0x01) {
            data = parse_help_rep_short(bytes)
        } else {
            errors.push("Unknown short command ID")
        }
    } else {
        errors.push("Unknown protocol version")
    }

    return {
        data: data,
        warnings: [],
        errors: errors
    };
}

console.log(decodeUplink({"bytes": [128, 131, 189, 2, 152, 0, 145, 199, 247, 2, 2]}))
