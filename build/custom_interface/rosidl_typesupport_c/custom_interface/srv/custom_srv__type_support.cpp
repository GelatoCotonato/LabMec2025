// generated from rosidl_typesupport_c/resource/idl__type_support.cpp.em
// with input from custom_interface:srv/CustomSrv.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "custom_interface/srv/detail/custom_srv__struct.h"
#include "custom_interface/srv/detail/custom_srv__type_support.h"
#include "custom_interface/srv/detail/custom_srv__functions.h"
#include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/message_type_support_dispatch.h"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_c/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace custom_interface
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _CustomSrv_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _CustomSrv_Request_type_support_ids_t;

static const _CustomSrv_Request_type_support_ids_t _CustomSrv_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _CustomSrv_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _CustomSrv_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _CustomSrv_Request_type_support_symbol_names_t _CustomSrv_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, custom_interface, srv, CustomSrv_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_interface, srv, CustomSrv_Request)),
  }
};

typedef struct _CustomSrv_Request_type_support_data_t
{
  void * data[2];
} _CustomSrv_Request_type_support_data_t;

static _CustomSrv_Request_type_support_data_t _CustomSrv_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _CustomSrv_Request_message_typesupport_map = {
  2,
  "custom_interface",
  &_CustomSrv_Request_message_typesupport_ids.typesupport_identifier[0],
  &_CustomSrv_Request_message_typesupport_symbol_names.symbol_name[0],
  &_CustomSrv_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t CustomSrv_Request_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_CustomSrv_Request_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &custom_interface__srv__CustomSrv_Request__get_type_hash,
  &custom_interface__srv__CustomSrv_Request__get_type_description,
  &custom_interface__srv__CustomSrv_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace custom_interface

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, custom_interface, srv, CustomSrv_Request)() {
  return &::custom_interface::srv::rosidl_typesupport_c::CustomSrv_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "custom_interface/srv/detail/custom_srv__struct.h"
// already included above
// #include "custom_interface/srv/detail/custom_srv__type_support.h"
// already included above
// #include "custom_interface/srv/detail/custom_srv__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace custom_interface
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _CustomSrv_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _CustomSrv_Response_type_support_ids_t;

static const _CustomSrv_Response_type_support_ids_t _CustomSrv_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _CustomSrv_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _CustomSrv_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _CustomSrv_Response_type_support_symbol_names_t _CustomSrv_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, custom_interface, srv, CustomSrv_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_interface, srv, CustomSrv_Response)),
  }
};

typedef struct _CustomSrv_Response_type_support_data_t
{
  void * data[2];
} _CustomSrv_Response_type_support_data_t;

static _CustomSrv_Response_type_support_data_t _CustomSrv_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _CustomSrv_Response_message_typesupport_map = {
  2,
  "custom_interface",
  &_CustomSrv_Response_message_typesupport_ids.typesupport_identifier[0],
  &_CustomSrv_Response_message_typesupport_symbol_names.symbol_name[0],
  &_CustomSrv_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t CustomSrv_Response_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_CustomSrv_Response_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &custom_interface__srv__CustomSrv_Response__get_type_hash,
  &custom_interface__srv__CustomSrv_Response__get_type_description,
  &custom_interface__srv__CustomSrv_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace custom_interface

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, custom_interface, srv, CustomSrv_Response)() {
  return &::custom_interface::srv::rosidl_typesupport_c::CustomSrv_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "custom_interface/srv/detail/custom_srv__struct.h"
// already included above
// #include "custom_interface/srv/detail/custom_srv__type_support.h"
// already included above
// #include "custom_interface/srv/detail/custom_srv__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace custom_interface
{

namespace srv
{

namespace rosidl_typesupport_c
{

typedef struct _CustomSrv_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _CustomSrv_Event_type_support_ids_t;

static const _CustomSrv_Event_type_support_ids_t _CustomSrv_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _CustomSrv_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _CustomSrv_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _CustomSrv_Event_type_support_symbol_names_t _CustomSrv_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, custom_interface, srv, CustomSrv_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_interface, srv, CustomSrv_Event)),
  }
};

typedef struct _CustomSrv_Event_type_support_data_t
{
  void * data[2];
} _CustomSrv_Event_type_support_data_t;

static _CustomSrv_Event_type_support_data_t _CustomSrv_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _CustomSrv_Event_message_typesupport_map = {
  2,
  "custom_interface",
  &_CustomSrv_Event_message_typesupport_ids.typesupport_identifier[0],
  &_CustomSrv_Event_message_typesupport_symbol_names.symbol_name[0],
  &_CustomSrv_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t CustomSrv_Event_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_CustomSrv_Event_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &custom_interface__srv__CustomSrv_Event__get_type_hash,
  &custom_interface__srv__CustomSrv_Event__get_type_description,
  &custom_interface__srv__CustomSrv_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace custom_interface

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, custom_interface, srv, CustomSrv_Event)() {
  return &::custom_interface::srv::rosidl_typesupport_c::CustomSrv_Event_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "custom_interface/srv/detail/custom_srv__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/service_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
#include "service_msgs/msg/service_event_info.h"
#include "builtin_interfaces/msg/time.h"

namespace custom_interface
{

namespace srv
{

namespace rosidl_typesupport_c
{
typedef struct _CustomSrv_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _CustomSrv_type_support_ids_t;

static const _CustomSrv_type_support_ids_t _CustomSrv_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _CustomSrv_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _CustomSrv_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _CustomSrv_type_support_symbol_names_t _CustomSrv_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, custom_interface, srv, CustomSrv)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, custom_interface, srv, CustomSrv)),
  }
};

typedef struct _CustomSrv_type_support_data_t
{
  void * data[2];
} _CustomSrv_type_support_data_t;

static _CustomSrv_type_support_data_t _CustomSrv_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _CustomSrv_service_typesupport_map = {
  2,
  "custom_interface",
  &_CustomSrv_service_typesupport_ids.typesupport_identifier[0],
  &_CustomSrv_service_typesupport_symbol_names.symbol_name[0],
  &_CustomSrv_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t CustomSrv_service_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_CustomSrv_service_typesupport_map),
  rosidl_typesupport_c__get_service_typesupport_handle_function,
  &CustomSrv_Request_message_type_support_handle,
  &CustomSrv_Response_message_type_support_handle,
  &CustomSrv_Event_message_type_support_handle,
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_CREATE_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    custom_interface,
    srv,
    CustomSrv
  ),
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_DESTROY_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    custom_interface,
    srv,
    CustomSrv
  ),
  &custom_interface__srv__CustomSrv__get_type_hash,
  &custom_interface__srv__CustomSrv__get_type_description,
  &custom_interface__srv__CustomSrv__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace srv

}  // namespace custom_interface

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_c, custom_interface, srv, CustomSrv)() {
  return &::custom_interface::srv::rosidl_typesupport_c::CustomSrv_service_type_support_handle;
}

#ifdef __cplusplus
}
#endif
