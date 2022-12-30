import json
f = open("donnees_communes.json")
dz_data = json.loads(f.read())

def communes(wilaya):
  communes = [commune for commune in dz_data if commune["wilaya"].lower() == wilaya.lower()]
  communes = [x["commune"] for x in communes]
  return sorted(communes)

def wilayaString(codeWilaya):
  for x in dz_data:
    if( x["wilaya_code"] == str(codeWilaya)):
      return x["wilaya"]
  return "Invalid"