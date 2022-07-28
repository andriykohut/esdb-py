# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: streams.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import shared_pb2 as shared__pb2
from . import status_pb2 as status__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rstreams.proto\x12\x1a\x65vent_store.client.streams\x1a\x0cshared.proto\x1a\x0cstatus.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xad\x0e\n\x07ReadReq\x12<\n\x07options\x18\x01 \x01(\x0b\x32+.event_store.client.streams.ReadReq.Options\x1a\xe3\r\n\x07Options\x12K\n\x06stream\x18\x01 \x01(\x0b\x32\x39.event_store.client.streams.ReadReq.Options.StreamOptionsH\x00\x12\x45\n\x03\x61ll\x18\x02 \x01(\x0b\x32\x36.event_store.client.streams.ReadReq.Options.AllOptionsH\x00\x12Q\n\x0eread_direction\x18\x03 \x01(\x0e\x32\x39.event_store.client.streams.ReadReq.Options.ReadDirection\x12\x15\n\rresolve_links\x18\x04 \x01(\x08\x12\x0f\n\x05\x63ount\x18\x05 \x01(\x04H\x01\x12W\n\x0csubscription\x18\x06 \x01(\x0b\x32?.event_store.client.streams.ReadReq.Options.SubscriptionOptionsH\x01\x12K\n\x06\x66ilter\x18\x07 \x01(\x0b\x32\x39.event_store.client.streams.ReadReq.Options.FilterOptionsH\x02\x12.\n\tno_filter\x18\x08 \x01(\x0b\x32\x19.event_store.client.EmptyH\x02\x12K\n\x0buuid_option\x18\t \x01(\x0b\x32\x36.event_store.client.streams.ReadReq.Options.UUIDOption\x12Q\n\x0e\x63ontrol_option\x18\n \x01(\x0b\x32\x39.event_store.client.streams.ReadReq.Options.ControlOption\x1a\xcd\x01\n\rStreamOptions\x12?\n\x11stream_identifier\x18\x01 \x01(\x0b\x32$.event_store.client.StreamIdentifier\x12\x12\n\x08revision\x18\x02 \x01(\x04H\x00\x12*\n\x05start\x18\x03 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x12(\n\x03\x65nd\x18\x04 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x42\x11\n\x0frevision_option\x1a\xba\x01\n\nAllOptions\x12H\n\x08position\x18\x01 \x01(\x0b\x32\x34.event_store.client.streams.ReadReq.Options.PositionH\x00\x12*\n\x05start\x18\x02 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x12(\n\x03\x65nd\x18\x03 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x42\x0c\n\nall_option\x1a\x15\n\x13SubscriptionOptions\x1a=\n\x08Position\x12\x17\n\x0f\x63ommit_position\x18\x01 \x01(\x04\x12\x18\n\x10prepare_position\x18\x02 \x01(\x04\x1a\xf0\x02\n\rFilterOptions\x12\x61\n\x11stream_identifier\x18\x01 \x01(\x0b\x32\x44.event_store.client.streams.ReadReq.Options.FilterOptions.ExpressionH\x00\x12Z\n\nevent_type\x18\x02 \x01(\x0b\x32\x44.event_store.client.streams.ReadReq.Options.FilterOptions.ExpressionH\x00\x12\r\n\x03max\x18\x03 \x01(\rH\x01\x12*\n\x05\x63ount\x18\x04 \x01(\x0b\x32\x19.event_store.client.EmptyH\x01\x12$\n\x1c\x63heckpointIntervalMultiplier\x18\x05 \x01(\r\x1a+\n\nExpression\x12\r\n\x05regex\x18\x01 \x01(\t\x12\x0e\n\x06prefix\x18\x02 \x03(\tB\x08\n\x06\x66ilterB\x08\n\x06window\x1au\n\nUUIDOption\x12/\n\nstructured\x18\x01 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x12+\n\x06string\x18\x02 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x42\t\n\x07\x63ontent\x1a&\n\rControlOption\x12\x15\n\rcompatibility\x18\x01 \x01(\r\",\n\rReadDirection\x12\x0c\n\x08\x46orwards\x10\x00\x12\r\n\tBackwards\x10\x01\x42\x0f\n\rstream_optionB\x0e\n\x0c\x63ount_optionB\x0f\n\rfilter_option\"\x95\n\n\x08ReadResp\x12?\n\x05\x65vent\x18\x01 \x01(\x0b\x32..event_store.client.streams.ReadResp.ReadEventH\x00\x12U\n\x0c\x63onfirmation\x18\x02 \x01(\x0b\x32=.event_store.client.streams.ReadResp.SubscriptionConfirmationH\x00\x12\x45\n\ncheckpoint\x18\x03 \x01(\x0b\x32/.event_store.client.streams.ReadResp.CheckpointH\x00\x12O\n\x10stream_not_found\x18\x04 \x01(\x0b\x32\x33.event_store.client.streams.ReadResp.StreamNotFoundH\x00\x12\x1f\n\x15\x66irst_stream_position\x18\x05 \x01(\x04H\x00\x12\x1e\n\x14last_stream_position\x18\x06 \x01(\x04H\x00\x12I\n\x18last_all_stream_position\x18\x07 \x01(\x0b\x32%.event_store.client.AllStreamPositionH\x00\x1a\xf8\x04\n\tReadEvent\x12K\n\x05\x65vent\x18\x01 \x01(\x0b\x32<.event_store.client.streams.ReadResp.ReadEvent.RecordedEvent\x12J\n\x04link\x18\x02 \x01(\x0b\x32<.event_store.client.streams.ReadResp.ReadEvent.RecordedEvent\x12\x19\n\x0f\x63ommit_position\x18\x03 \x01(\x04H\x00\x12\x30\n\x0bno_position\x18\x04 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x1a\xf8\x02\n\rRecordedEvent\x12$\n\x02id\x18\x01 \x01(\x0b\x32\x18.event_store.client.UUID\x12?\n\x11stream_identifier\x18\x02 \x01(\x0b\x32$.event_store.client.StreamIdentifier\x12\x17\n\x0fstream_revision\x18\x03 \x01(\x04\x12\x18\n\x10prepare_position\x18\x04 \x01(\x04\x12\x17\n\x0f\x63ommit_position\x18\x05 \x01(\x04\x12\\\n\x08metadata\x18\x06 \x03(\x0b\x32J.event_store.client.streams.ReadResp.ReadEvent.RecordedEvent.MetadataEntry\x12\x17\n\x0f\x63ustom_metadata\x18\x07 \x01(\x0c\x12\x0c\n\x04\x64\x61ta\x18\x08 \x01(\x0c\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42\n\n\x08position\x1a\x33\n\x18SubscriptionConfirmation\x12\x17\n\x0fsubscription_id\x18\x01 \x01(\t\x1a?\n\nCheckpoint\x12\x17\n\x0f\x63ommit_position\x18\x01 \x01(\x04\x12\x18\n\x10prepare_position\x18\x02 \x01(\x04\x1aQ\n\x0eStreamNotFound\x12?\n\x11stream_identifier\x18\x01 \x01(\x0b\x32$.event_store.client.StreamIdentifierB\t\n\x07\x63ontent\"\x9f\x05\n\tAppendReq\x12@\n\x07options\x18\x01 \x01(\x0b\x32-.event_store.client.streams.AppendReq.OptionsH\x00\x12Q\n\x10proposed_message\x18\x02 \x01(\x0b\x32\x35.event_store.client.streams.AppendReq.ProposedMessageH\x00\x1a\x88\x02\n\x07Options\x12?\n\x11stream_identifier\x18\x01 \x01(\x0b\x32$.event_store.client.StreamIdentifier\x12\x12\n\x08revision\x18\x02 \x01(\x04H\x00\x12.\n\tno_stream\x18\x03 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x12(\n\x03\x61ny\x18\x04 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x12\x32\n\rstream_exists\x18\x05 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x42\x1a\n\x18\x65xpected_stream_revision\x1a\xe6\x01\n\x0fProposedMessage\x12$\n\x02id\x18\x01 \x01(\x0b\x32\x18.event_store.client.UUID\x12U\n\x08metadata\x18\x02 \x03(\x0b\x32\x43.event_store.client.streams.AppendReq.ProposedMessage.MetadataEntry\x12\x17\n\x0f\x63ustom_metadata\x18\x03 \x01(\x0c\x12\x0c\n\x04\x64\x61ta\x18\x04 \x01(\x0c\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42\t\n\x07\x63ontent\"\x8d\t\n\nAppendResp\x12\x41\n\x07success\x18\x01 \x01(\x0b\x32..event_store.client.streams.AppendResp.SuccessH\x00\x12]\n\x16wrong_expected_version\x18\x02 \x01(\x0b\x32;.event_store.client.streams.AppendResp.WrongExpectedVersionH\x00\x1a=\n\x08Position\x12\x17\n\x0f\x63ommit_position\x18\x01 \x01(\x04\x12\x18\n\x10prepare_position\x18\x02 \x01(\x04\x1a\xfa\x01\n\x07Success\x12\x1a\n\x10\x63urrent_revision\x18\x01 \x01(\x04H\x00\x12.\n\tno_stream\x18\x02 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x12\x43\n\x08position\x18\x03 \x01(\x0b\x32/.event_store.client.streams.AppendResp.PositionH\x01\x12\x30\n\x0bno_position\x18\x04 \x01(\x0b\x32\x19.event_store.client.EmptyH\x01\x42\x19\n\x17\x63urrent_revision_optionB\x11\n\x0fposition_option\x1a\x96\x05\n\x14WrongExpectedVersion\x12!\n\x17\x63urrent_revision_20_6_0\x18\x01 \x01(\x04H\x00\x12\x35\n\x10no_stream_20_6_0\x18\x02 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x12\"\n\x18\x65xpected_revision_20_6_0\x18\x03 \x01(\x04H\x01\x12/\n\nany_20_6_0\x18\x04 \x01(\x0b\x32\x19.event_store.client.EmptyH\x01\x12\x39\n\x14stream_exists_20_6_0\x18\x05 \x01(\x0b\x32\x19.event_store.client.EmptyH\x01\x12\x1a\n\x10\x63urrent_revision\x18\x06 \x01(\x04H\x02\x12\x36\n\x11\x63urrent_no_stream\x18\x07 \x01(\x0b\x32\x19.event_store.client.EmptyH\x02\x12\x1b\n\x11\x65xpected_revision\x18\x08 \x01(\x04H\x03\x12\x31\n\x0c\x65xpected_any\x18\t \x01(\x0b\x32\x19.event_store.client.EmptyH\x03\x12;\n\x16\x65xpected_stream_exists\x18\n \x01(\x0b\x32\x19.event_store.client.EmptyH\x03\x12\x37\n\x12\x65xpected_no_stream\x18\x0b \x01(\x0b\x32\x19.event_store.client.EmptyH\x03\x42 \n\x1e\x63urrent_revision_option_20_6_0B!\n\x1f\x65xpected_revision_option_20_6_0B\x19\n\x17\x63urrent_revision_optionB\x1a\n\x18\x65xpected_revision_optionB\x08\n\x06result\"\xe1\x06\n\x0e\x42\x61tchAppendReq\x12\x30\n\x0e\x63orrelation_id\x18\x01 \x01(\x0b\x32\x18.event_store.client.UUID\x12\x43\n\x07options\x18\x02 \x01(\x0b\x32\x32.event_store.client.streams.BatchAppendReq.Options\x12U\n\x11proposed_messages\x18\x03 \x03(\x0b\x32:.event_store.client.streams.BatchAppendReq.ProposedMessage\x12\x10\n\x08is_final\x18\x04 \x01(\x08\x1a\x80\x03\n\x07Options\x12?\n\x11stream_identifier\x18\x01 \x01(\x0b\x32$.event_store.client.StreamIdentifier\x12\x19\n\x0fstream_position\x18\x02 \x01(\x04H\x00\x12+\n\tno_stream\x18\x03 \x01(\x0b\x32\x16.google.protobuf.EmptyH\x00\x12%\n\x03\x61ny\x18\x04 \x01(\x0b\x32\x16.google.protobuf.EmptyH\x00\x12/\n\rstream_exists\x18\x05 \x01(\x0b\x32\x16.google.protobuf.EmptyH\x00\x12\x36\n\x10\x64\x65\x61\x64line_21_10_0\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x01\x12-\n\x08\x64\x65\x61\x64line\x18\x07 \x01(\x0b\x32\x19.google.protobuf.DurationH\x01\x42\x1a\n\x18\x65xpected_stream_positionB\x11\n\x0f\x64\x65\x61\x64line_option\x1a\xeb\x01\n\x0fProposedMessage\x12$\n\x02id\x18\x01 \x01(\x0b\x32\x18.event_store.client.UUID\x12Z\n\x08metadata\x18\x02 \x03(\x0b\x32H.event_store.client.streams.BatchAppendReq.ProposedMessage.MetadataEntry\x12\x17\n\x0f\x63ustom_metadata\x18\x03 \x01(\x0c\x12\x0c\n\x04\x64\x61ta\x18\x04 \x01(\x0c\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xa4\x05\n\x0f\x42\x61tchAppendResp\x12\x30\n\x0e\x63orrelation_id\x18\x01 \x01(\x0b\x32\x18.event_store.client.UUID\x12#\n\x05\x65rror\x18\x02 \x01(\x0b\x32\x12.google.rpc.StatusH\x00\x12\x46\n\x07success\x18\x03 \x01(\x0b\x32\x33.event_store.client.streams.BatchAppendResp.SuccessH\x00\x12?\n\x11stream_identifier\x18\x04 \x01(\x0b\x32$.event_store.client.StreamIdentifier\x12\x19\n\x0fstream_position\x18\x05 \x01(\x04H\x01\x12+\n\tno_stream\x18\x06 \x01(\x0b\x32\x16.google.protobuf.EmptyH\x01\x12%\n\x03\x61ny\x18\x07 \x01(\x0b\x32\x16.google.protobuf.EmptyH\x01\x12/\n\rstream_exists\x18\x08 \x01(\x0b\x32\x16.google.protobuf.EmptyH\x01\x1a\xea\x01\n\x07Success\x12\x1a\n\x10\x63urrent_revision\x18\x01 \x01(\x04H\x00\x12+\n\tno_stream\x18\x02 \x01(\x0b\x32\x16.google.protobuf.EmptyH\x00\x12\x39\n\x08position\x18\x03 \x01(\x0b\x32%.event_store.client.AllStreamPositionH\x01\x12-\n\x0bno_position\x18\x04 \x01(\x0b\x32\x16.google.protobuf.EmptyH\x01\x42\x19\n\x17\x63urrent_revision_optionB\x11\n\x0fposition_optionB\x08\n\x06resultB\x1a\n\x18\x65xpected_stream_position\"\xd6\x02\n\tDeleteReq\x12>\n\x07options\x18\x01 \x01(\x0b\x32-.event_store.client.streams.DeleteReq.Options\x1a\x88\x02\n\x07Options\x12?\n\x11stream_identifier\x18\x01 \x01(\x0b\x32$.event_store.client.StreamIdentifier\x12\x12\n\x08revision\x18\x02 \x01(\x04H\x00\x12.\n\tno_stream\x18\x03 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x12(\n\x03\x61ny\x18\x04 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x12\x32\n\rstream_exists\x18\x05 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x42\x1a\n\x18\x65xpected_stream_revision\"\xd5\x01\n\nDeleteResp\x12\x43\n\x08position\x18\x01 \x01(\x0b\x32/.event_store.client.streams.DeleteResp.PositionH\x00\x12\x30\n\x0bno_position\x18\x02 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x1a=\n\x08Position\x12\x17\n\x0f\x63ommit_position\x18\x01 \x01(\x04\x12\x18\n\x10prepare_position\x18\x02 \x01(\x04\x42\x11\n\x0fposition_option\"\xdc\x02\n\x0cTombstoneReq\x12\x41\n\x07options\x18\x01 \x01(\x0b\x32\x30.event_store.client.streams.TombstoneReq.Options\x1a\x88\x02\n\x07Options\x12?\n\x11stream_identifier\x18\x01 \x01(\x0b\x32$.event_store.client.StreamIdentifier\x12\x12\n\x08revision\x18\x02 \x01(\x04H\x00\x12.\n\tno_stream\x18\x03 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x12(\n\x03\x61ny\x18\x04 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x12\x32\n\rstream_exists\x18\x05 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x42\x1a\n\x18\x65xpected_stream_revision\"\xdb\x01\n\rTombstoneResp\x12\x46\n\x08position\x18\x01 \x01(\x0b\x32\x32.event_store.client.streams.TombstoneResp.PositionH\x00\x12\x30\n\x0bno_position\x18\x02 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x1a=\n\x08Position\x12\x17\n\x0f\x63ommit_position\x18\x01 \x01(\x04\x12\x18\n\x10prepare_position\x18\x02 \x01(\x04\x42\x11\n\x0fposition_option2\xe0\x03\n\x07Streams\x12S\n\x04Read\x12#.event_store.client.streams.ReadReq\x1a$.event_store.client.streams.ReadResp0\x01\x12Y\n\x06\x41ppend\x12%.event_store.client.streams.AppendReq\x1a&.event_store.client.streams.AppendResp(\x01\x12W\n\x06\x44\x65lete\x12%.event_store.client.streams.DeleteReq\x1a&.event_store.client.streams.DeleteResp\x12`\n\tTombstone\x12(.event_store.client.streams.TombstoneReq\x1a).event_store.client.streams.TombstoneResp\x12j\n\x0b\x42\x61tchAppend\x12*.event_store.client.streams.BatchAppendReq\x1a+.event_store.client.streams.BatchAppendResp(\x01\x30\x01\x42\'\n%com.eventstore.dbclient.proto.streamsb\x06proto3')



_READREQ = DESCRIPTOR.message_types_by_name['ReadReq']
_READREQ_OPTIONS = _READREQ.nested_types_by_name['Options']
_READREQ_OPTIONS_STREAMOPTIONS = _READREQ_OPTIONS.nested_types_by_name['StreamOptions']
_READREQ_OPTIONS_ALLOPTIONS = _READREQ_OPTIONS.nested_types_by_name['AllOptions']
_READREQ_OPTIONS_SUBSCRIPTIONOPTIONS = _READREQ_OPTIONS.nested_types_by_name['SubscriptionOptions']
_READREQ_OPTIONS_POSITION = _READREQ_OPTIONS.nested_types_by_name['Position']
_READREQ_OPTIONS_FILTEROPTIONS = _READREQ_OPTIONS.nested_types_by_name['FilterOptions']
_READREQ_OPTIONS_FILTEROPTIONS_EXPRESSION = _READREQ_OPTIONS_FILTEROPTIONS.nested_types_by_name['Expression']
_READREQ_OPTIONS_UUIDOPTION = _READREQ_OPTIONS.nested_types_by_name['UUIDOption']
_READREQ_OPTIONS_CONTROLOPTION = _READREQ_OPTIONS.nested_types_by_name['ControlOption']
_READRESP = DESCRIPTOR.message_types_by_name['ReadResp']
_READRESP_READEVENT = _READRESP.nested_types_by_name['ReadEvent']
_READRESP_READEVENT_RECORDEDEVENT = _READRESP_READEVENT.nested_types_by_name['RecordedEvent']
_READRESP_READEVENT_RECORDEDEVENT_METADATAENTRY = _READRESP_READEVENT_RECORDEDEVENT.nested_types_by_name['MetadataEntry']
_READRESP_SUBSCRIPTIONCONFIRMATION = _READRESP.nested_types_by_name['SubscriptionConfirmation']
_READRESP_CHECKPOINT = _READRESP.nested_types_by_name['Checkpoint']
_READRESP_STREAMNOTFOUND = _READRESP.nested_types_by_name['StreamNotFound']
_APPENDREQ = DESCRIPTOR.message_types_by_name['AppendReq']
_APPENDREQ_OPTIONS = _APPENDREQ.nested_types_by_name['Options']
_APPENDREQ_PROPOSEDMESSAGE = _APPENDREQ.nested_types_by_name['ProposedMessage']
_APPENDREQ_PROPOSEDMESSAGE_METADATAENTRY = _APPENDREQ_PROPOSEDMESSAGE.nested_types_by_name['MetadataEntry']
_APPENDRESP = DESCRIPTOR.message_types_by_name['AppendResp']
_APPENDRESP_POSITION = _APPENDRESP.nested_types_by_name['Position']
_APPENDRESP_SUCCESS = _APPENDRESP.nested_types_by_name['Success']
_APPENDRESP_WRONGEXPECTEDVERSION = _APPENDRESP.nested_types_by_name['WrongExpectedVersion']
_BATCHAPPENDREQ = DESCRIPTOR.message_types_by_name['BatchAppendReq']
_BATCHAPPENDREQ_OPTIONS = _BATCHAPPENDREQ.nested_types_by_name['Options']
_BATCHAPPENDREQ_PROPOSEDMESSAGE = _BATCHAPPENDREQ.nested_types_by_name['ProposedMessage']
_BATCHAPPENDREQ_PROPOSEDMESSAGE_METADATAENTRY = _BATCHAPPENDREQ_PROPOSEDMESSAGE.nested_types_by_name['MetadataEntry']
_BATCHAPPENDRESP = DESCRIPTOR.message_types_by_name['BatchAppendResp']
_BATCHAPPENDRESP_SUCCESS = _BATCHAPPENDRESP.nested_types_by_name['Success']
_DELETEREQ = DESCRIPTOR.message_types_by_name['DeleteReq']
_DELETEREQ_OPTIONS = _DELETEREQ.nested_types_by_name['Options']
_DELETERESP = DESCRIPTOR.message_types_by_name['DeleteResp']
_DELETERESP_POSITION = _DELETERESP.nested_types_by_name['Position']
_TOMBSTONEREQ = DESCRIPTOR.message_types_by_name['TombstoneReq']
_TOMBSTONEREQ_OPTIONS = _TOMBSTONEREQ.nested_types_by_name['Options']
_TOMBSTONERESP = DESCRIPTOR.message_types_by_name['TombstoneResp']
_TOMBSTONERESP_POSITION = _TOMBSTONERESP.nested_types_by_name['Position']
_READREQ_OPTIONS_READDIRECTION = _READREQ_OPTIONS.enum_types_by_name['ReadDirection']
ReadReq = _reflection.GeneratedProtocolMessageType('ReadReq', (_message.Message,), {

  'Options' : _reflection.GeneratedProtocolMessageType('Options', (_message.Message,), {

    'StreamOptions' : _reflection.GeneratedProtocolMessageType('StreamOptions', (_message.Message,), {
      'DESCRIPTOR' : _READREQ_OPTIONS_STREAMOPTIONS,
      '__module__' : 'streams_pb2'
      # @@protoc_insertion_point(class_scope:event_store.client.streams.ReadReq.Options.StreamOptions)
      })
    ,

    'AllOptions' : _reflection.GeneratedProtocolMessageType('AllOptions', (_message.Message,), {
      'DESCRIPTOR' : _READREQ_OPTIONS_ALLOPTIONS,
      '__module__' : 'streams_pb2'
      # @@protoc_insertion_point(class_scope:event_store.client.streams.ReadReq.Options.AllOptions)
      })
    ,

    'SubscriptionOptions' : _reflection.GeneratedProtocolMessageType('SubscriptionOptions', (_message.Message,), {
      'DESCRIPTOR' : _READREQ_OPTIONS_SUBSCRIPTIONOPTIONS,
      '__module__' : 'streams_pb2'
      # @@protoc_insertion_point(class_scope:event_store.client.streams.ReadReq.Options.SubscriptionOptions)
      })
    ,

    'Position' : _reflection.GeneratedProtocolMessageType('Position', (_message.Message,), {
      'DESCRIPTOR' : _READREQ_OPTIONS_POSITION,
      '__module__' : 'streams_pb2'
      # @@protoc_insertion_point(class_scope:event_store.client.streams.ReadReq.Options.Position)
      })
    ,

    'FilterOptions' : _reflection.GeneratedProtocolMessageType('FilterOptions', (_message.Message,), {

      'Expression' : _reflection.GeneratedProtocolMessageType('Expression', (_message.Message,), {
        'DESCRIPTOR' : _READREQ_OPTIONS_FILTEROPTIONS_EXPRESSION,
        '__module__' : 'streams_pb2'
        # @@protoc_insertion_point(class_scope:event_store.client.streams.ReadReq.Options.FilterOptions.Expression)
        })
      ,
      'DESCRIPTOR' : _READREQ_OPTIONS_FILTEROPTIONS,
      '__module__' : 'streams_pb2'
      # @@protoc_insertion_point(class_scope:event_store.client.streams.ReadReq.Options.FilterOptions)
      })
    ,

    'UUIDOption' : _reflection.GeneratedProtocolMessageType('UUIDOption', (_message.Message,), {
      'DESCRIPTOR' : _READREQ_OPTIONS_UUIDOPTION,
      '__module__' : 'streams_pb2'
      # @@protoc_insertion_point(class_scope:event_store.client.streams.ReadReq.Options.UUIDOption)
      })
    ,

    'ControlOption' : _reflection.GeneratedProtocolMessageType('ControlOption', (_message.Message,), {
      'DESCRIPTOR' : _READREQ_OPTIONS_CONTROLOPTION,
      '__module__' : 'streams_pb2'
      # @@protoc_insertion_point(class_scope:event_store.client.streams.ReadReq.Options.ControlOption)
      })
    ,
    'DESCRIPTOR' : _READREQ_OPTIONS,
    '__module__' : 'streams_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.streams.ReadReq.Options)
    })
  ,
  'DESCRIPTOR' : _READREQ,
  '__module__' : 'streams_pb2'
  # @@protoc_insertion_point(class_scope:event_store.client.streams.ReadReq)
  })
_sym_db.RegisterMessage(ReadReq)
_sym_db.RegisterMessage(ReadReq.Options)
_sym_db.RegisterMessage(ReadReq.Options.StreamOptions)
_sym_db.RegisterMessage(ReadReq.Options.AllOptions)
_sym_db.RegisterMessage(ReadReq.Options.SubscriptionOptions)
_sym_db.RegisterMessage(ReadReq.Options.Position)
_sym_db.RegisterMessage(ReadReq.Options.FilterOptions)
_sym_db.RegisterMessage(ReadReq.Options.FilterOptions.Expression)
_sym_db.RegisterMessage(ReadReq.Options.UUIDOption)
_sym_db.RegisterMessage(ReadReq.Options.ControlOption)

ReadResp = _reflection.GeneratedProtocolMessageType('ReadResp', (_message.Message,), {

  'ReadEvent' : _reflection.GeneratedProtocolMessageType('ReadEvent', (_message.Message,), {

    'RecordedEvent' : _reflection.GeneratedProtocolMessageType('RecordedEvent', (_message.Message,), {

      'MetadataEntry' : _reflection.GeneratedProtocolMessageType('MetadataEntry', (_message.Message,), {
        'DESCRIPTOR' : _READRESP_READEVENT_RECORDEDEVENT_METADATAENTRY,
        '__module__' : 'streams_pb2'
        # @@protoc_insertion_point(class_scope:event_store.client.streams.ReadResp.ReadEvent.RecordedEvent.MetadataEntry)
        })
      ,
      'DESCRIPTOR' : _READRESP_READEVENT_RECORDEDEVENT,
      '__module__' : 'streams_pb2'
      # @@protoc_insertion_point(class_scope:event_store.client.streams.ReadResp.ReadEvent.RecordedEvent)
      })
    ,
    'DESCRIPTOR' : _READRESP_READEVENT,
    '__module__' : 'streams_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.streams.ReadResp.ReadEvent)
    })
  ,

  'SubscriptionConfirmation' : _reflection.GeneratedProtocolMessageType('SubscriptionConfirmation', (_message.Message,), {
    'DESCRIPTOR' : _READRESP_SUBSCRIPTIONCONFIRMATION,
    '__module__' : 'streams_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.streams.ReadResp.SubscriptionConfirmation)
    })
  ,

  'Checkpoint' : _reflection.GeneratedProtocolMessageType('Checkpoint', (_message.Message,), {
    'DESCRIPTOR' : _READRESP_CHECKPOINT,
    '__module__' : 'streams_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.streams.ReadResp.Checkpoint)
    })
  ,

  'StreamNotFound' : _reflection.GeneratedProtocolMessageType('StreamNotFound', (_message.Message,), {
    'DESCRIPTOR' : _READRESP_STREAMNOTFOUND,
    '__module__' : 'streams_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.streams.ReadResp.StreamNotFound)
    })
  ,
  'DESCRIPTOR' : _READRESP,
  '__module__' : 'streams_pb2'
  # @@protoc_insertion_point(class_scope:event_store.client.streams.ReadResp)
  })
_sym_db.RegisterMessage(ReadResp)
_sym_db.RegisterMessage(ReadResp.ReadEvent)
_sym_db.RegisterMessage(ReadResp.ReadEvent.RecordedEvent)
_sym_db.RegisterMessage(ReadResp.ReadEvent.RecordedEvent.MetadataEntry)
_sym_db.RegisterMessage(ReadResp.SubscriptionConfirmation)
_sym_db.RegisterMessage(ReadResp.Checkpoint)
_sym_db.RegisterMessage(ReadResp.StreamNotFound)

AppendReq = _reflection.GeneratedProtocolMessageType('AppendReq', (_message.Message,), {

  'Options' : _reflection.GeneratedProtocolMessageType('Options', (_message.Message,), {
    'DESCRIPTOR' : _APPENDREQ_OPTIONS,
    '__module__' : 'streams_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.streams.AppendReq.Options)
    })
  ,

  'ProposedMessage' : _reflection.GeneratedProtocolMessageType('ProposedMessage', (_message.Message,), {

    'MetadataEntry' : _reflection.GeneratedProtocolMessageType('MetadataEntry', (_message.Message,), {
      'DESCRIPTOR' : _APPENDREQ_PROPOSEDMESSAGE_METADATAENTRY,
      '__module__' : 'streams_pb2'
      # @@protoc_insertion_point(class_scope:event_store.client.streams.AppendReq.ProposedMessage.MetadataEntry)
      })
    ,
    'DESCRIPTOR' : _APPENDREQ_PROPOSEDMESSAGE,
    '__module__' : 'streams_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.streams.AppendReq.ProposedMessage)
    })
  ,
  'DESCRIPTOR' : _APPENDREQ,
  '__module__' : 'streams_pb2'
  # @@protoc_insertion_point(class_scope:event_store.client.streams.AppendReq)
  })
_sym_db.RegisterMessage(AppendReq)
_sym_db.RegisterMessage(AppendReq.Options)
_sym_db.RegisterMessage(AppendReq.ProposedMessage)
_sym_db.RegisterMessage(AppendReq.ProposedMessage.MetadataEntry)

AppendResp = _reflection.GeneratedProtocolMessageType('AppendResp', (_message.Message,), {

  'Position' : _reflection.GeneratedProtocolMessageType('Position', (_message.Message,), {
    'DESCRIPTOR' : _APPENDRESP_POSITION,
    '__module__' : 'streams_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.streams.AppendResp.Position)
    })
  ,

  'Success' : _reflection.GeneratedProtocolMessageType('Success', (_message.Message,), {
    'DESCRIPTOR' : _APPENDRESP_SUCCESS,
    '__module__' : 'streams_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.streams.AppendResp.Success)
    })
  ,

  'WrongExpectedVersion' : _reflection.GeneratedProtocolMessageType('WrongExpectedVersion', (_message.Message,), {
    'DESCRIPTOR' : _APPENDRESP_WRONGEXPECTEDVERSION,
    '__module__' : 'streams_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.streams.AppendResp.WrongExpectedVersion)
    })
  ,
  'DESCRIPTOR' : _APPENDRESP,
  '__module__' : 'streams_pb2'
  # @@protoc_insertion_point(class_scope:event_store.client.streams.AppendResp)
  })
_sym_db.RegisterMessage(AppendResp)
_sym_db.RegisterMessage(AppendResp.Position)
_sym_db.RegisterMessage(AppendResp.Success)
_sym_db.RegisterMessage(AppendResp.WrongExpectedVersion)

BatchAppendReq = _reflection.GeneratedProtocolMessageType('BatchAppendReq', (_message.Message,), {

  'Options' : _reflection.GeneratedProtocolMessageType('Options', (_message.Message,), {
    'DESCRIPTOR' : _BATCHAPPENDREQ_OPTIONS,
    '__module__' : 'streams_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.streams.BatchAppendReq.Options)
    })
  ,

  'ProposedMessage' : _reflection.GeneratedProtocolMessageType('ProposedMessage', (_message.Message,), {

    'MetadataEntry' : _reflection.GeneratedProtocolMessageType('MetadataEntry', (_message.Message,), {
      'DESCRIPTOR' : _BATCHAPPENDREQ_PROPOSEDMESSAGE_METADATAENTRY,
      '__module__' : 'streams_pb2'
      # @@protoc_insertion_point(class_scope:event_store.client.streams.BatchAppendReq.ProposedMessage.MetadataEntry)
      })
    ,
    'DESCRIPTOR' : _BATCHAPPENDREQ_PROPOSEDMESSAGE,
    '__module__' : 'streams_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.streams.BatchAppendReq.ProposedMessage)
    })
  ,
  'DESCRIPTOR' : _BATCHAPPENDREQ,
  '__module__' : 'streams_pb2'
  # @@protoc_insertion_point(class_scope:event_store.client.streams.BatchAppendReq)
  })
_sym_db.RegisterMessage(BatchAppendReq)
_sym_db.RegisterMessage(BatchAppendReq.Options)
_sym_db.RegisterMessage(BatchAppendReq.ProposedMessage)
_sym_db.RegisterMessage(BatchAppendReq.ProposedMessage.MetadataEntry)

BatchAppendResp = _reflection.GeneratedProtocolMessageType('BatchAppendResp', (_message.Message,), {

  'Success' : _reflection.GeneratedProtocolMessageType('Success', (_message.Message,), {
    'DESCRIPTOR' : _BATCHAPPENDRESP_SUCCESS,
    '__module__' : 'streams_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.streams.BatchAppendResp.Success)
    })
  ,
  'DESCRIPTOR' : _BATCHAPPENDRESP,
  '__module__' : 'streams_pb2'
  # @@protoc_insertion_point(class_scope:event_store.client.streams.BatchAppendResp)
  })
_sym_db.RegisterMessage(BatchAppendResp)
_sym_db.RegisterMessage(BatchAppendResp.Success)

DeleteReq = _reflection.GeneratedProtocolMessageType('DeleteReq', (_message.Message,), {

  'Options' : _reflection.GeneratedProtocolMessageType('Options', (_message.Message,), {
    'DESCRIPTOR' : _DELETEREQ_OPTIONS,
    '__module__' : 'streams_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.streams.DeleteReq.Options)
    })
  ,
  'DESCRIPTOR' : _DELETEREQ,
  '__module__' : 'streams_pb2'
  # @@protoc_insertion_point(class_scope:event_store.client.streams.DeleteReq)
  })
_sym_db.RegisterMessage(DeleteReq)
_sym_db.RegisterMessage(DeleteReq.Options)

DeleteResp = _reflection.GeneratedProtocolMessageType('DeleteResp', (_message.Message,), {

  'Position' : _reflection.GeneratedProtocolMessageType('Position', (_message.Message,), {
    'DESCRIPTOR' : _DELETERESP_POSITION,
    '__module__' : 'streams_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.streams.DeleteResp.Position)
    })
  ,
  'DESCRIPTOR' : _DELETERESP,
  '__module__' : 'streams_pb2'
  # @@protoc_insertion_point(class_scope:event_store.client.streams.DeleteResp)
  })
_sym_db.RegisterMessage(DeleteResp)
_sym_db.RegisterMessage(DeleteResp.Position)

TombstoneReq = _reflection.GeneratedProtocolMessageType('TombstoneReq', (_message.Message,), {

  'Options' : _reflection.GeneratedProtocolMessageType('Options', (_message.Message,), {
    'DESCRIPTOR' : _TOMBSTONEREQ_OPTIONS,
    '__module__' : 'streams_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.streams.TombstoneReq.Options)
    })
  ,
  'DESCRIPTOR' : _TOMBSTONEREQ,
  '__module__' : 'streams_pb2'
  # @@protoc_insertion_point(class_scope:event_store.client.streams.TombstoneReq)
  })
_sym_db.RegisterMessage(TombstoneReq)
_sym_db.RegisterMessage(TombstoneReq.Options)

TombstoneResp = _reflection.GeneratedProtocolMessageType('TombstoneResp', (_message.Message,), {

  'Position' : _reflection.GeneratedProtocolMessageType('Position', (_message.Message,), {
    'DESCRIPTOR' : _TOMBSTONERESP_POSITION,
    '__module__' : 'streams_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.streams.TombstoneResp.Position)
    })
  ,
  'DESCRIPTOR' : _TOMBSTONERESP,
  '__module__' : 'streams_pb2'
  # @@protoc_insertion_point(class_scope:event_store.client.streams.TombstoneResp)
  })
_sym_db.RegisterMessage(TombstoneResp)
_sym_db.RegisterMessage(TombstoneResp.Position)

_STREAMS = DESCRIPTOR.services_by_name['Streams']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n%com.eventstore.dbclient.proto.streams'
  _READRESP_READEVENT_RECORDEDEVENT_METADATAENTRY._options = None
  _READRESP_READEVENT_RECORDEDEVENT_METADATAENTRY._serialized_options = b'8\001'
  _APPENDREQ_PROPOSEDMESSAGE_METADATAENTRY._options = None
  _APPENDREQ_PROPOSEDMESSAGE_METADATAENTRY._serialized_options = b'8\001'
  _BATCHAPPENDREQ_PROPOSEDMESSAGE_METADATAENTRY._options = None
  _BATCHAPPENDREQ_PROPOSEDMESSAGE_METADATAENTRY._serialized_options = b'8\001'
  _READREQ._serialized_start=168
  _READREQ._serialized_end=2005
  _READREQ_OPTIONS._serialized_start=242
  _READREQ_OPTIONS._serialized_end=2005
  _READREQ_OPTIONS_STREAMOPTIONS._serialized_start=899
  _READREQ_OPTIONS_STREAMOPTIONS._serialized_end=1104
  _READREQ_OPTIONS_ALLOPTIONS._serialized_start=1107
  _READREQ_OPTIONS_ALLOPTIONS._serialized_end=1293
  _READREQ_OPTIONS_SUBSCRIPTIONOPTIONS._serialized_start=1295
  _READREQ_OPTIONS_SUBSCRIPTIONOPTIONS._serialized_end=1316
  _READREQ_OPTIONS_POSITION._serialized_start=1318
  _READREQ_OPTIONS_POSITION._serialized_end=1379
  _READREQ_OPTIONS_FILTEROPTIONS._serialized_start=1382
  _READREQ_OPTIONS_FILTEROPTIONS._serialized_end=1750
  _READREQ_OPTIONS_FILTEROPTIONS_EXPRESSION._serialized_start=1687
  _READREQ_OPTIONS_FILTEROPTIONS_EXPRESSION._serialized_end=1730
  _READREQ_OPTIONS_UUIDOPTION._serialized_start=1752
  _READREQ_OPTIONS_UUIDOPTION._serialized_end=1869
  _READREQ_OPTIONS_CONTROLOPTION._serialized_start=1871
  _READREQ_OPTIONS_CONTROLOPTION._serialized_end=1909
  _READREQ_OPTIONS_READDIRECTION._serialized_start=1911
  _READREQ_OPTIONS_READDIRECTION._serialized_end=1955
  _READRESP._serialized_start=2008
  _READRESP._serialized_end=3309
  _READRESP_READEVENT._serialized_start=2465
  _READRESP_READEVENT._serialized_end=3097
  _READRESP_READEVENT_RECORDEDEVENT._serialized_start=2709
  _READRESP_READEVENT_RECORDEDEVENT._serialized_end=3085
  _READRESP_READEVENT_RECORDEDEVENT_METADATAENTRY._serialized_start=3038
  _READRESP_READEVENT_RECORDEDEVENT_METADATAENTRY._serialized_end=3085
  _READRESP_SUBSCRIPTIONCONFIRMATION._serialized_start=3099
  _READRESP_SUBSCRIPTIONCONFIRMATION._serialized_end=3150
  _READRESP_CHECKPOINT._serialized_start=3152
  _READRESP_CHECKPOINT._serialized_end=3215
  _READRESP_STREAMNOTFOUND._serialized_start=3217
  _READRESP_STREAMNOTFOUND._serialized_end=3298
  _APPENDREQ._serialized_start=3312
  _APPENDREQ._serialized_end=3983
  _APPENDREQ_OPTIONS._serialized_start=3475
  _APPENDREQ_OPTIONS._serialized_end=3739
  _APPENDREQ_PROPOSEDMESSAGE._serialized_start=3742
  _APPENDREQ_PROPOSEDMESSAGE._serialized_end=3972
  _APPENDREQ_PROPOSEDMESSAGE_METADATAENTRY._serialized_start=3038
  _APPENDREQ_PROPOSEDMESSAGE_METADATAENTRY._serialized_end=3085
  _APPENDRESP._serialized_start=3986
  _APPENDRESP._serialized_end=5151
  _APPENDRESP_POSITION._serialized_start=1318
  _APPENDRESP_POSITION._serialized_end=1379
  _APPENDRESP_SUCCESS._serialized_start=4226
  _APPENDRESP_SUCCESS._serialized_end=4476
  _APPENDRESP_WRONGEXPECTEDVERSION._serialized_start=4479
  _APPENDRESP_WRONGEXPECTEDVERSION._serialized_end=5141
  _BATCHAPPENDREQ._serialized_start=5154
  _BATCHAPPENDREQ._serialized_end=6019
  _BATCHAPPENDREQ_OPTIONS._serialized_start=5397
  _BATCHAPPENDREQ_OPTIONS._serialized_end=5781
  _BATCHAPPENDREQ_PROPOSEDMESSAGE._serialized_start=5784
  _BATCHAPPENDREQ_PROPOSEDMESSAGE._serialized_end=6019
  _BATCHAPPENDREQ_PROPOSEDMESSAGE_METADATAENTRY._serialized_start=3038
  _BATCHAPPENDREQ_PROPOSEDMESSAGE_METADATAENTRY._serialized_end=3085
  _BATCHAPPENDRESP._serialized_start=6022
  _BATCHAPPENDRESP._serialized_end=6698
  _BATCHAPPENDRESP_SUCCESS._serialized_start=6426
  _BATCHAPPENDRESP_SUCCESS._serialized_end=6660
  _DELETEREQ._serialized_start=6701
  _DELETEREQ._serialized_end=7043
  _DELETEREQ_OPTIONS._serialized_start=3475
  _DELETEREQ_OPTIONS._serialized_end=3739
  _DELETERESP._serialized_start=7046
  _DELETERESP._serialized_end=7259
  _DELETERESP_POSITION._serialized_start=1318
  _DELETERESP_POSITION._serialized_end=1379
  _TOMBSTONEREQ._serialized_start=7262
  _TOMBSTONEREQ._serialized_end=7610
  _TOMBSTONEREQ_OPTIONS._serialized_start=3475
  _TOMBSTONEREQ_OPTIONS._serialized_end=3739
  _TOMBSTONERESP._serialized_start=7613
  _TOMBSTONERESP._serialized_end=7832
  _TOMBSTONERESP_POSITION._serialized_start=1318
  _TOMBSTONERESP_POSITION._serialized_end=1379
  _STREAMS._serialized_start=7835
  _STREAMS._serialized_end=8315
# @@protoc_insertion_point(module_scope)
