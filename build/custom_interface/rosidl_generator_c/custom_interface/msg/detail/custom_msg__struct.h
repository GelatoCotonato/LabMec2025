// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from custom_interface:msg/CustomMsg.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "custom_interface/msg/custom_msg.h"


#ifndef CUSTOM_INTERFACE__MSG__DETAIL__CUSTOM_MSG__STRUCT_H_
#define CUSTOM_INTERFACE__MSG__DETAIL__CUSTOM_MSG__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

/// Struct defined in msg/CustomMsg in the package custom_interface.
typedef struct custom_interface__msg__CustomMsg
{
  int64_t index;
  uint8_t name;
} custom_interface__msg__CustomMsg;

// Struct for a sequence of custom_interface__msg__CustomMsg.
typedef struct custom_interface__msg__CustomMsg__Sequence
{
  custom_interface__msg__CustomMsg * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_interface__msg__CustomMsg__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CUSTOM_INTERFACE__MSG__DETAIL__CUSTOM_MSG__STRUCT_H_
