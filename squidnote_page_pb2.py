# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: squidnote_page.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14squidnote_page.proto\"]\n\x0bSN_BG_Ruled\x12\x14\n\x0cline_spacing\x18\x01 \x01(\x02\x12\x0e\n\x06margin\x18\x02 \x01(\x02\x12\x13\n\x0bshow_margin\x18\x03 \x01(\x08\x12\x13\n\x0bline_weight\x18\x04 \x01(\x02\"\x0c\n\nSN_BG_Quad\"\r\n\x0bSN_BG_Blank\"@\n\tSN_BG_PDF\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\nimage_hash\x18\x02 \x01(\t\x12\x13\n\x0bpage_number\x18\x03 \x01(\r\"\r\n\x0bSN_BG_Papyr\"\x91\x02\n\rSN_Background\x12!\n\x04type\x18\x01 \x01(\x0e\x32\x13.SN_Background_Type\x12\n\n\x02id\x18\x02 \x01(\t\x12\x12\n\nimage_hash\x18\x03 \x01(\t\x12\r\n\x05width\x18\x04 \x01(\x02\x12\x0e\n\x06height\x18\x05 \x01(\x02\x12\x0e\n\x06\x63olour\x18\x06 \x01(\r\x12\x1c\n\x05ruled\x18\xe8\x07 \x01(\x0b\x32\x0c.SN_BG_Ruled\x12\x1a\n\x04quad\x18\xe9\x07 \x01(\x0b\x32\x0b.SN_BG_Quad\x12\x1c\n\x05\x62lank\x18\xea\x07 \x01(\x0b\x32\x0c.SN_BG_Blank\x12\x18\n\x03pdf\x18\xeb\x07 \x01(\x0b\x32\n.SN_BG_PDF\x12\x1c\n\x05papyr\x18\xec\x07 \x01(\x0b\x32\x0c.SN_BG_Papyr\"\x1d\n\x05SN_SP\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\"/\n\x05SN_DP\x12\n\n\x02\x64x\x18\x01 \x01(\x02\x12\n\n\x02\x64y\x18\x02 \x01(\x02\x12\x0e\n\x06weight\x18\x03 \x01(\x02\"C\n\x07SN_Rect\x12\x0c\n\x04left\x18\x01 \x01(\x05\x12\r\n\x05right\x18\x02 \x01(\x05\x12\x0b\n\x03top\x18\x03 \x01(\x05\x12\x0e\n\x06\x62ottom\x18\x04 \x01(\x05\"D\n\x08SN_RectF\x12\x0c\n\x04left\x18\x01 \x01(\x02\x12\r\n\x05right\x18\x02 \x01(\x02\x12\x0b\n\x03top\x18\x03 \x01(\x02\x12\x0e\n\x06\x62ottom\x18\x04 \x01(\x02\"\xb0\x01\n\tSN_Stroke\x12\x0e\n\x06\x63olour\x18\x01 \x01(\r\x12\x0e\n\x06weight\x18\x02 \x01(\x02\x12\x15\n\x05start\x18\x03 \x01(\x0b\x32\x06.SN_SP\x12\x15\n\x05\x64\x65lta\x18\x04 \x03(\x0b\x32\x06.SN_DP\x12\x19\n\x06\x62ounds\x18\x05 \x01(\x0b\x32\t.SN_RectF\x12\x1d\n\x04type\x18\x06 \x01(\x0e\x32\x0f.SN_Stroke_Type\x12\x1b\n\x08\x66_bounds\x18\x07 \x01(\x0b\x32\t.SN_RectF\"\n\n\x08SN_Shape\"\t\n\x07SN_Text\"\x96\x01\n\x08SN_Image\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\nimage_hash\x18\x02 \x01(\t\x12\x19\n\x06\x62ounds\x18\x03 \x01(\x0b\x32\t.SN_RectF\x12\x0e\n\x06\x66lip_x\x18\x04 \x01(\x08\x12\x0e\n\x06\x66lip_y\x18\x05 \x01(\x08\x12\x1d\n\x0b\x63rop_bounds\x18\x06 \x01(\x0b\x32\x08.SN_Rect\x12\x10\n\x08rotation\x18\x07 \x01(\x05\"\x0c\n\nSN_Ellipse\"\xa2\x01\n\x07SN_Item\x12\x1b\n\x04type\x18\x01 \x01(\x0e\x32\r.SN_Item_Type\x12\x1d\n\x06stroke\x18\xe8\x07 \x01(\x0b\x32\n.SN_StrokeH\x00\x12\x1b\n\x05shape\x18\xe9\x07 \x01(\x0b\x32\t.SN_ShapeH\x00\x12\x19\n\x04text\x18\xea\x07 \x01(\x0b\x32\x08.SN_TextH\x00\x12\x1b\n\x05image\x18\xeb\x07 \x01(\x0b\x32\t.SN_ImageH\x00\x42\x06\n\x04item\"?\n\x08SN_Layer\x12\x16\n\x04item\x18\x01 \x03(\x0b\x32\x08.SN_Item\x12\x1b\n\x08\x66_bounds\x18\x02 \x01(\x0b\x32\t.SN_RectF\"G\n\x07SN_Page\x12\"\n\nbackground\x18\x01 \x01(\x0b\x32\x0e.SN_Background\x12\x18\n\x05layer\x18\x03 \x03(\x0b\x32\t.SN_Layer*\x85\x01\n\x12SN_Background_Type\x12\x13\n\x0fSN_BT_UNDEFINED\x10\x00\x12\x14\n\x10SN_BT_RULEDPAPER\x10\x01\x12\x13\n\x0fSN_BT_QUADPAPER\x10\x02\x12\x0f\n\x0bSN_BT_BLANK\x10\x03\x12\r\n\tSN_BT_PDF\x10\x04\x12\x0f\n\x0bSN_BT_PAPYR\x10\x05*n\n\x0eSN_Stroke_Type\x12\x13\n\x0fSN_ST_UNDEFINED\x10\x00\x12\x10\n\x0cSN_ST_NORMAL\x10\x01\x12\x0e\n\nSN_ST_LINE\x10\x02\x12\x13\n\x0fSN_ST_HIGHLIGHT\x10\x03\x12\x10\n\x0cSN_ST_SMOOTH\x10\x04*g\n\x0cSN_Item_Type\x12\x13\n\x0fSN_IT_UNDEFINED\x10\x00\x12\x10\n\x0cSN_IT_STROKE\x10\x01\x12\x0f\n\x0bSN_IT_SHAPE\x10\x02\x12\x0e\n\nSN_IT_TEXT\x10\x03\x12\x0f\n\x0bSN_IT_IMAGE\x10\x04\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'squidnote_page_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_SN_BACKGROUND_TYPE']._serialized_start=1397
  _globals['_SN_BACKGROUND_TYPE']._serialized_end=1530
  _globals['_SN_STROKE_TYPE']._serialized_start=1532
  _globals['_SN_STROKE_TYPE']._serialized_end=1642
  _globals['_SN_ITEM_TYPE']._serialized_start=1644
  _globals['_SN_ITEM_TYPE']._serialized_end=1747
  _globals['_SN_BG_RULED']._serialized_start=24
  _globals['_SN_BG_RULED']._serialized_end=117
  _globals['_SN_BG_QUAD']._serialized_start=119
  _globals['_SN_BG_QUAD']._serialized_end=131
  _globals['_SN_BG_BLANK']._serialized_start=133
  _globals['_SN_BG_BLANK']._serialized_end=146
  _globals['_SN_BG_PDF']._serialized_start=148
  _globals['_SN_BG_PDF']._serialized_end=212
  _globals['_SN_BG_PAPYR']._serialized_start=214
  _globals['_SN_BG_PAPYR']._serialized_end=227
  _globals['_SN_BACKGROUND']._serialized_start=230
  _globals['_SN_BACKGROUND']._serialized_end=503
  _globals['_SN_SP']._serialized_start=505
  _globals['_SN_SP']._serialized_end=534
  _globals['_SN_DP']._serialized_start=536
  _globals['_SN_DP']._serialized_end=583
  _globals['_SN_RECT']._serialized_start=585
  _globals['_SN_RECT']._serialized_end=652
  _globals['_SN_RECTF']._serialized_start=654
  _globals['_SN_RECTF']._serialized_end=722
  _globals['_SN_STROKE']._serialized_start=725
  _globals['_SN_STROKE']._serialized_end=901
  _globals['_SN_SHAPE']._serialized_start=903
  _globals['_SN_SHAPE']._serialized_end=913
  _globals['_SN_TEXT']._serialized_start=915
  _globals['_SN_TEXT']._serialized_end=924
  _globals['_SN_IMAGE']._serialized_start=927
  _globals['_SN_IMAGE']._serialized_end=1077
  _globals['_SN_ELLIPSE']._serialized_start=1079
  _globals['_SN_ELLIPSE']._serialized_end=1091
  _globals['_SN_ITEM']._serialized_start=1094
  _globals['_SN_ITEM']._serialized_end=1256
  _globals['_SN_LAYER']._serialized_start=1258
  _globals['_SN_LAYER']._serialized_end=1321
  _globals['_SN_PAGE']._serialized_start=1323
  _globals['_SN_PAGE']._serialized_end=1394
# @@protoc_insertion_point(module_scope)
