# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: monitoring.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10monitoring.proto\x12\x1d\x65vent_store.client.monitoring\"C\n\x08StatsReq\x12\x14\n\x0cuse_metadata\x18\x01 \x01(\x08\x12!\n\x19refresh_time_period_in_ms\x18\x04 \x01(\x04\"}\n\tStatsResp\x12\x42\n\x05stats\x18\x01 \x03(\x0b\x32\x33.event_store.client.monitoring.StatsResp.StatsEntry\x1a,\n\nStatsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x32j\n\nMonitoring\x12\\\n\x05Stats\x12\'.event_store.client.monitoring.StatsReq\x1a(.event_store.client.monitoring.StatsResp0\x01\x42*\n(com.eventstore.dbclient.proto.monitoringb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'monitoring_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n(com.eventstore.dbclient.proto.monitoring'
  _globals['_STATSRESP_STATSENTRY']._options = None
  _globals['_STATSRESP_STATSENTRY']._serialized_options = b'8\001'
  _globals['_STATSREQ']._serialized_start=51
  _globals['_STATSREQ']._serialized_end=118
  _globals['_STATSRESP']._serialized_start=120
  _globals['_STATSRESP']._serialized_end=245
  _globals['_STATSRESP_STATSENTRY']._serialized_start=201
  _globals['_STATSRESP_STATSENTRY']._serialized_end=245
  _globals['_MONITORING']._serialized_start=247
  _globals['_MONITORING']._serialized_end=353
# @@protoc_insertion_point(module_scope)
