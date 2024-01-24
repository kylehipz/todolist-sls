from boto3.dynamodb.types import TypeDeserializer, TypeSerializer

srl = TypeSerializer()
dsrl = TypeDeserializer()


def serialize(obj):
    return {k: srl.serialize(v) for k, v in obj.items()}


def deserialize(obj):
    return {k: dsrl.deserialize(v) for k, v in obj.items()}


__all__ = ["serialize", "deserialize"]
