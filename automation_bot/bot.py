import json

def loadFromJSNON(fileName):
  with open(fileName) as f:
    fileStuff = f.read()
    loadedStructure = json.loads(fileStuff)
  return loadedStructure

if __name__ == "__main__":
  print('configure: ', loadFromJSNON('bot_config.json'))