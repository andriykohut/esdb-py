# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: persistent.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import shared_pb2 as shared__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10persistent.proto\x12+event_store.client.persistent_subscriptions\x1a\x0cshared.proto\"\x99\x07\n\x07ReadReq\x12O\n\x07options\x18\x01 \x01(\x0b\x32<.event_store.client.persistent_subscriptions.ReadReq.OptionsH\x00\x12G\n\x03\x61\x63k\x18\x02 \x01(\x0b\x32\x38.event_store.client.persistent_subscriptions.ReadReq.AckH\x00\x12I\n\x04nack\x18\x03 \x01(\x0b\x32\x39.event_store.client.persistent_subscriptions.ReadReq.NackH\x00\x1a\x85\x03\n\x07Options\x12\x41\n\x11stream_identifier\x18\x01 \x01(\x0b\x32$.event_store.client.StreamIdentifierH\x00\x12(\n\x03\x61ll\x18\x05 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x12\x12\n\ngroup_name\x18\x02 \x01(\t\x12\x13\n\x0b\x62uffer_size\x18\x03 \x01(\x05\x12\\\n\x0buuid_option\x18\x04 \x01(\x0b\x32G.event_store.client.persistent_subscriptions.ReadReq.Options.UUIDOption\x1au\n\nUUIDOption\x12/\n\nstructured\x18\x01 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x12+\n\x06string\x18\x02 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x42\t\n\x07\x63ontentB\x0f\n\rstream_option\x1a\x38\n\x03\x41\x63k\x12\n\n\x02id\x18\x01 \x01(\x0c\x12%\n\x03ids\x18\x02 \x03(\x0b\x32\x18.event_store.client.UUID\x1a\xdb\x01\n\x04Nack\x12\n\n\x02id\x18\x01 \x01(\x0c\x12%\n\x03ids\x18\x02 \x03(\x0b\x32\x18.event_store.client.UUID\x12P\n\x06\x61\x63tion\x18\x03 \x01(\x0e\x32@.event_store.client.persistent_subscriptions.ReadReq.Nack.Action\x12\x0e\n\x06reason\x18\x04 \x01(\t\">\n\x06\x41\x63tion\x12\x0b\n\x07Unknown\x10\x00\x12\x08\n\x04Park\x10\x01\x12\t\n\x05Retry\x10\x02\x12\x08\n\x04Skip\x10\x03\x12\x08\n\x04Stop\x10\x04\x42\t\n\x07\x63ontent\"\x94\x08\n\x08ReadResp\x12P\n\x05\x65vent\x18\x01 \x01(\x0b\x32?.event_store.client.persistent_subscriptions.ReadResp.ReadEventH\x00\x12s\n\x19subscription_confirmation\x18\x02 \x01(\x0b\x32N.event_store.client.persistent_subscriptions.ReadResp.SubscriptionConfirmationH\x00\x1a\x80\x06\n\tReadEvent\x12\\\n\x05\x65vent\x18\x01 \x01(\x0b\x32M.event_store.client.persistent_subscriptions.ReadResp.ReadEvent.RecordedEvent\x12[\n\x04link\x18\x02 \x01(\x0b\x32M.event_store.client.persistent_subscriptions.ReadResp.ReadEvent.RecordedEvent\x12\x19\n\x0f\x63ommit_position\x18\x03 \x01(\x04H\x00\x12\x30\n\x0bno_position\x18\x04 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x12\x15\n\x0bretry_count\x18\x05 \x01(\x05H\x01\x12\x33\n\x0eno_retry_count\x18\x06 \x01(\x0b\x32\x19.event_store.client.EmptyH\x01\x1a\x89\x03\n\rRecordedEvent\x12$\n\x02id\x18\x01 \x01(\x0b\x32\x18.event_store.client.UUID\x12?\n\x11stream_identifier\x18\x02 \x01(\x0b\x32$.event_store.client.StreamIdentifier\x12\x17\n\x0fstream_revision\x18\x03 \x01(\x04\x12\x18\n\x10prepare_position\x18\x04 \x01(\x04\x12\x17\n\x0f\x63ommit_position\x18\x05 \x01(\x04\x12m\n\x08metadata\x18\x06 \x03(\x0b\x32[.event_store.client.persistent_subscriptions.ReadResp.ReadEvent.RecordedEvent.MetadataEntry\x12\x17\n\x0f\x63ustom_metadata\x18\x07 \x01(\x0c\x12\x0c\n\x04\x64\x61ta\x18\x08 \x01(\x0c\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42\n\n\x08positionB\x07\n\x05\x63ount\x1a\x33\n\x18SubscriptionConfirmation\x12\x17\n\x0fsubscription_id\x18\x01 \x01(\tB\t\n\x07\x63ontent\"\xf6\x10\n\tCreateReq\x12O\n\x07options\x18\x01 \x01(\x0b\x32>.event_store.client.persistent_subscriptions.CreateReq.Options\x1a\xf0\x02\n\x07Options\x12V\n\x06stream\x18\x04 \x01(\x0b\x32\x44.event_store.client.persistent_subscriptions.CreateReq.StreamOptionsH\x00\x12P\n\x03\x61ll\x18\x05 \x01(\x0b\x32\x41.event_store.client.persistent_subscriptions.CreateReq.AllOptionsH\x00\x12\x43\n\x11stream_identifier\x18\x01 \x01(\x0b\x32$.event_store.client.StreamIdentifierB\x02\x18\x01\x12\x12\n\ngroup_name\x18\x02 \x01(\t\x12Q\n\x08settings\x18\x03 \x01(\x0b\x32?.event_store.client.persistent_subscriptions.CreateReq.SettingsB\x0f\n\rstream_option\x1a\xcd\x01\n\rStreamOptions\x12?\n\x11stream_identifier\x18\x01 \x01(\x0b\x32$.event_store.client.StreamIdentifier\x12\x12\n\x08revision\x18\x02 \x01(\x04H\x00\x12*\n\x05start\x18\x03 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x12(\n\x03\x65nd\x18\x04 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x42\x11\n\x0frevision_option\x1a\x88\x06\n\nAllOptions\x12S\n\x08position\x18\x01 \x01(\x0b\x32?.event_store.client.persistent_subscriptions.CreateReq.PositionH\x00\x12*\n\x05start\x18\x02 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x12(\n\x03\x65nd\x18\x03 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x12\x61\n\x06\x66ilter\x18\x04 \x01(\x0b\x32O.event_store.client.persistent_subscriptions.CreateReq.AllOptions.FilterOptionsH\x01\x12.\n\tno_filter\x18\x05 \x01(\x0b\x32\x19.event_store.client.EmptyH\x01\x1a\x9c\x03\n\rFilterOptions\x12w\n\x11stream_identifier\x18\x01 \x01(\x0b\x32Z.event_store.client.persistent_subscriptions.CreateReq.AllOptions.FilterOptions.ExpressionH\x00\x12p\n\nevent_type\x18\x02 \x01(\x0b\x32Z.event_store.client.persistent_subscriptions.CreateReq.AllOptions.FilterOptions.ExpressionH\x00\x12\r\n\x03max\x18\x03 \x01(\rH\x01\x12*\n\x05\x63ount\x18\x04 \x01(\x0b\x32\x19.event_store.client.EmptyH\x01\x12$\n\x1c\x63heckpointIntervalMultiplier\x18\x05 \x01(\r\x1a+\n\nExpression\x12\r\n\x05regex\x18\x01 \x01(\t\x12\x0e\n\x06prefix\x18\x02 \x03(\tB\x08\n\x06\x66ilterB\x08\n\x06windowB\x0c\n\nall_optionB\x0f\n\rfilter_option\x1a=\n\x08Position\x12\x17\n\x0f\x63ommit_position\x18\x01 \x01(\x04\x12\x18\n\x10prepare_position\x18\x02 \x01(\x04\x1a\xc4\x04\n\x08Settings\x12\x15\n\rresolve_links\x18\x01 \x01(\x08\x12\x14\n\x08revision\x18\x02 \x01(\x04\x42\x02\x18\x01\x12\x18\n\x10\x65xtra_statistics\x18\x03 \x01(\x08\x12\x17\n\x0fmax_retry_count\x18\x05 \x01(\x05\x12\x1c\n\x14min_checkpoint_count\x18\x07 \x01(\x05\x12\x1c\n\x14max_checkpoint_count\x18\x08 \x01(\x05\x12\x1c\n\x14max_subscriber_count\x18\t \x01(\x05\x12\x18\n\x10live_buffer_size\x18\n \x01(\x05\x12\x17\n\x0fread_batch_size\x18\x0b \x01(\x05\x12\x1b\n\x13history_buffer_size\x18\x0c \x01(\x05\x12l\n\x17named_consumer_strategy\x18\r \x01(\x0e\x32G.event_store.client.persistent_subscriptions.CreateReq.ConsumerStrategyB\x02\x18\x01\x12\x1f\n\x15message_timeout_ticks\x18\x04 \x01(\x03H\x00\x12\x1c\n\x12message_timeout_ms\x18\x0e \x01(\x05H\x00\x12 \n\x16\x63heckpoint_after_ticks\x18\x06 \x01(\x03H\x01\x12\x1d\n\x13\x63heckpoint_after_ms\x18\x0f \x01(\x05H\x01\x12\x19\n\x11\x63onsumer_strategy\x18\x10 \x01(\tB\x11\n\x0fmessage_timeoutB\x12\n\x10\x63heckpoint_after\"D\n\x10\x43onsumerStrategy\x12\x14\n\x10\x44ispatchToSingle\x10\x00\x12\x0e\n\nRoundRobin\x10\x01\x12\n\n\x06Pinned\x10\x02\"\x0c\n\nCreateResp\"\x94\x0c\n\tUpdateReq\x12O\n\x07options\x18\x01 \x01(\x0b\x32>.event_store.client.persistent_subscriptions.UpdateReq.Options\x1a\xf0\x02\n\x07Options\x12V\n\x06stream\x18\x04 \x01(\x0b\x32\x44.event_store.client.persistent_subscriptions.UpdateReq.StreamOptionsH\x00\x12P\n\x03\x61ll\x18\x05 \x01(\x0b\x32\x41.event_store.client.persistent_subscriptions.UpdateReq.AllOptionsH\x00\x12\x43\n\x11stream_identifier\x18\x01 \x01(\x0b\x32$.event_store.client.StreamIdentifierB\x02\x18\x01\x12\x12\n\ngroup_name\x18\x02 \x01(\t\x12Q\n\x08settings\x18\x03 \x01(\x0b\x32?.event_store.client.persistent_subscriptions.UpdateReq.SettingsB\x0f\n\rstream_option\x1a\xcd\x01\n\rStreamOptions\x12?\n\x11stream_identifier\x18\x01 \x01(\x0b\x32$.event_store.client.StreamIdentifier\x12\x12\n\x08revision\x18\x02 \x01(\x04H\x00\x12*\n\x05start\x18\x03 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x12(\n\x03\x65nd\x18\x04 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x42\x11\n\x0frevision_option\x1a\xc5\x01\n\nAllOptions\x12S\n\x08position\x18\x01 \x01(\x0b\x32?.event_store.client.persistent_subscriptions.UpdateReq.PositionH\x00\x12*\n\x05start\x18\x02 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x12(\n\x03\x65nd\x18\x03 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x42\x0c\n\nall_option\x1a=\n\x08Position\x12\x17\n\x0f\x63ommit_position\x18\x01 \x01(\x04\x12\x18\n\x10prepare_position\x18\x02 \x01(\x04\x1a\xa5\x04\n\x08Settings\x12\x15\n\rresolve_links\x18\x01 \x01(\x08\x12\x14\n\x08revision\x18\x02 \x01(\x04\x42\x02\x18\x01\x12\x18\n\x10\x65xtra_statistics\x18\x03 \x01(\x08\x12\x17\n\x0fmax_retry_count\x18\x05 \x01(\x05\x12\x1c\n\x14min_checkpoint_count\x18\x07 \x01(\x05\x12\x1c\n\x14max_checkpoint_count\x18\x08 \x01(\x05\x12\x1c\n\x14max_subscriber_count\x18\t \x01(\x05\x12\x18\n\x10live_buffer_size\x18\n \x01(\x05\x12\x17\n\x0fread_batch_size\x18\x0b \x01(\x05\x12\x1b\n\x13history_buffer_size\x18\x0c \x01(\x05\x12h\n\x17named_consumer_strategy\x18\r \x01(\x0e\x32G.event_store.client.persistent_subscriptions.UpdateReq.ConsumerStrategy\x12\x1f\n\x15message_timeout_ticks\x18\x04 \x01(\x03H\x00\x12\x1c\n\x12message_timeout_ms\x18\x0e \x01(\x05H\x00\x12 \n\x16\x63heckpoint_after_ticks\x18\x06 \x01(\x03H\x01\x12\x1d\n\x13\x63heckpoint_after_ms\x18\x0f \x01(\x05H\x01\x42\x11\n\x0fmessage_timeoutB\x12\n\x10\x63heckpoint_after\"D\n\x10\x43onsumerStrategy\x12\x14\n\x10\x44ispatchToSingle\x10\x00\x12\x0e\n\nRoundRobin\x10\x01\x12\n\n\x06Pinned\x10\x02\"\x0c\n\nUpdateResp\"\xfa\x01\n\tDeleteReq\x12O\n\x07options\x18\x01 \x01(\x0b\x32>.event_store.client.persistent_subscriptions.DeleteReq.Options\x1a\x9b\x01\n\x07Options\x12\x41\n\x11stream_identifier\x18\x01 \x01(\x0b\x32$.event_store.client.StreamIdentifierH\x00\x12(\n\x03\x61ll\x18\x03 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x12\x12\n\ngroup_name\x18\x02 \x01(\tB\x0f\n\rstream_option\"\x0c\n\nDeleteResp\"\xfc\x01\n\nGetInfoReq\x12P\n\x07options\x18\x01 \x01(\x0b\x32?.event_store.client.persistent_subscriptions.GetInfoReq.Options\x1a\x9b\x01\n\x07Options\x12\x41\n\x11stream_identifier\x18\x01 \x01(\x0b\x32$.event_store.client.StreamIdentifierH\x00\x12(\n\x03\x61ll\x18\x02 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x12\x12\n\ngroup_name\x18\x03 \x01(\tB\x0f\n\rstream_option\"g\n\x0bGetInfoResp\x12X\n\x11subscription_info\x18\x01 \x01(\x0b\x32=.event_store.client.persistent_subscriptions.SubscriptionInfo\"\xf0\t\n\x10SubscriptionInfo\x12\x14\n\x0c\x65vent_source\x18\x01 \x01(\t\x12\x12\n\ngroup_name\x18\x02 \x01(\t\x12\x0e\n\x06status\x18\x03 \x01(\t\x12\x61\n\x0b\x63onnections\x18\x04 \x03(\x0b\x32L.event_store.client.persistent_subscriptions.SubscriptionInfo.ConnectionInfo\x12\x1a\n\x12\x61verage_per_second\x18\x05 \x01(\x05\x12\x13\n\x0btotal_items\x18\x06 \x01(\x03\x12$\n\x1c\x63ount_since_last_measurement\x18\x07 \x01(\x03\x12(\n last_checkpointed_event_position\x18\x08 \x01(\t\x12!\n\x19last_known_event_position\x18\t \x01(\t\x12\x18\n\x10resolve_link_tos\x18\n \x01(\x08\x12\x12\n\nstart_from\x18\x0b \x01(\t\x12$\n\x1cmessage_timeout_milliseconds\x18\x0c \x01(\x05\x12\x18\n\x10\x65xtra_statistics\x18\r \x01(\x08\x12\x17\n\x0fmax_retry_count\x18\x0e \x01(\x05\x12\x18\n\x10live_buffer_size\x18\x0f \x01(\x05\x12\x13\n\x0b\x62uffer_size\x18\x10 \x01(\x05\x12\x17\n\x0fread_batch_size\x18\x11 \x01(\x05\x12&\n\x1e\x63heck_point_after_milliseconds\x18\x12 \x01(\x05\x12\x1d\n\x15min_check_point_count\x18\x13 \x01(\x05\x12\x1d\n\x15max_check_point_count\x18\x14 \x01(\x05\x12\x19\n\x11read_buffer_count\x18\x15 \x01(\x05\x12\x19\n\x11live_buffer_count\x18\x16 \x01(\x03\x12\x1a\n\x12retry_buffer_count\x18\x17 \x01(\x05\x12 \n\x18total_in_flight_messages\x18\x18 \x01(\x05\x12\"\n\x1aoutstanding_messages_count\x18\x19 \x01(\x05\x12\x1f\n\x17named_consumer_strategy\x18\x1a \x01(\t\x12\x1c\n\x14max_subscriber_count\x18\x1b \x01(\x05\x12\x1c\n\x14parked_message_count\x18\x1c \x01(\x03\x1a\xc5\x02\n\x0e\x43onnectionInfo\x12\x0c\n\x04\x66rom\x18\x01 \x01(\t\x12\x10\n\x08username\x18\x02 \x01(\t\x12 \n\x18\x61verage_items_per_second\x18\x03 \x01(\x05\x12\x13\n\x0btotal_items\x18\x04 \x01(\x03\x12$\n\x1c\x63ount_since_last_measurement\x18\x05 \x01(\x03\x12h\n\x15observed_measurements\x18\x06 \x03(\x0b\x32I.event_store.client.persistent_subscriptions.SubscriptionInfo.Measurement\x12\x17\n\x0f\x61vailable_slots\x18\x07 \x01(\x05\x12\x1a\n\x12in_flight_messages\x18\x08 \x01(\x05\x12\x17\n\x0f\x63onnection_name\x18\t \x01(\t\x1a)\n\x0bMeasurement\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x03\"\xda\x02\n\x0fReplayParkedReq\x12U\n\x07options\x18\x01 \x01(\x0b\x32\x44.event_store.client.persistent_subscriptions.ReplayParkedReq.Options\x1a\xef\x01\n\x07Options\x12\x12\n\ngroup_name\x18\x01 \x01(\t\x12\x41\n\x11stream_identifier\x18\x02 \x01(\x0b\x32$.event_store.client.StreamIdentifierH\x00\x12(\n\x03\x61ll\x18\x03 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x12\x11\n\x07stop_at\x18\x04 \x01(\x03H\x01\x12-\n\x08no_limit\x18\x05 \x01(\x0b\x32\x19.event_store.client.EmptyH\x01\x42\x0f\n\rstream_optionB\x10\n\x0estop_at_option\"\x12\n\x10ReplayParkedResp\"\x92\x03\n\x07ListReq\x12M\n\x07options\x18\x01 \x01(\x0b\x32<.event_store.client.persistent_subscriptions.ListReq.Options\x1a\xb3\x01\n\x07Options\x12;\n\x16list_all_subscriptions\x18\x01 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x12\\\n\x0flist_for_stream\x18\x02 \x01(\x0b\x32\x41.event_store.client.persistent_subscriptions.ListReq.StreamOptionH\x00\x42\r\n\x0blist_option\x1a\x81\x01\n\x0cStreamOption\x12\x36\n\x06stream\x18\x01 \x01(\x0b\x32$.event_store.client.StreamIdentifierH\x00\x12(\n\x03\x61ll\x18\x02 \x01(\x0b\x32\x19.event_store.client.EmptyH\x00\x42\x0f\n\rstream_option\"`\n\x08ListResp\x12T\n\rsubscriptions\x18\x01 \x03(\x0b\x32=.event_store.client.persistent_subscriptions.SubscriptionInfo2\xce\x07\n\x17PersistentSubscriptions\x12y\n\x06\x43reate\x12\x36.event_store.client.persistent_subscriptions.CreateReq\x1a\x37.event_store.client.persistent_subscriptions.CreateResp\x12y\n\x06Update\x12\x36.event_store.client.persistent_subscriptions.UpdateReq\x1a\x37.event_store.client.persistent_subscriptions.UpdateResp\x12y\n\x06\x44\x65lete\x12\x36.event_store.client.persistent_subscriptions.DeleteReq\x1a\x37.event_store.client.persistent_subscriptions.DeleteResp\x12w\n\x04Read\x12\x34.event_store.client.persistent_subscriptions.ReadReq\x1a\x35.event_store.client.persistent_subscriptions.ReadResp(\x01\x30\x01\x12|\n\x07GetInfo\x12\x37.event_store.client.persistent_subscriptions.GetInfoReq\x1a\x38.event_store.client.persistent_subscriptions.GetInfoResp\x12\x8b\x01\n\x0cReplayParked\x12<.event_store.client.persistent_subscriptions.ReplayParkedReq\x1a=.event_store.client.persistent_subscriptions.ReplayParkedResp\x12s\n\x04List\x12\x34.event_store.client.persistent_subscriptions.ListReq\x1a\x35.event_store.client.persistent_subscriptions.ListResp\x12H\n\x10RestartSubsystem\x12\x19.event_store.client.Empty\x1a\x19.event_store.client.EmptyB7\n5com.eventstore.dbclient.proto.persistentsubscriptionsb\x06proto3')



