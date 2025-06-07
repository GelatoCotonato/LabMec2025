// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_interface:srv/CustomSrv.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "custom_interface/srv/custom_srv.hpp"


#ifndef CUSTOM_INTERFACE__SRV__DETAIL__CUSTOM_SRV__BUILDER_HPP_
#define CUSTOM_INTERFACE__SRV__DETAIL__CUSTOM_SRV__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_interface/srv/detail/custom_srv__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_interface
{

namespace srv
{

namespace builder
{

class Init_CustomSrv_Request_start
{
public:
  Init_CustomSrv_Request_start()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::custom_interface::srv::CustomSrv_Request start(::custom_interface::srv::CustomSrv_Request::_start_type arg)
  {
    msg_.start = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interface::srv::CustomSrv_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interface::srv::CustomSrv_Request>()
{
  return custom_interface::srv::builder::Init_CustomSrv_Request_start();
}

}  // namespace custom_interface


namespace custom_interface
{

namespace srv
{

namespace builder
{

class Init_CustomSrv_Response_message
{
public:
  explicit Init_CustomSrv_Response_message(::custom_interface::srv::CustomSrv_Response & msg)
  : msg_(msg)
  {}
  ::custom_interface::srv::CustomSrv_Response message(::custom_interface::srv::CustomSrv_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interface::srv::CustomSrv_Response msg_;
};

class Init_CustomSrv_Response_success
{
public:
  Init_CustomSrv_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_CustomSrv_Response_message success(::custom_interface::srv::CustomSrv_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_CustomSrv_Response_message(msg_);
  }

private:
  ::custom_interface::srv::CustomSrv_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interface::srv::CustomSrv_Response>()
{
  return custom_interface::srv::builder::Init_CustomSrv_Response_success();
}

}  // namespace custom_interface


namespace custom_interface
{

namespace srv
{

namespace builder
{

class Init_CustomSrv_Event_response
{
public:
  explicit Init_CustomSrv_Event_response(::custom_interface::srv::CustomSrv_Event & msg)
  : msg_(msg)
  {}
  ::custom_interface::srv::CustomSrv_Event response(::custom_interface::srv::CustomSrv_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interface::srv::CustomSrv_Event msg_;
};

class Init_CustomSrv_Event_request
{
public:
  explicit Init_CustomSrv_Event_request(::custom_interface::srv::CustomSrv_Event & msg)
  : msg_(msg)
  {}
  Init_CustomSrv_Event_response request(::custom_interface::srv::CustomSrv_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_CustomSrv_Event_response(msg_);
  }

private:
  ::custom_interface::srv::CustomSrv_Event msg_;
};

class Init_CustomSrv_Event_info
{
public:
  Init_CustomSrv_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_CustomSrv_Event_request info(::custom_interface::srv::CustomSrv_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_CustomSrv_Event_request(msg_);
  }

private:
  ::custom_interface::srv::CustomSrv_Event msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interface::srv::CustomSrv_Event>()
{
  return custom_interface::srv::builder::Init_CustomSrv_Event_info();
}

}  // namespace custom_interface

#endif  // CUSTOM_INTERFACE__SRV__DETAIL__CUSTOM_SRV__BUILDER_HPP_
