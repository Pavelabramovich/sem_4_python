from SerializationOfClassesAndFuncs.serializers_factory import SerializersFactory, SerializerType
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Serialization from file to file')
    parser.add_argument('file_from', type=str, help='Input filepath for file_from')
    parser.add_argument('file_to', type=str, help='Input filepath for file_to')
    parser.add_argument('format_from', type=str, help='Input format_from')
    parser.add_argument('format_to', type=str, help='Input format_to')
    args = parser.parse_args()

    file_from = args.file_from
    file_to = args.file_to

    format_from = args.format_from
    format_to = args.format_to

    format_from = SerializersFactory.create_serializer(SerializerType.XML if format_from == "xml" else SerializerType.JSON)
    format_to = SerializersFactory.create_serializer(SerializerType.XML if format_to == "xml" else SerializerType.JSON)

    with open(file_from, "r") as file:
        obj = format_from.load(file)

    with open(file_to, "w") as file:
        format_to.dump(obj, file)
