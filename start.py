import xml.etree.ElementTree as Xet 
import pandas as pd 

cols = ["name","id","ref","ref_name","ref_type","asm"]
# name - nazwa użyta z sufixem :kolejne_wystapienie
# id - id użycia
# ref - id referencji (źródła) 1:n (n użyć)
# ref_name - nazwa referncji
# ref_type - typ referencji (solid, assembly)
# asm - id assembly (tu trzeba będzie obrócić bo to asm mają listę części a mi trzeba )
rows = []

#parsing xml
xmlparse = Xet.parse('test.xml')
root = xmlparse.getroot()
#print(root)
maszyna = xmlparse.find('{http://www.plmxml.org/Schemas/PLMXMLSchema}ProductDef/{http://www.plmxml.org/Schemas/PLMXMLSchema}InstanceGraph')
#print(maszyna)
print("\n")
skladowe = list(maszyna.findall('{http://www.plmxml.org/Schemas/PLMXMLSchema}Instance'))
referencje = list(maszyna.findall('{http://www.plmxml.org/Schemas/PLMXMLSchema}ProductRevisionView'))
print(referencje)
for i in skladowe: 
    name=i.attrib["name"]
    id=i.attrib["id"]
    ref=i.attrib["partRef"]
    for x in referencje:
        ref_name = "x"
        ref_type = "x"
        asm = "x"
        if x.attrib["id"] == ref[1:]:
            ref_name = x.attrib["name"]
            ref_type = x.attrib["type"]
            if ref_type == "assembly":
                asm = x.attrib["instanceRefs"]
    rows.append({"name": name,
                  "id": id,
                  "ref": ref[1:],
                  "ref_name": ref_name,
                  "ref_type": ref_type,
                  "asm": asm
                  })
    
df = pd.DataFrame(rows)
df.to_csv('output.csv')