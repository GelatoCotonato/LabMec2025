// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from custom_interface:msg/CustomMsg.idl
// generated code does not contain a copyright notice
#include "custom_interface/msg/detail/custom_msg__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
custom_interface__msg__CustomMsg__init(custom_interface__msg__CustomMsg * msg)
{
  if (!msg) {
    return false;
  }
  // index
  // name
  return true;
}

void
custom_interface__msg__CustomMsg__fini(custom_interface__msg__CustomMsg * msg)
{
  if (!msg) {
    return;
  }
  // index
  // name
}

bool
custom_interface__msg__CustomMsg__are_equal(const custom_interface__msg__CustomMsg * lhs, const custom_interface__msg__CustomMsg * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // index
  if (lhs->index != rhs->index) {
    return false;
  }
  // name
  if (lhs->name != rhs->name) {
    return false;
  }
  return true;
}

bool
custom_interface__msg__CustomMsg__copy(
  const custom_interface__msg__CustomMsg * input,
  custom_interface__msg__CustomMsg * output)
{
  if (!input || !output) {
    return false;
  }
  // index
  output->index = input->index;
  // name
  output->name = input->name;
  return true;
}

custom_interface__msg__CustomMsg *
custom_interface__msg__CustomMsg__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  custom_interface__msg__CustomMsg * msg = (custom_interface__msg__CustomMsg *)allocator.allocate(sizeof(custom_interface__msg__CustomMsg), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(custom_interface__msg__CustomMsg));
  bool success = custom_interface__msg__CustomMsg__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
custom_interface__msg__CustomMsg__destroy(custom_interface__msg__CustomMsg * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    custom_interface__msg__CustomMsg__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
custom_interface__msg__CustomMsg__Sequence__init(custom_interface__msg__CustomMsg__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  custom_interface__msg__CustomMsg * data = NULL;

  if (size) {
    data = (custom_interface__msg__CustomMsg *)allocator.zero_allocate(size, sizeof(custom_interface__msg__CustomMsg), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = custom_interface__msg__CustomMsg__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        custom_interface__msg__CustomMsg__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
custom_interface__msg__CustomMsg__Sequence__fini(custom_interface__msg__CustomMsg__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      custom_interface__msg__CustomMsg__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

custom_interface__msg__CustomMsg__Sequence *
custom_interface__msg__CustomMsg__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  custom_interface__msg__CustomMsg__Sequence * array = (custom_interface__msg__CustomMsg__Sequence *)allocator.allocate(sizeof(custom_interface__msg__CustomMsg__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = custom_interface__msg__CustomMsg__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
custom_interface__msg__CustomMsg__Sequence__destroy(custom_interface__msg__CustomMsg__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    custom_interface__msg__CustomMsg__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
custom_interface__msg__CustomMsg__Sequence__are_equal(const custom_interface__msg__CustomMsg__Sequence * lhs, const custom_interface__msg__CustomMsg__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!custom_interface__msg__CustomMsg__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
custom_interface__msg__CustomMsg__Sequence__copy(
  const custom_interface__msg__CustomMsg__Sequence * input,
  custom_interface__msg__CustomMsg__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(custom_interface__msg__CustomMsg);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    custom_interface__msg__CustomMsg * data =
      (custom_interface__msg__CustomMsg *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!custom_interface__msg__CustomMsg__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          custom_interface__msg__CustomMsg__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!custom_interface__msg__CustomMsg__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
