SerializationOfClassesAndFuncs
A library for that help you to serialize functions, classes, objects etc.

Installation
pip install SerializationOfClassesAndFuncs
Get started


from SerializationOfClassesAndFuncs import SerializersFactory, SerializerType

s = SerializersFactory.create_serializer(SerializerType.XML)

with open("data_file.xml", "w") as file:
    s.dump(T.tst4, file)
    
with open("data_file.xml", "r") as file:
    a = s.load(file)
	
