import base64
import argparse

def get_args():
    configuredArgs = [{
        "shortName": "f",
        "name": "file",
        "default": "log.log",
        "help": "Specify the log file"
    }]
    parser = argparse.ArgumentParser()

    for arg in configuredArgs:
        parser.add_argument(
            f"-{arg['shortName']}",
            f"--{arg['name']}",
            default = arg["default"],
            help = arg["help"]            
        )

    return parser.parse_args()

args = get_args()
file1 = open("log1.log", "r") 
hook = '"Payload'
hook2 = 'ERROR'
hook3 = 'INFO'
#print('line,decoded')
for index, line in enumerate(file1):
    if hook2 in line or hook3 in line:
        print('Fecha: ', line[0:30])
    if hook in line:
        # print(index + 1)
        payloadIndex = line.index(hook)
        # print("####################### START #######################")
        # print(line)
        payloadIndexReal = 0
        for counter in range(1, 20, 1):
            posibleIndex = payloadIndex + len(hook) + counter
            character = line[posibleIndex]
            if not (character in '\"": \\"'):
                payloadIndexReal = posibleIndex
                break
        payloadIndexEnd = len(line)
        try:
            payloadIndexEnd = line[payloadIndexReal:len(line)].index('"') +payloadIndexReal
        except:
            pass
        # print(payloadIndexReal,payloadIndexEnd)
        payloadCleaned = line[payloadIndexReal:payloadIndexEnd]
        if (payloadCleaned[-1] == "\\"):
            payloadCleaned = line[payloadIndexReal:payloadIndexEnd - 1]
        decoded = ""
        attemp = 1
        while attemp < 4:
            try:
                decoded = base64.b64decode(payloadCleaned + "=")
                break
            except:
                payloadCleaned = payloadCleaned[0: len(payloadCleaned) - 2]
                attemp += 1
        print("Decode: ",decoded) 
        # print("####################### END #######################")
    