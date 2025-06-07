// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_interface:msg/CustomMsg.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "custom_interface/msg/custom_msg.hpp"


#ifndef CUSTOM_INTERFACE__MSG__DETAIL__CUSTOM_MSG__BUILDER_HPP_
#define CUSTOM_INTERFACE__MSG__DETAIL__CUSTOM_MSG__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_interface/msg/detail/custom_msg__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_interface
{

namespace msg
{

namespace builder
{

class Init_CustomMsg_name
{
public:
  explicit Init_CustomMsg_name(::custom_interface::msg::CustomMsg & msg)
  : msg_(msg)
  {}
  ::custom_interface::msg::CustomMsg name(::custom_interface::msg::CustomMsg::_name_type arg)
  {
    msg_.name = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_interface::msg::CustomMsg msg_;
};

class Init_CustomMsg_index
{
public:
  Init_CustomMsg_index()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_CustomMsg_name index(::custom_interface::msg::CustomMsg::_index_type arg)
  {
    msg_.index = std::move(arg);
    return Init_CustomMsg_name(msg_);
  }

private:
  ::custom_interface::msg::CustomMsg msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_interface::msg::CustomMsg>()
{
  return custom_interface::msg::builder::Init_CustomMsg_index();
}

}  // namespace custom_interface

#endif  // CUSTOM_INTERFACE__MSG__DETAIL__CUSTOM_MSG__BUILDER_HPP_
