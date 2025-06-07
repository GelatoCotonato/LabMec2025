// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from custom_interface:msg/CustomMsg.idl
// generated code does not contain a copyright notice

#include "custom_interface/msg/detail/custom_msg__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_custom_interface
const rosidl_type_hash_t *
custom_interface__msg__CustomMsg__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x1b, 0x50, 0x11, 0x4a, 0x6a, 0x3d, 0x85, 0x0b,
      0x97, 0x03, 0x1d, 0x09, 0x80, 0x06, 0x35, 0xca,
      0xae, 0xa5, 0x6a, 0xfe, 0xe3, 0xae, 0x92, 0xb1,
      0xf6, 0xb3, 0x38, 0xda, 0x9d, 0x5f, 0xc7, 0xaf,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char custom_interface__msg__CustomMsg__TYPE_NAME[] = "custom_interface/msg/CustomMsg";

// Define type names, field names, and default values
static char custom_interface__msg__CustomMsg__FIELD_NAME__index[] = "index";
static char custom_interface__msg__CustomMsg__FIELD_NAME__name[] = "name";

static rosidl_runtime_c__type_description__Field custom_interface__msg__CustomMsg__FIELDS[] = {
  {
    {custom_interface__msg__CustomMsg__FIELD_NAME__index, 5, 5},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT64,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {custom_interface__msg__CustomMsg__FIELD_NAME__name, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_UINT8,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
custom_interface__msg__CustomMsg__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {custom_interface__msg__CustomMsg__TYPE_NAME, 30, 30},
      {custom_interface__msg__CustomMsg__FIELDS, 2, 2},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "\n"
  "int64 index\n"
  "\n"
  "char name";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
custom_interface__msg__CustomMsg__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {custom_interface__msg__CustomMsg__TYPE_NAME, 30, 30},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 24, 24},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
custom_interface__msg__CustomMsg__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *custom_interface__msg__CustomMsg__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