_READREQ = DESCRIPTOR.message_types_by_name['ReadReq']
_READREQ_OPTIONS = _READREQ.nested_types_by_name['Options']
_READREQ_OPTIONS_UUIDOPTION = _READREQ_OPTIONS.nested_types_by_name['UUIDOption']
_READREQ_ACK = _READREQ.nested_types_by_name['Ack']
_READREQ_NACK = _READREQ.nested_types_by_name['Nack']
_READRESP = DESCRIPTOR.message_types_by_name['ReadResp']
_READRESP_READEVENT = _READRESP.nested_types_by_name['ReadEvent']
_READRESP_READEVENT_RECORDEDEVENT = _READRESP_READEVENT.nested_types_by_name['RecordedEvent']
_READRESP_READEVENT_RECORDEDEVENT_METADATAENTRY = _READRESP_READEVENT_RECORDEDEVENT.nested_types_by_name['MetadataEntry']
_READRESP_SUBSCRIPTIONCONFIRMATION = _READRESP.nested_types_by_name['SubscriptionConfirmation']
_CREATEREQ = DESCRIPTOR.message_types_by_name['CreateReq']
_CREATEREQ_OPTIONS = _CREATEREQ.nested_types_by_name['Options']
_CREATEREQ_STREAMOPTIONS = _CREATEREQ.nested_types_by_name['StreamOptions']
_CREATEREQ_ALLOPTIONS = _CREATEREQ.nested_types_by_name['AllOptions']
_CREATEREQ_ALLOPTIONS_FILTEROPTIONS = _CREATEREQ_ALLOPTIONS.nested_types_by_name['FilterOptions']
_CREATEREQ_ALLOPTIONS_FILTEROPTIONS_EXPRESSION = _CREATEREQ_ALLOPTIONS_FILTEROPTIONS.nested_types_by_name['Expression']
_CREATEREQ_POSITION = _CREATEREQ.nested_types_by_name['Position']
_CREATEREQ_SETTINGS = _CREATEREQ.nested_types_by_name['Settings']
_CREATERESP = DESCRIPTOR.message_types_by_name['CreateResp']
_UPDATEREQ = DESCRIPTOR.message_types_by_name['UpdateReq']
_UPDATEREQ_OPTIONS = _UPDATEREQ.nested_types_by_name['Options']
_UPDATEREQ_STREAMOPTIONS = _UPDATEREQ.nested_types_by_name['StreamOptions']
_UPDATEREQ_ALLOPTIONS = _UPDATEREQ.nested_types_by_name['AllOptions']
_UPDATEREQ_POSITION = _UPDATEREQ.nested_types_by_name['Position']
_UPDATEREQ_SETTINGS = _UPDATEREQ.nested_types_by_name['Settings']
_UPDATERESP = DESCRIPTOR.message_types_by_name['UpdateResp']
_DELETEREQ = DESCRIPTOR.message_types_by_name['DeleteReq']
_DELETEREQ_OPTIONS = _DELETEREQ.nested_types_by_name['Options']
_DELETERESP = DESCRIPTOR.message_types_by_name['DeleteResp']
_GETINFOREQ = DESCRIPTOR.message_types_by_name['GetInfoReq']
_GETINFOREQ_OPTIONS = _GETINFOREQ.nested_types_by_name['Options']
_GETINFORESP = DESCRIPTOR.message_types_by_name['GetInfoResp']
_SUBSCRIPTIONINFO = DESCRIPTOR.message_types_by_name['SubscriptionInfo']
_SUBSCRIPTIONINFO_CONNECTIONINFO = _SUBSCRIPTIONINFO.nested_types_by_name['ConnectionInfo']
_SUBSCRIPTIONINFO_MEASUREMENT = _SUBSCRIPTIONINFO.nested_types_by_name['Measurement']
_REPLAYPARKEDREQ = DESCRIPTOR.message_types_by_name['ReplayParkedReq']
_REPLAYPARKEDREQ_OPTIONS = _REPLAYPARKEDREQ.nested_types_by_name['Options']
_REPLAYPARKEDRESP = DESCRIPTOR.message_types_by_name['ReplayParkedResp']
_LISTREQ = DESCRIPTOR.message_types_by_name['ListReq']
_LISTREQ_OPTIONS = _LISTREQ.nested_types_by_name['Options']
_LISTREQ_STREAMOPTION = _LISTREQ.nested_types_by_name['StreamOption']
_LISTRESP = DESCRIPTOR.message_types_by_name['ListResp']
_READREQ_NACK_ACTION = _READREQ_NACK.enum_types_by_name['Action']
_CREATEREQ_CONSUMERSTRATEGY = _CREATEREQ.enum_types_by_name['ConsumerStrategy']
_UPDATEREQ_CONSUMERSTRATEGY = _UPDATEREQ.enum_types_by_name['ConsumerStrategy']
ReadReq = _reflection.GeneratedProtocolMessageType('ReadReq', (_message.Message,), {

  'Options' : _reflection.GeneratedProtocolMessageType('Options', (_message.Message,), {

    'UUIDOption' : _reflection.GeneratedProtocolMessageType('UUIDOption', (_message.Message,), {
      'DESCRIPTOR' : _READREQ_OPTIONS_UUIDOPTION,
      '__module__' : 'persistent_pb2'
      # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.ReadReq.Options.UUIDOption)
      })
    ,
    'DESCRIPTOR' : _READREQ_OPTIONS,
    '__module__' : 'persistent_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.ReadReq.Options)
    })
  ,

  'Ack' : _reflection.GeneratedProtocolMessageType('Ack', (_message.Message,), {
    'DESCRIPTOR' : _READREQ_ACK,
    '__module__' : 'persistent_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.ReadReq.Ack)
    })
  ,

  'Nack' : _reflection.GeneratedProtocolMessageType('Nack', (_message.Message,), {
    'DESCRIPTOR' : _READREQ_NACK,
    '__module__' : 'persistent_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.ReadReq.Nack)
    })
  ,
  'DESCRIPTOR' : _READREQ,
  '__module__' : 'persistent_pb2'
  # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.ReadReq)
  })
