// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from custom_interface:msg/CustomMsg.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "custom_interface/msg/custom_msg.hpp"


#ifndef CUSTOM_INTERFACE__MSG__DETAIL__CUSTOM_MSG__STRUCT_HPP_
#define CUSTOM_INTERFACE__MSG__DETAIL__CUSTOM_MSG__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__custom_interface__msg__CustomMsg __attribute__((deprecated))
#else
# define DEPRECATED__custom_interface__msg__CustomMsg __declspec(deprecated)
#endif

namespace custom_interface
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct CustomMsg_
{
  using Type = CustomMsg_<ContainerAllocator>;

  explicit CustomMsg_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->index = 0ll;
      this->name = 0;
    }
  }

  explicit CustomMsg_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->index = 0ll;
      this->name = 0;
    }
  }

  // field types and members
  using _index_type =
    int64_t;
  _index_type index;
  using _name_type =
    uint8_t;
  _name_type name;

  // setters for named parameter idiom
  Type & set__index(
    const int64_t & _arg)
  {
    this->index = _arg;
    return *this;
  }
  Type & set__name(
    const uint8_t & _arg)
  {
    this->name = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    custom_interface::msg::CustomMsg_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_interface::msg::CustomMsg_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_interface::msg::CustomMsg_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_interface::msg::CustomMsg_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_interface::msg::CustomMsg_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_interface::msg::CustomMsg_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_interface::msg::CustomMsg_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_interface::msg::CustomMsg_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_interface::msg::CustomMsg_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_interface::msg::CustomMsg_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_interface__msg__CustomMsg
    std::shared_ptr<custom_interface::msg::CustomMsg_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_interface__msg__CustomMsg
    std::shared_ptr<custom_interface::msg::CustomMsg_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const CustomMsg_ & other) const
  {
    if (this->index != other.index) {
      return false;
    }
    if (this->name != other.name) {
      return false;
    }
    return true;
  }
  bool operator!=(const CustomMsg_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct CustomMsg_

// alias to use template instance with default allocator
using CustomMsg =
  custom_interface::msg::CustomMsg_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace custom_interface

#endif  // CUSTOM_INTERFACE__MSG__DETAIL__CUSTOM_MSG__STRUCT_HPP_
