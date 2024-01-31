import xml.etree.ElementTree as Xet 
import pandas as pd 

cols = ["name","id","parent"]
rows = []

#parsing xml
xmlparse = Xet.parse('test.xml')
root = xmlparse.getroot()
#print(root)
maszyna = xmlparse.find('{http://www.plmxml.org/Schemas/PLMXMLSchema}ProductDef/{http://www.plmxml.org/Schemas/PLMXMLSchema}InstanceGraph')
print(maszyna)
print("\n")
skladowe = list(maszyna.findall('{http://www.plmxml.org/Schemas/PLMXMLSchema}Instance'))
print(skladowe)
for i in skladowe: 
    name=i.attrib["name"]
    id=i.attrib["id"]
    parent=i.attrib[""]
    rows.append({"name": name,
                 "id": id,
                 "parent": parent})
    
#df = pd.DataFrame(rows, colums=cols)
#df.to_csv('output.csv')