_sym_db.RegisterMessage(ReadReq)
_sym_db.RegisterMessage(ReadReq.Options)
_sym_db.RegisterMessage(ReadReq.Options.UUIDOption)
_sym_db.RegisterMessage(ReadReq.Ack)
_sym_db.RegisterMessage(ReadReq.Nack)

ReadResp = _reflection.GeneratedProtocolMessageType('ReadResp', (_message.Message,), {

  'ReadEvent' : _reflection.GeneratedProtocolMessageType('ReadEvent', (_message.Message,), {

    'RecordedEvent' : _reflection.GeneratedProtocolMessageType('RecordedEvent', (_message.Message,), {

      'MetadataEntry' : _reflection.GeneratedProtocolMessageType('MetadataEntry', (_message.Message,), {
        'DESCRIPTOR' : _READRESP_READEVENT_RECORDEDEVENT_METADATAENTRY,
        '__module__' : 'persistent_pb2'
        # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.ReadResp.ReadEvent.RecordedEvent.MetadataEntry)
        })
      ,
      'DESCRIPTOR' : _READRESP_READEVENT_RECORDEDEVENT,
      '__module__' : 'persistent_pb2'
      # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.ReadResp.ReadEvent.RecordedEvent)
      })
    ,
    'DESCRIPTOR' : _READRESP_READEVENT,
    '__module__' : 'persistent_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.ReadResp.ReadEvent)
    })
  ,

  'SubscriptionConfirmation' : _reflection.GeneratedProtocolMessageType('SubscriptionConfirmation', (_message.Message,), {
    'DESCRIPTOR' : _READRESP_SUBSCRIPTIONCONFIRMATION,
    '__module__' : 'persistent_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.ReadResp.SubscriptionConfirmation)
    })
  ,
  'DESCRIPTOR' : _READRESP,
  '__module__' : 'persistent_pb2'
  # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.ReadResp)
  })
