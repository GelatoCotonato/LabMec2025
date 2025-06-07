// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from custom_interface:msg/CustomMsg.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "custom_interface/msg/custom_msg.hpp"


#ifndef CUSTOM_INTERFACE__MSG__DETAIL__CUSTOM_MSG__TRAITS_HPP_
#define CUSTOM_INTERFACE__MSG__DETAIL__CUSTOM_MSG__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "custom_interface/msg/detail/custom_msg__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace custom_interface
{

namespace msg
{

inline void to_flow_style_yaml(
  const CustomMsg & msg,
  std::ostream & out)
{
  out << "{";
  // member: index
  {
    out << "index: ";
    rosidl_generator_traits::value_to_yaml(msg.index, out);
    out << ", ";
  }

  // member: name
  {
    out << "name: ";
    rosidl_generator_traits::value_to_yaml(msg.name, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const CustomMsg & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: index
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "index: ";
    rosidl_generator_traits::value_to_yaml(msg.index, out);
    out << "\n";
  }

  // member: name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "name: ";
    rosidl_generator_traits::value_to_yaml(msg.name, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const CustomMsg & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace custom_interface

namespace rosidl_generator_traits
{

[[deprecated("use custom_interface::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const custom_interface::msg::CustomMsg & msg,
  std::ostream & out, size_t indentation = 0)
{
  custom_interface::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use custom_interface::msg::to_yaml() instead")]]
inline std::string to_yaml(const custom_interface::msg::CustomMsg & msg)
{
  return custom_interface::msg::to_yaml(msg);
}

template<>
inline const char * data_type<custom_interface::msg::CustomMsg>()
{
  return "custom_interface::msg::CustomMsg";
}

template<>
inline const char * name<custom_interface::msg::CustomMsg>()
{
  return "custom_interface/msg/CustomMsg";
}

template<>
struct has_fixed_size<custom_interface::msg::CustomMsg>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<custom_interface::msg::CustomMsg>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<custom_interface::msg::CustomMsg>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // CUSTOM_INTERFACE__MSG__DETAIL__CUSTOM_MSG__TRAITS_HPP_
