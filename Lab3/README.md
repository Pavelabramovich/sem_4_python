SerializationOfClassesAndFuncs
A library for that help you to serialize functions, classes, objects etc.

Installation
pip install SerializationOfClassesAndFuncs
Get started


from SerializationOfClassesAndFuncs import SerializersFactory
from someclass import SomeClass

obj1 = SomeClass()

s = SerializersFactory.create_serializer("xml")

with open("data_file.xml", "w") as file:
    s.dump(obj, file)
    
with open("data_file.xml", "r") as file:
    obj2 = s.load(file)
	