_sym_db.RegisterMessage(ReadResp)
_sym_db.RegisterMessage(ReadResp.ReadEvent)
_sym_db.RegisterMessage(ReadResp.ReadEvent.RecordedEvent)
_sym_db.RegisterMessage(ReadResp.ReadEvent.RecordedEvent.MetadataEntry)
_sym_db.RegisterMessage(ReadResp.SubscriptionConfirmation)

CreateReq = _reflection.GeneratedProtocolMessageType('CreateReq', (_message.Message,), {

  'Options' : _reflection.GeneratedProtocolMessageType('Options', (_message.Message,), {
    'DESCRIPTOR' : _CREATEREQ_OPTIONS,
    '__module__' : 'persistent_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.CreateReq.Options)
    })
  ,

  'StreamOptions' : _reflection.GeneratedProtocolMessageType('StreamOptions', (_message.Message,), {
    'DESCRIPTOR' : _CREATEREQ_STREAMOPTIONS,
    '__module__' : 'persistent_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.CreateReq.StreamOptions)
    })
  ,

  'AllOptions' : _reflection.GeneratedProtocolMessageType('AllOptions', (_message.Message,), {

    'FilterOptions' : _reflection.GeneratedProtocolMessageType('FilterOptions', (_message.Message,), {

      'Expression' : _reflection.GeneratedProtocolMessageType('Expression', (_message.Message,), {
        'DESCRIPTOR' : _CREATEREQ_ALLOPTIONS_FILTEROPTIONS_EXPRESSION,
        '__module__' : 'persistent_pb2'
        # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.CreateReq.AllOptions.FilterOptions.Expression)
        })
      ,
      'DESCRIPTOR' : _CREATEREQ_ALLOPTIONS_FILTEROPTIONS,
      '__module__' : 'persistent_pb2'
      # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.CreateReq.AllOptions.FilterOptions)
      })
    ,
    'DESCRIPTOR' : _CREATEREQ_ALLOPTIONS,
    '__module__' : 'persistent_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.CreateReq.AllOptions)
    })
  ,

  'Position' : _reflection.GeneratedProtocolMessageType('Position', (_message.Message,), {
    'DESCRIPTOR' : _CREATEREQ_POSITION,
    '__module__' : 'persistent_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.CreateReq.Position)
    })
  ,

  'Settings' : _reflection.GeneratedProtocolMessageType('Settings', (_message.Message,), {
    'DESCRIPTOR' : _CREATEREQ_SETTINGS,
    '__module__' : 'persistent_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.CreateReq.Settings)
    })
  ,
  'DESCRIPTOR' : _CREATEREQ,
  '__module__' : 'persistent_pb2'
  # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.CreateReq)
  })
