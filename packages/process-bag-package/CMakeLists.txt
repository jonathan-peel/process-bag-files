cmake_minimum_required(VERSION 2.8.3)
project(process-bag-package)

find_package(catkin REQUIRED COMPONENTS
  rospy
)

catkin_package()