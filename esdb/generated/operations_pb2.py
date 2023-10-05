# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: operations.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import shared_pb2 as shared__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10operations.proto\x12\x1d\x65vent_store.client.operations\x1a\x0cshared.proto\"\x97\x01\n\x10StartScavengeReq\x12H\n\x07options\x18\x01 \x01(\x0b\x32\x37.event_store.client.operations.StartScavengeReq.Options\x1a\x39\n\x07Options\x12\x14\n\x0cthread_count\x18\x01 \x01(\x05\x12\x18\n\x10start_from_chunk\x18\x02 \x01(\x05\"z\n\x0fStopScavengeReq\x12G\n\x07options\x18\x01 \x01(\x0b\x32\x36.event_store.client.operations.StopScavengeReq.Options\x1a\x1e\n\x07Options\x12\x13\n\x0bscavenge_id\x18\x01 \x01(\t\"\xb4\x01\n\x0cScavengeResp\x12\x13\n\x0bscavenge_id\x18\x01 \x01(\t\x12S\n\x0fscavenge_result\x18\x02 \x01(\x0e\x32:.event_store.client.operations.ScavengeResp.ScavengeResult\":\n\x0eScavengeResult\x12\x0b\n\x07Started\x10\x00\x12\x0e\n\nInProgress\x10\x01\x12\x0b\n\x07Stopped\x10\x02\"&\n\x12SetNodePriorityReq\x12\x10\n\x08priority\x18\x01 \x01(\x05\x32\xed\x04\n\nOperations\x12m\n\rStartScavenge\x12/.event_store.client.operations.StartScavengeReq\x1a+.event_store.client.operations.ScavengeResp\x12k\n\x0cStopScavenge\x12..event_store.client.operations.StopScavengeReq\x1a+.event_store.client.operations.ScavengeResp\x12@\n\x08Shutdown\x12\x19.event_store.client.Empty\x1a\x19.event_store.client.Empty\x12\x44\n\x0cMergeIndexes\x12\x19.event_store.client.Empty\x1a\x19.event_store.client.Empty\x12\x42\n\nResignNode\x12\x19.event_store.client.Empty\x1a\x19.event_store.client.Empty\x12_\n\x0fSetNodePriority\x12\x31.event_store.client.operations.SetNodePriorityReq\x1a\x19.event_store.client.Empty\x12V\n\x1eRestartPersistentSubscriptions\x12\x19.event_store.client.Empty\x1a\x19.event_store.client.EmptyB*\n(com.eventstore.dbclient.proto.operationsb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'operations_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n(com.eventstore.dbclient.proto.operations'
  _globals['_STARTSCAVENGEREQ']._serialized_start=66
  _globals['_STARTSCAVENGEREQ']._serialized_end=217
  _globals['_STARTSCAVENGEREQ_OPTIONS']._serialized_start=160
  _globals['_STARTSCAVENGEREQ_OPTIONS']._serialized_end=217
  _globals['_STOPSCAVENGEREQ']._serialized_start=219
  _globals['_STOPSCAVENGEREQ']._serialized_end=341
  _globals['_STOPSCAVENGEREQ_OPTIONS']._serialized_start=311
  _globals['_STOPSCAVENGEREQ_OPTIONS']._serialized_end=341
  _globals['_SCAVENGERESP']._serialized_start=344
  _globals['_SCAVENGERESP']._serialized_end=524
  _globals['_SCAVENGERESP_SCAVENGERESULT']._serialized_start=466
  _globals['_SCAVENGERESP_SCAVENGERESULT']._serialized_end=524
  _globals['_SETNODEPRIORITYREQ']._serialized_start=526
  _globals['_SETNODEPRIORITYREQ']._serialized_end=564
  _globals['_OPERATIONS']._serialized_start=567
  _globals['_OPERATIONS']._serialized_end=1188
# @@protoc_insertion_point(module_scope)