_sym_db.RegisterMessage(CreateReq)
_sym_db.RegisterMessage(CreateReq.Options)
_sym_db.RegisterMessage(CreateReq.StreamOptions)
_sym_db.RegisterMessage(CreateReq.AllOptions)
_sym_db.RegisterMessage(CreateReq.AllOptions.FilterOptions)
_sym_db.RegisterMessage(CreateReq.AllOptions.FilterOptions.Expression)
_sym_db.RegisterMessage(CreateReq.Position)
_sym_db.RegisterMessage(CreateReq.Settings)

CreateResp = _reflection.GeneratedProtocolMessageType('CreateResp', (_message.Message,), {
  'DESCRIPTOR' : _CREATERESP,
  '__module__' : 'persistent_pb2'
  # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.CreateResp)
  })
_sym_db.RegisterMessage(CreateResp)

UpdateReq = _reflection.GeneratedProtocolMessageType('UpdateReq', (_message.Message,), {

  'Options' : _reflection.GeneratedProtocolMessageType('Options', (_message.Message,), {
    'DESCRIPTOR' : _UPDATEREQ_OPTIONS,
    '__module__' : 'persistent_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.UpdateReq.Options)
    })
  ,

  'StreamOptions' : _reflection.GeneratedProtocolMessageType('StreamOptions', (_message.Message,), {
    'DESCRIPTOR' : _UPDATEREQ_STREAMOPTIONS,
    '__module__' : 'persistent_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.UpdateReq.StreamOptions)
    })
  ,

  'AllOptions' : _reflection.GeneratedProtocolMessageType('AllOptions', (_message.Message,), {
    'DESCRIPTOR' : _UPDATEREQ_ALLOPTIONS,
    '__module__' : 'persistent_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.UpdateReq.AllOptions)
    })
  ,

  'Position' : _reflection.GeneratedProtocolMessageType('Position', (_message.Message,), {
    'DESCRIPTOR' : _UPDATEREQ_POSITION,
    '__module__' : 'persistent_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.UpdateReq.Position)
    })
  ,

  'Settings' : _reflection.GeneratedProtocolMessageType('Settings', (_message.Message,), {
    'DESCRIPTOR' : _UPDATEREQ_SETTINGS,
    '__module__' : 'persistent_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.UpdateReq.Settings)
    })
  ,
  'DESCRIPTOR' : _UPDATEREQ,
  '__module__' : 'persistent_pb2'
  # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.UpdateReq)
  })
