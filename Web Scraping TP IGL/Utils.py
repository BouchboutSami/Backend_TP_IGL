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

def GetPrice(ancienPrix:str):
  remplacements = {"Millions":"10000","Milliards":"10000000","DA":"1","m²":"1","/":"1"," ":"1","000":"1000"}
  ops = ancienPrix.split(" ")
  if ops[0].isnumeric() and ops[1].isnumeric():
    ops[0]=int(str(ops[0])+str(ops[1]))
    ops[1]=1
  newops=[]
  for op in ops:
    valid=False
    for key in remplacements:
      if op == key:
        valid= True
        newops.append(remplacements[key])
        break
    if valid == False:
      newops.append(op)
  res=1
  mul=1
  for op in newops:
    try:
      mul = float(op)
    except:
      mul =1
      
    res *= mul
  return int(res)

def getURL(styleimage:str):
  elements = styleimage.split('"')
  return elements[1]

def wilayaFromCommune(commune:str):
  for x in dz_data:
    if (x["commune"].lower() == commune.lower()):
      return x["wilaya"]