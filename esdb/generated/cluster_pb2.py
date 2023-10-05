# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: cluster.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import shared_pb2 as shared__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rcluster.proto\x12\x13\x65vent_store.cluster\x1a\x0cshared.proto\"n\n\rGossipRequest\x12.\n\x04info\x18\x01 \x01(\x0b\x32 .event_store.cluster.ClusterInfo\x12-\n\x06server\x18\x02 \x01(\x0b\x32\x1d.event_store.cluster.EndPoint\"\x8c\x01\n\x11ViewChangeRequest\x12+\n\tserver_id\x18\x01 \x01(\x0b\x32\x18.event_store.client.UUID\x12\x32\n\x0bserver_http\x18\x02 \x01(\x0b\x32\x1d.event_store.cluster.EndPoint\x12\x16\n\x0e\x61ttempted_view\x18\x03 \x01(\x05\"\x91\x01\n\x16ViewChangeProofRequest\x12+\n\tserver_id\x18\x01 \x01(\x0b\x32\x18.event_store.client.UUID\x12\x32\n\x0bserver_http\x18\x02 \x01(\x0b\x32\x1d.event_store.cluster.EndPoint\x12\x16\n\x0einstalled_view\x18\x03 \x01(\x05\"\x7f\n\x0ePrepareRequest\x12+\n\tserver_id\x18\x01 \x01(\x0b\x32\x18.event_store.client.UUID\x12\x32\n\x0bserver_http\x18\x02 \x01(\x0b\x32\x1d.event_store.cluster.EndPoint\x12\x0c\n\x04view\x18\x03 \x01(\x05\"\xba\x03\n\x10PrepareOkRequest\x12\x0c\n\x04view\x18\x01 \x01(\x05\x12+\n\tserver_id\x18\x02 \x01(\x0b\x32\x18.event_store.client.UUID\x12\x32\n\x0bserver_http\x18\x03 \x01(\x0b\x32\x1d.event_store.cluster.EndPoint\x12\x14\n\x0c\x65poch_number\x18\x04 \x01(\x05\x12\x16\n\x0e\x65poch_position\x18\x05 \x01(\x03\x12*\n\x08\x65poch_id\x18\x06 \x01(\x0b\x32\x18.event_store.client.UUID\x12:\n\x18\x65poch_leader_instance_id\x18\x07 \x01(\x0b\x32\x18.event_store.client.UUID\x12\x1c\n\x14last_commit_position\x18\x08 \x01(\x03\x12\x19\n\x11writer_checkpoint\x18\t \x01(\x03\x12\x19\n\x11\x63haser_checkpoint\x18\n \x01(\x03\x12\x15\n\rnode_priority\x18\x0b \x01(\x05\x12\x36\n\x0c\x63luster_info\x18\x0c \x01(\x0b\x32 .event_store.cluster.ClusterInfo\"\xe2\x03\n\x0fProposalRequest\x12+\n\tserver_id\x18\x01 \x01(\x0b\x32\x18.event_store.client.UUID\x12\x32\n\x0bserver_http\x18\x02 \x01(\x0b\x32\x1d.event_store.cluster.EndPoint\x12+\n\tleader_id\x18\x03 \x01(\x0b\x32\x18.event_store.client.UUID\x12\x32\n\x0bleader_http\x18\x04 \x01(\x0b\x32\x1d.event_store.cluster.EndPoint\x12\x0c\n\x04view\x18\x05 \x01(\x05\x12\x14\n\x0c\x65poch_number\x18\x06 \x01(\x05\x12\x16\n\x0e\x65poch_position\x18\x07 \x01(\x03\x12*\n\x08\x65poch_id\x18\x08 \x01(\x0b\x32\x18.event_store.client.UUID\x12:\n\x18\x65poch_leader_instance_id\x18\t \x01(\x0b\x32\x18.event_store.client.UUID\x12\x1c\n\x14last_commit_position\x18\n \x01(\x03\x12\x19\n\x11writer_checkpoint\x18\x0b \x01(\x03\x12\x19\n\x11\x63haser_checkpoint\x18\x0c \x01(\x03\x12\x15\n\rnode_priority\x18\r \x01(\x05\"\xdf\x01\n\rAcceptRequest\x12+\n\tserver_id\x18\x01 \x01(\x0b\x32\x18.event_store.client.UUID\x12\x32\n\x0bserver_http\x18\x02 \x01(\x0b\x32\x1d.event_store.cluster.EndPoint\x12+\n\tleader_id\x18\x03 \x01(\x0b\x32\x18.event_store.client.UUID\x12\x32\n\x0bleader_http\x18\x04 \x01(\x0b\x32\x1d.event_store.cluster.EndPoint\x12\x0c\n\x04view\x18\x05 \x01(\x05\"{\n\x18LeaderIsResigningRequest\x12+\n\tleader_id\x18\x01 \x01(\x0b\x32\x18.event_store.client.UUID\x12\x32\n\x0bleader_http\x18\x02 \x01(\x0b\x32\x1d.event_store.cluster.EndPoint\"\xde\x01\n\x1aLeaderIsResigningOkRequest\x12+\n\tleader_id\x18\x01 \x01(\x0b\x32\x18.event_store.client.UUID\x12\x32\n\x0bleader_http\x18\x02 \x01(\x0b\x32\x1d.event_store.cluster.EndPoint\x12+\n\tserver_id\x18\x03 \x01(\x0b\x32\x18.event_store.client.UUID\x12\x32\n\x0bserver_http\x18\x04 \x01(\x0b\x32\x1d.event_store.cluster.EndPoint\"?\n\x0b\x43lusterInfo\x12\x30\n\x07members\x18\x01 \x03(\x0b\x32\x1f.event_store.cluster.MemberInfo\")\n\x08\x45ndPoint\x12\x0f\n\x07\x61\x64\x64ress\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\r\"\xf3\x07\n\nMemberInfo\x12-\n\x0binstance_id\x18\x01 \x01(\x0b\x32\x18.event_store.client.UUID\x12\x12\n\ntime_stamp\x18\x02 \x01(\x03\x12\x39\n\x05state\x18\x03 \x01(\x0e\x32*.event_store.cluster.MemberInfo.VNodeState\x12\x10\n\x08is_alive\x18\x04 \x01(\x08\x12\x35\n\x0ehttp_end_point\x18\x05 \x01(\x0b\x32\x1d.event_store.cluster.EndPoint\x12\x33\n\x0cinternal_tcp\x18\x06 \x01(\x0b\x32\x1d.event_store.cluster.EndPoint\x12\x33\n\x0c\x65xternal_tcp\x18\x07 \x01(\x0b\x32\x1d.event_store.cluster.EndPoint\x12\x1d\n\x15internal_tcp_uses_tls\x18\x08 \x01(\x08\x12\x1d\n\x15\x65xternal_tcp_uses_tls\x18\t \x01(\x08\x12\x1c\n\x14last_commit_position\x18\n \x01(\x03\x12\x19\n\x11writer_checkpoint\x18\x0b \x01(\x03\x12\x19\n\x11\x63haser_checkpoint\x18\x0c \x01(\x03\x12\x16\n\x0e\x65poch_position\x18\r \x01(\x03\x12\x14\n\x0c\x65poch_number\x18\x0e \x01(\x05\x12*\n\x08\x65poch_id\x18\x0f \x01(\x0b\x32\x18.event_store.client.UUID\x12\x15\n\rnode_priority\x18\x10 \x01(\x05\x12\x1c\n\x14is_read_only_replica\x18\x11 \x01(\x08\x12#\n\x1b\x61\x64vertise_host_to_client_as\x18\x12 \x01(\t\x12(\n advertise_http_port_to_client_as\x18\x13 \x01(\r\x12\'\n\x1f\x61\x64vertise_tcp_port_to_client_as\x18\x14 \x01(\r\"\x9a\x02\n\nVNodeState\x12\x10\n\x0cInitializing\x10\x00\x12\x12\n\x0e\x44iscoverLeader\x10\x01\x12\x0b\n\x07Unknown\x10\x02\x12\x0e\n\nPreReplica\x10\x03\x12\x0e\n\nCatchingUp\x10\x04\x12\t\n\x05\x43lone\x10\x05\x12\x0c\n\x08\x46ollower\x10\x06\x12\r\n\tPreLeader\x10\x07\x12\n\n\x06Leader\x10\x08\x12\x0b\n\x07Manager\x10\t\x12\x10\n\x0cShuttingDown\x10\n\x12\x0c\n\x08Shutdown\x10\x0b\x12\x16\n\x12ReadOnlyLeaderless\x10\x0c\x12\x16\n\x12PreReadOnlyReplica\x10\r\x12\x13\n\x0fReadOnlyReplica\x10\x0e\x12\x13\n\x0fResigningLeader\x10\x0f\";\n\x0fReplicaLogWrite\x12\x14\n\x0clog_position\x18\x01 \x01(\x03\x12\x12\n\nreplica_id\x18\x02 \x01(\x0c\"$\n\x0cReplicatedTo\x12\x14\n\x0clog_position\x18\x01 \x01(\x03\"G\n\x05\x45poch\x12\x16\n\x0e\x65poch_position\x18\x01 \x01(\x03\x12\x14\n\x0c\x65poch_number\x18\x02 \x01(\x05\x12\x10\n\x08\x65poch_id\x18\x03 \x01(\x0c\"\xd8\x01\n\x10SubscribeReplica\x12\x14\n\x0clog_position\x18\x01 \x01(\x03\x12\x10\n\x08\x63hunk_id\x18\x02 \x01(\x0c\x12.\n\nLastEpochs\x18\x03 \x03(\x0b\x32\x1a.event_store.cluster.Epoch\x12\n\n\x02ip\x18\x04 \x01(\x0c\x12\x0c\n\x04port\x18\x05 \x01(\x05\x12\x11\n\tleader_id\x18\x06 \x01(\x0c\x12\x17\n\x0fsubscription_id\x18\x07 \x01(\x0c\x12\x15\n\ris_promotable\x18\x08 \x01(\x08\x12\x0f\n\x07version\x18\t \x01(\x05\"F\n\x18ReplicaSubscriptionRetry\x12\x11\n\tleader_id\x18\x01 \x01(\x0c\x12\x17\n\x0fsubscription_id\x18\x02 \x01(\x0c\"^\n\x11ReplicaSubscribed\x12\x11\n\tleader_id\x18\x01 \x01(\x0c\x12\x17\n\x0fsubscription_id\x18\x02 \x01(\x0c\x12\x1d\n\x15subscription_position\x18\x03 \x01(\x03\"o\n\x15ReplicaLogPositionAck\x12\x17\n\x0fsubscription_id\x18\x01 \x01(\x0c\x12 \n\x18replication_log_position\x18\x02 \x01(\x03\x12\x1b\n\x13writer_log_position\x18\x03 \x01(\x03\"\x84\x01\n\x0b\x43reateChunk\x12\x11\n\tleader_id\x18\x01 \x01(\x0c\x12\x17\n\x0fsubscription_id\x18\x02 \x01(\x0c\x12\x1a\n\x12\x63hunk_header_bytes\x18\x03 \x01(\x0c\x12\x11\n\tfile_size\x18\x04 \x01(\x05\x12\x1a\n\x12is_completed_chunk\x18\x05 \x01(\x08\"\xb1\x01\n\x0cRawChunkBulk\x12\x11\n\tleader_id\x18\x01 \x01(\x0c\x12\x17\n\x0fsubscription_id\x18\x02 \x01(\x0c\x12\x1a\n\x12\x63hunk_start_number\x18\x03 \x01(\x05\x12\x18\n\x10\x63hunk_end_number\x18\x04 \x01(\x05\x12\x14\n\x0craw_position\x18\x05 \x01(\x05\x12\x11\n\traw_bytes\x18\x06 \x01(\x0c\x12\x16\n\x0e\x63omplete_chunk\x18\x07 \x01(\x08\"\xbc\x01\n\rDataChunkBulk\x12\x11\n\tleader_id\x18\x01 \x01(\x0c\x12\x17\n\x0fsubscription_id\x18\x02 \x01(\x0c\x12\x1a\n\x12\x63hunk_start_number\x18\x03 \x01(\x05\x12\x18\n\x10\x63hunk_end_number\x18\x04 \x01(\x05\x12\x1d\n\x15subscription_position\x18\x05 \x01(\x03\x12\x12\n\ndata_bytes\x18\x06 \x01(\x0c\x12\x16\n\x0e\x63omplete_chunk\x18\x07 \x01(\x08\"@\n\x12\x46ollowerAssignment\x12\x11\n\tleader_id\x18\x01 \x01(\x0c\x12\x17\n\x0fsubscription_id\x18\x02 \x01(\x0c\"=\n\x0f\x43loneAssignment\x12\x11\n\tleader_id\x18\x01 \x01(\x0c\x12\x17\n\x0fsubscription_id\x18\x02 \x01(\x0c\">\n\x10\x44ropSubscription\x12\x11\n\tleader_id\x18\x01 \x01(\x0c\x12\x17\n\x0fsubscription_id\x18\x02 \x01(\x0c\x32\x9d\x01\n\x06Gossip\x12N\n\x06Update\x12\".event_store.cluster.GossipRequest\x1a .event_store.cluster.ClusterInfo\x12\x43\n\x04Read\x12\x19.event_store.client.Empty\x1a .event_store.cluster.ClusterInfo2\xa9\x05\n\tElections\x12O\n\nViewChange\x12&.event_store.cluster.ViewChangeRequest\x1a\x19.event_store.client.Empty\x12Y\n\x0fViewChangeProof\x12+.event_store.cluster.ViewChangeProofRequest\x1a\x19.event_store.client.Empty\x12I\n\x07Prepare\x12#.event_store.cluster.PrepareRequest\x1a\x19.event_store.client.Empty\x12M\n\tPrepareOk\x12%.event_store.cluster.PrepareOkRequest\x1a\x19.event_store.client.Empty\x12K\n\x08Proposal\x12$.event_store.cluster.ProposalRequest\x1a\x19.event_store.client.Empty\x12G\n\x06\x41\x63\x63\x65pt\x12\".event_store.cluster.AcceptRequest\x1a\x19.event_store.client.Empty\x12]\n\x11LeaderIsResigning\x12-.event_store.cluster.LeaderIsResigningRequest\x1a\x19.event_store.client.Empty\x12\x61\n\x13LeaderIsResigningOk\x12/.event_store.cluster.LeaderIsResigningOkRequest\x1a\x19.event_store.client.EmptyB\'\n%com.eventstore.dbclient.proto.clusterb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'cluster_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n%com.eventstore.dbclient.proto.cluster'
  _globals['_GOSSIPREQUEST']._serialized_start=52
  _globals['_GOSSIPREQUEST']._serialized_end=162
  _globals['_VIEWCHANGEREQUEST']._serialized_start=165
  _globals['_VIEWCHANGEREQUEST']._serialized_end=305
  _globals['_VIEWCHANGEPROOFREQUEST']._serialized_start=308
  _globals['_VIEWCHANGEPROOFREQUEST']._serialized_end=453
  _globals['_PREPAREREQUEST']._serialized_start=455
  _globals['_PREPAREREQUEST']._serialized_end=582
  _globals['_PREPAREOKREQUEST']._serialized_start=585
  _globals['_PREPAREOKREQUEST']._serialized_end=1027
  _globals['_PROPOSALREQUEST']._serialized_start=1030
  _globals['_PROPOSALREQUEST']._serialized_end=1512
  _globals['_ACCEPTREQUEST']._serialized_start=1515
  _globals['_ACCEPTREQUEST']._serialized_end=1738
  _globals['_LEADERISRESIGNINGREQUEST']._serialized_start=1740
  _globals['_LEADERISRESIGNINGREQUEST']._serialized_end=1863
  _globals['_LEADERISRESIGNINGOKREQUEST']._serialized_start=1866
  _globals['_LEADERISRESIGNINGOKREQUEST']._serialized_end=2088
  _globals['_CLUSTERINFO']._serialized_start=2090
  _globals['_CLUSTERINFO']._serialized_end=2153
  _globals['_ENDPOINT']._serialized_start=2155
  _globals['_ENDPOINT']._serialized_end=2196
  _globals['_MEMBERINFO']._serialized_start=2199
  _globals['_MEMBERINFO']._serialized_end=3210
  _globals['_MEMBERINFO_VNODESTATE']._serialized_start=2928
  _globals['_MEMBERINFO_VNODESTATE']._serialized_end=3210
  _globals['_REPLICALOGWRITE']._serialized_start=3212
  _globals['_REPLICALOGWRITE']._serialized_end=3271
  _globals['_REPLICATEDTO']._serialized_start=3273
  _globals['_REPLICATEDTO']._serialized_end=3309
  _globals['_EPOCH']._serialized_start=3311
  _globals['_EPOCH']._serialized_end=3382
  _globals['_SUBSCRIBEREPLICA']._serialized_start=3385
  _globals['_SUBSCRIBEREPLICA']._serialized_end=3601
  _globals['_REPLICASUBSCRIPTIONRETRY']._serialized_start=3603
  _globals['_REPLICASUBSCRIPTIONRETRY']._serialized_end=3673
  _globals['_REPLICASUBSCRIBED']._serialized_start=3675
  _globals['_REPLICASUBSCRIBED']._serialized_end=3769
  _globals['_REPLICALOGPOSITIONACK']._serialized_start=3771
  _globals['_REPLICALOGPOSITIONACK']._serialized_end=3882
  _globals['_CREATECHUNK']._serialized_start=3885
  _globals['_CREATECHUNK']._serialized_end=4017
  _globals['_RAWCHUNKBULK']._serialized_start=4020
  _globals['_RAWCHUNKBULK']._serialized_end=4197
  _globals['_DATACHUNKBULK']._serialized_start=4200
  _globals['_DATACHUNKBULK']._serialized_end=4388
  _globals['_FOLLOWERASSIGNMENT']._serialized_start=4390
  _globals['_FOLLOWERASSIGNMENT']._serialized_end=4454
  _globals['_CLONEASSIGNMENT']._serialized_start=4456
  _globals['_CLONEASSIGNMENT']._serialized_end=4517
  _globals['_DROPSUBSCRIPTION']._serialized_start=4519
  _globals['_DROPSUBSCRIPTION']._serialized_end=4581
  _globals['_GOSSIP']._serialized_start=4584
  _globals['_GOSSIP']._serialized_end=4741
  _globals['_ELECTIONS']._serialized_start=4744
  _globals['_ELECTIONS']._serialized_end=5425
# @@protoc_insertion_point(module_scope)
