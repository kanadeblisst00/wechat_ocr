# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: ocr_protobuf.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12ocr_protobuf.proto\x12\x0cocr_protobuf\"\xa8\x06\n\x0bOcrResponse\x12\x0c\n\x04type\x18\x01 \x01(\x05\x12\x0f\n\x07task_id\x18\x02 \x01(\x05\x12\x10\n\x08\x65rr_code\x18\x03 \x01(\x05\x12\x37\n\nocr_result\x18\x04 \x01(\x0b\x32#.ocr_protobuf.OcrResponse.OcrResult\x1a\xae\x05\n\tOcrResult\x12G\n\rsingle_result\x18\x01 \x03(\x0b\x32\x30.ocr_protobuf.OcrResponse.OcrResult.SingleResult\x12\x11\n\tunknown_1\x18\x02 \x01(\x05\x12\x11\n\tunknown_2\x18\x03 \x01(\x05\x1al\n\tResultPos\x12@\n\x03pos\x18\x01 \x03(\x0b\x32\x33.ocr_protobuf.OcrResponse.OcrResult.ResultPos.PosXY\x1a\x1d\n\x05PosXY\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\x1a\xc3\x03\n\x0cSingleResult\x12\x41\n\nsingle_pos\x18\x01 \x01(\x0b\x32-.ocr_protobuf.OcrResponse.OcrResult.ResultPos\x12\x17\n\x0fsingle_str_utf8\x18\x02 \x01(\x0c\x12\x13\n\x0bsingle_rate\x18\x03 \x01(\x02\x12N\n\none_result\x18\x04 \x03(\x0b\x32:.ocr_protobuf.OcrResponse.OcrResult.SingleResult.OneResult\x12\x0c\n\x04left\x18\x05 \x01(\x02\x12\x0b\n\x03top\x18\x06 \x01(\x02\x12\r\n\x05right\x18\x07 \x01(\x02\x12\x0e\n\x06\x62ottom\x18\x08 \x01(\x02\x12\x11\n\tunknown_0\x18\t \x01(\x05\x12\x42\n\x0bunknown_pos\x18\n \x01(\x0b\x32-.ocr_protobuf.OcrResponse.OcrResult.ResultPos\x1a\x61\n\tOneResult\x12>\n\x07one_pos\x18\x01 \x01(\x0b\x32-.ocr_protobuf.OcrResponse.OcrResult.ResultPos\x12\x14\n\x0cone_str_utf8\x18\x02 \x01(\x0c\"\x80\x01\n\nOcrRequest\x12\x0e\n\x06unknow\x18\x01 \x01(\x05\x12\x0f\n\x07task_id\x18\x02 \x01(\x05\x12\x33\n\x08pic_path\x18\x03 \x01(\x0b\x32!.ocr_protobuf.OcrRequest.PicPaths\x1a\x1c\n\x08PicPaths\x12\x10\n\x08pic_path\x18\x01 \x03(\tb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ocr_protobuf_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _OCRRESPONSE._serialized_start=37
  _OCRRESPONSE._serialized_end=845
  _OCRRESPONSE_OCRRESULT._serialized_start=159
  _OCRRESPONSE_OCRRESULT._serialized_end=845
  _OCRRESPONSE_OCRRESULT_RESULTPOS._serialized_start=283
  _OCRRESPONSE_OCRRESULT_RESULTPOS._serialized_end=391
  _OCRRESPONSE_OCRRESULT_RESULTPOS_POSXY._serialized_start=362
  _OCRRESPONSE_OCRRESULT_RESULTPOS_POSXY._serialized_end=391
  _OCRRESPONSE_OCRRESULT_SINGLERESULT._serialized_start=394
  _OCRRESPONSE_OCRRESULT_SINGLERESULT._serialized_end=845
  _OCRRESPONSE_OCRRESULT_SINGLERESULT_ONERESULT._serialized_start=748
  _OCRRESPONSE_OCRRESULT_SINGLERESULT_ONERESULT._serialized_end=845
  _OCRREQUEST._serialized_start=848
  _OCRREQUEST._serialized_end=976
  _OCRREQUEST_PICPATHS._serialized_start=948
  _OCRREQUEST_PICPATHS._serialized_end=976
# @@protoc_insertion_point(module_scope)