_sym_db.RegisterMessage(UpdateReq)
_sym_db.RegisterMessage(UpdateReq.Options)
_sym_db.RegisterMessage(UpdateReq.StreamOptions)
_sym_db.RegisterMessage(UpdateReq.AllOptions)
_sym_db.RegisterMessage(UpdateReq.Position)
_sym_db.RegisterMessage(UpdateReq.Settings)

UpdateResp = _reflection.GeneratedProtocolMessageType('UpdateResp', (_message.Message,), {
  'DESCRIPTOR' : _UPDATERESP,
  '__module__' : 'persistent_pb2'
  # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.UpdateResp)
  })
_sym_db.RegisterMessage(UpdateResp)

DeleteReq = _reflection.GeneratedProtocolMessageType('DeleteReq', (_message.Message,), {

  'Options' : _reflection.GeneratedProtocolMessageType('Options', (_message.Message,), {
    'DESCRIPTOR' : _DELETEREQ_OPTIONS,
    '__module__' : 'persistent_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.DeleteReq.Options)
    })
  ,
  'DESCRIPTOR' : _DELETEREQ,
  '__module__' : 'persistent_pb2'
  # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.DeleteReq)
  })
_sym_db.RegisterMessage(DeleteReq)
_sym_db.RegisterMessage(DeleteReq.Options)

DeleteResp = _reflection.GeneratedProtocolMessageType('DeleteResp', (_message.Message,), {
  'DESCRIPTOR' : _DELETERESP,
  '__module__' : 'persistent_pb2'
  # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.DeleteResp)
  })
