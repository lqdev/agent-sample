# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: messages.proto
# Protobuf Python Version: 6.31.0-rc1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    6,
    31,
    0,
    '-rc1',
    'messages.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0emessages.proto\x12\x0bHelloAgents\"2\n\x0bTextMessage\x12\x13\n\x0btextMessage\x18\x01 \x01(\t\x12\x0e\n\x06source\x18\x02 \x01(\t\"\x18\n\x05Input\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x1f\n\x0eInputProcessed\x12\r\n\x05route\x18\x01 \x01(\t\"\x19\n\x06Output\x12\x0f\n\x07message\x18\x01 \x01(\t\"\x1e\n\rOutputWritten\x12\r\n\x05route\x18\x01 \x01(\t\"\x1a\n\x07IOError\x12\x0f\n\x07message\x18\x01 \x01(\t\"%\n\x12NewMessageReceived\x12\x0f\n\x07message\x18\x01 \x01(\t\"%\n\x11ResponseGenerated\x12\x10\n\x08response\x18\x01 \x01(\t\"\x1a\n\x07GoodBye\x12\x0f\n\x07message\x18\x01 \x01(\t\" \n\rMessageStored\x12\x0f\n\x07message\x18\x01 \x01(\t\";\n\x12\x43onversationClosed\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\x14\n\x0cuser_message\x18\x02 \x01(\t\"\x1b\n\x08Shutdown\x12\x0f\n\x07message\x18\x01 \x01(\tB\x1e\xaa\x02\x1bMicrosoft.AutoGen.Contractsb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'messages_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\252\002\033Microsoft.AutoGen.Contracts'
  _globals['_TEXTMESSAGE']._serialized_start=31
  _globals['_TEXTMESSAGE']._serialized_end=81
  _globals['_INPUT']._serialized_start=83
  _globals['_INPUT']._serialized_end=107
  _globals['_INPUTPROCESSED']._serialized_start=109
  _globals['_INPUTPROCESSED']._serialized_end=140
  _globals['_OUTPUT']._serialized_start=142
  _globals['_OUTPUT']._serialized_end=167
  _globals['_OUTPUTWRITTEN']._serialized_start=169
  _globals['_OUTPUTWRITTEN']._serialized_end=199
  _globals['_IOERROR']._serialized_start=201
  _globals['_IOERROR']._serialized_end=227
  _globals['_NEWMESSAGERECEIVED']._serialized_start=229
  _globals['_NEWMESSAGERECEIVED']._serialized_end=266
  _globals['_RESPONSEGENERATED']._serialized_start=268
  _globals['_RESPONSEGENERATED']._serialized_end=305
  _globals['_GOODBYE']._serialized_start=307
  _globals['_GOODBYE']._serialized_end=333
  _globals['_MESSAGESTORED']._serialized_start=335
  _globals['_MESSAGESTORED']._serialized_end=367
  _globals['_CONVERSATIONCLOSED']._serialized_start=369
  _globals['_CONVERSATIONCLOSED']._serialized_end=428
  _globals['_SHUTDOWN']._serialized_start=430
  _globals['_SHUTDOWN']._serialized_end=457
# @@protoc_insertion_point(module_scope)