_sym_db.RegisterMessage(DeleteResp)

GetInfoReq = _reflection.GeneratedProtocolMessageType('GetInfoReq', (_message.Message,), {

  'Options' : _reflection.GeneratedProtocolMessageType('Options', (_message.Message,), {
    'DESCRIPTOR' : _GETINFOREQ_OPTIONS,
    '__module__' : 'persistent_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.GetInfoReq.Options)
    })
  ,
  'DESCRIPTOR' : _GETINFOREQ,
  '__module__' : 'persistent_pb2'
  # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.GetInfoReq)
  })
_sym_db.RegisterMessage(GetInfoReq)
_sym_db.RegisterMessage(GetInfoReq.Options)

GetInfoResp = _reflection.GeneratedProtocolMessageType('GetInfoResp', (_message.Message,), {
  'DESCRIPTOR' : _GETINFORESP,
  '__module__' : 'persistent_pb2'
  # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.GetInfoResp)
  })
_sym_db.RegisterMessage(GetInfoResp)

SubscriptionInfo = _reflection.GeneratedProtocolMessageType('SubscriptionInfo', (_message.Message,), {

  'ConnectionInfo' : _reflection.GeneratedProtocolMessageType('ConnectionInfo', (_message.Message,), {
    'DESCRIPTOR' : _SUBSCRIPTIONINFO_CONNECTIONINFO,
    '__module__' : 'persistent_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.SubscriptionInfo.ConnectionInfo)
    })
  ,

  'Measurement' : _reflection.GeneratedProtocolMessageType('Measurement', (_message.Message,), {
    'DESCRIPTOR' : _SUBSCRIPTIONINFO_MEASUREMENT,
    '__module__' : 'persistent_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.SubscriptionInfo.Measurement)
    })
  ,
  'DESCRIPTOR' : _SUBSCRIPTIONINFO,
  '__module__' : 'persistent_pb2'
  # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.SubscriptionInfo)
  })
_sym_db.RegisterMessage(SubscriptionInfo)
_sym_db.RegisterMessage(SubscriptionInfo.ConnectionInfo)
_sym_db.RegisterMessage(SubscriptionInfo.Measurement)

ReplayParkedReq = _reflection.GeneratedProtocolMessageType('ReplayParkedReq', (_message.Message,), {

  'Options' : _reflection.GeneratedProtocolMessageType('Options', (_message.Message,), {
    'DESCRIPTOR' : _REPLAYPARKEDREQ_OPTIONS,
    '__module__' : 'persistent_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.ReplayParkedReq.Options)
    })
  ,
  'DESCRIPTOR' : _REPLAYPARKEDREQ,
  '__module__' : 'persistent_pb2'
  # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.ReplayParkedReq)
  })
_sym_db.RegisterMessage(ReplayParkedReq)
_sym_db.RegisterMessage(ReplayParkedReq.Options)

ReplayParkedResp = _reflection.GeneratedProtocolMessageType('ReplayParkedResp', (_message.Message,), {
  'DESCRIPTOR' : _REPLAYPARKEDRESP,
  '__module__' : 'persistent_pb2'
  # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.ReplayParkedResp)
  })
_sym_db.RegisterMessage(ReplayParkedResp)

ListReq = _reflection.GeneratedProtocolMessageType('ListReq', (_message.Message,), {

  'Options' : _reflection.GeneratedProtocolMessageType('Options', (_message.Message,), {
    'DESCRIPTOR' : _LISTREQ_OPTIONS,
    '__module__' : 'persistent_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.ListReq.Options)
    })
  ,

  'StreamOption' : _reflection.GeneratedProtocolMessageType('StreamOption', (_message.Message,), {
    'DESCRIPTOR' : _LISTREQ_STREAMOPTION,
    '__module__' : 'persistent_pb2'
    # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.ListReq.StreamOption)
    })
  ,
  'DESCRIPTOR' : _LISTREQ,
  '__module__' : 'persistent_pb2'
  # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.ListReq)
  })
_sym_db.RegisterMessage(ListReq)
_sym_db.RegisterMessage(ListReq.Options)
_sym_db.RegisterMessage(ListReq.StreamOption)

ListResp = _reflection.GeneratedProtocolMessageType('ListResp', (_message.Message,), {
  'DESCRIPTOR' : _LISTRESP,
  '__module__' : 'persistent_pb2'
  # @@protoc_insertion_point(class_scope:event_store.client.persistent_subscriptions.ListResp)
  })
_sym_db.RegisterMessage(ListResp)

_PERSISTENTSUBSCRIPTIONS = DESCRIPTOR.services_by_name['PersistentSubscriptions']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n5com.eventstore.dbclient.proto.persistentsubscriptions'
  _READRESP_READEVENT_RECORDEDEVENT_METADATAENTRY._options = None
  _READRESP_READEVENT_RECORDEDEVENT_METADATAENTRY._serialized_options = b'8\001'
  _CREATEREQ_OPTIONS.fields_by_name['stream_identifier']._options = None
  _CREATEREQ_OPTIONS.fields_by_name['stream_identifier']._serialized_options = b'\030\001'
  _CREATEREQ_SETTINGS.fields_by_name['revision']._options = None
  _CREATEREQ_SETTINGS.fields_by_name['revision']._serialized_options = b'\030\001'
  _CREATEREQ_SETTINGS.fields_by_name['named_consumer_strategy']._options = None
  _CREATEREQ_SETTINGS.fields_by_name['named_consumer_strategy']._serialized_options = b'\030\001'
  _UPDATEREQ_OPTIONS.fields_by_name['stream_identifier']._options = None
  _UPDATEREQ_OPTIONS.fields_by_name['stream_identifier']._serialized_options = b'\030\001'
  _UPDATEREQ_SETTINGS.fields_by_name['revision']._options = None
  _UPDATEREQ_SETTINGS.fields_by_name['revision']._serialized_options = b'\030\001'
  _READREQ._serialized_start=80
  _READREQ._serialized_end=1001
  _READREQ_OPTIONS._serialized_start=321
  _READREQ_OPTIONS._serialized_end=710
  _READREQ_OPTIONS_UUIDOPTION._serialized_start=576
  _READREQ_OPTIONS_UUIDOPTION._serialized_end=693
  _READREQ_ACK._serialized_start=712
  _READREQ_ACK._serialized_end=768
  _READREQ_NACK._serialized_start=771
  _READREQ_NACK._serialized_end=990
  _READREQ_NACK_ACTION._serialized_start=928
  _READREQ_NACK_ACTION._serialized_end=990
  _READRESP._serialized_start=1004
  _READRESP._serialized_end=2048
  _READRESP_READEVENT._serialized_start=1216
  _READRESP_READEVENT._serialized_end=1984
  _READRESP_READEVENT_RECORDEDEVENT._serialized_start=1570
  _READRESP_READEVENT_RECORDEDEVENT._serialized_end=1963
  _READRESP_READEVENT_RECORDEDEVENT_METADATAENTRY._serialized_start=1916
  _READRESP_READEVENT_RECORDEDEVENT_METADATAENTRY._serialized_end=1963
  _READRESP_SUBSCRIPTIONCONFIRMATION._serialized_start=1986
  _READRESP_SUBSCRIPTIONCONFIRMATION._serialized_end=2037
  _CREATEREQ._serialized_start=2051
  _CREATEREQ._serialized_end=4217
  _CREATEREQ_OPTIONS._serialized_start=2146
  _CREATEREQ_OPTIONS._serialized_end=2514
  _CREATEREQ_STREAMOPTIONS._serialized_start=2517
  _CREATEREQ_STREAMOPTIONS._serialized_end=2722
  _CREATEREQ_ALLOPTIONS._serialized_start=2725
  _CREATEREQ_ALLOPTIONS._serialized_end=3501
  _CREATEREQ_ALLOPTIONS_FILTEROPTIONS._serialized_start=3058
  _CREATEREQ_ALLOPTIONS_FILTEROPTIONS._serialized_end=3470
  _CREATEREQ_ALLOPTIONS_FILTEROPTIONS_EXPRESSION._serialized_start=3407
  _CREATEREQ_ALLOPTIONS_FILTEROPTIONS_EXPRESSION._serialized_end=3450
  _CREATEREQ_POSITION._serialized_start=3503
  _CREATEREQ_POSITION._serialized_end=3564
  _CREATEREQ_SETTINGS._serialized_start=3567
  _CREATEREQ_SETTINGS._serialized_end=4147
  _CREATEREQ_CONSUMERSTRATEGY._serialized_start=4149
  _CREATEREQ_CONSUMERSTRATEGY._serialized_end=4217
  _CREATERESP._serialized_start=4219
  _CREATERESP._serialized_end=4231
  _UPDATEREQ._serialized_start=4234
  _UPDATEREQ._serialized_end=5790
  _UPDATEREQ_OPTIONS._serialized_start=4329
  _UPDATEREQ_OPTIONS._serialized_end=4697
  _UPDATEREQ_STREAMOPTIONS._serialized_start=2517
  _UPDATEREQ_STREAMOPTIONS._serialized_end=2722
  _UPDATEREQ_ALLOPTIONS._serialized_start=4908
  _UPDATEREQ_ALLOPTIONS._serialized_end=5105
  _UPDATEREQ_POSITION._serialized_start=3503
  _UPDATEREQ_POSITION._serialized_end=3564
  _UPDATEREQ_SETTINGS._serialized_start=5171
  _UPDATEREQ_SETTINGS._serialized_end=5720
  _UPDATEREQ_CONSUMERSTRATEGY._serialized_start=4149
  _UPDATEREQ_CONSUMERSTRATEGY._serialized_end=4217
  _UPDATERESP._serialized_start=5792
  _UPDATERESP._serialized_end=5804
  _DELETEREQ._serialized_start=5807
  _DELETEREQ._serialized_end=6057
  _DELETEREQ_OPTIONS._serialized_start=5902
  _DELETEREQ_OPTIONS._serialized_end=6057
  _DELETERESP._serialized_start=6059
  _DELETERESP._serialized_end=6071
  _GETINFOREQ._serialized_start=6074
  _GETINFOREQ._serialized_end=6326
  _GETINFOREQ_OPTIONS._serialized_start=6171
  _GETINFOREQ_OPTIONS._serialized_end=6326
  _GETINFORESP._serialized_start=6328
  _GETINFORESP._serialized_end=6431
  _SUBSCRIPTIONINFO._serialized_start=6434
  _SUBSCRIPTIONINFO._serialized_end=7698
  _SUBSCRIPTIONINFO_CONNECTIONINFO._serialized_start=7330
  _SUBSCRIPTIONINFO_CONNECTIONINFO._serialized_end=7655
  _SUBSCRIPTIONINFO_MEASUREMENT._serialized_start=7657
  _SUBSCRIPTIONINFO_MEASUREMENT._serialized_end=7698
  _REPLAYPARKEDREQ._serialized_start=7701
  _REPLAYPARKEDREQ._serialized_end=8047
  _REPLAYPARKEDREQ_OPTIONS._serialized_start=7808
  _REPLAYPARKEDREQ_OPTIONS._serialized_end=8047
  _REPLAYPARKEDRESP._serialized_start=8049
  _REPLAYPARKEDRESP._serialized_end=8067
  _LISTREQ._serialized_start=8070
  _LISTREQ._serialized_end=8472
  _LISTREQ_OPTIONS._serialized_start=8161
  _LISTREQ_OPTIONS._serialized_end=8340
  _LISTREQ_STREAMOPTION._serialized_start=8343
  _LISTREQ_STREAMOPTION._serialized_end=8472
  _LISTRESP._serialized_start=8474
  _LISTRESP._serialized_end=8570
  _PERSISTENTSUBSCRIPTIONS._serialized_start=8573
  _PERSISTENTSUBSCRIPTIONS._serialized_end=9547
# @@protoc_insertion_point(module_scope)
