cmake_minimum_required(VERSION 3.13)
project(libgatemate)

if (POLICY CMP0167)
  # The existence check above avoids breaking the build on older cmake versions
  cmake_policy(SET CMP0167 NEW)
endif()

option(BUILD_SHARED "Build shared GateMate library" OFF)
option(STATIC_BUILD "Create static build of GateMate tools" ON)

set(PROGRAM_PREFIX "" CACHE STRING "Name prefix for executables")

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
if (MSVC)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -bigobj -EHsc")
else()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -pedantic -Wextra -O3")
endif()
set(CMAKE_DEFIN)
set(link_param "")
if (STATIC_BUILD)
    set(Boost_USE_STATIC_LIBS ON)
    if(MSVC)
        add_definitions(-DBOOST_PYTHON_STATIC_LIB)
        set(CMAKE_CXX_FLAGS_RELEASE "/MT")
        set(CMAKE_CXX_FLAGS_DEBUG "/MTd")
    elseif (NOT APPLE)
        set(link_param "-static")
    endif()
else()
    if(MSVC)
        set(CMAKE_WINDOWS_EXPORT_ALL_SYMBOLS ON)
    endif()
endif()

find_package(Boost REQUIRED COMPONENTS program_options)

find_package(Git)

include_directories(include/ ${Boost_INCLUDE_DIRS})

aux_source_directory(include/ INCLUDE_FILES)
aux_source_directory(src/ SOURCE_FILES)

if (BUILD_SHARED)
    add_library(gatemate SHARED ${INCLUDE_FILES} ${SOURCE_FILES})
else()
    add_library(gatemate STATIC ${INCLUDE_FILES} ${SOURCE_FILES})
endif()

target_link_libraries(gatemate LINK_PUBLIC ${Boost_LIBRARIES} ${CMAKE_THREAD_LIBS_INIT})

include(GNUInstallDirs)
file(RELATIVE_PATH GATEMATE_RPATH_LIBDIR /${CMAKE_INSTALL_BINDIR} /${CMAKE_INSTALL_LIBDIR})
file(RELATIVE_PATH GATEMATE_RPATH_DATADIR /${CMAKE_INSTALL_BINDIR} /${CMAKE_INSTALL_DATADIR})

function(setup_rpath name)
    if(APPLE)
        set_target_properties(${name} PROPERTIES
                              BUILD_WITH_INSTALL_RPATH ON
                              INSTALL_RPATH "@loader_path/${GATEMATE_RPATH_LIBDIR}/${PROGRAM_PREFIX}gatemate"
                              INSTALL_NAME_DIR "@rpath")
    elseif(UNIX)
        set_target_properties(${name} PROPERTIES
                              BUILD_WITH_INSTALL_RPATH ON
                              INSTALL_RPATH "\$ORIGIN/${GATEMATE_RPATH_LIBDIR}/${PROGRAM_PREFIX}gatemate")
    endif()
endfunction()


# Avoid perturbing build if git version hasn't changed
file(MAKE_DIRECTORY "${CMAKE_BINARY_DIR}/generated")
set(LAST_GIT_VERSION "")
if (NOT DEFINED CURRENT_GIT_VERSION)
    execute_process(COMMAND git describe --tags OUTPUT_VARIABLE CURRENT_GIT_VERSION WORKING_DIRECTORY ${CMAKE_SOURCE_DIR})
endif()
string(STRIP "${CURRENT_GIT_VERSION}" CURRENT_GIT_VERSION)
if (EXISTS "${CMAKE_BINARY_DIR}/generated/last_git_version")
    file(READ "${CMAKE_BINARY_DIR}/generated/last_git_version" LAST_GIT_VERSION)
endif()
if (NOT ("${LAST_GIT_VERSION}" STREQUAL "${CURRENT_GIT_VERSION}") OR NOT GIT_EXECUTABLE)
    configure_file(
      ${CMAKE_SOURCE_DIR}/tools/version.cpp.in
      ${CMAKE_BINARY_DIR}/generated/version.cpp
    )
endif()
file(WRITE "${CMAKE_BINARY_DIR}/generated/last_git_version" CURRENT_GIT_VERSION)

add_executable(${PROGRAM_PREFIX}gmunpack ${INCLUDE_FILES} tools/gmunpack.cpp "${CMAKE_BINARY_DIR}/generated/version.cpp")
target_include_directories(${PROGRAM_PREFIX}gmunpack PRIVATE tools)
target_compile_definitions(${PROGRAM_PREFIX}gmunpack PRIVATE GATEMATE_RPATH_DATADIR="${GATEMATE_RPATH_DATADIR}" GATEMATE_PREFIX="${CMAKE_INSTALL_PREFIX}" GATEMATE_PROGRAM_PREFIX="${PROGRAM_PREFIX}")
target_link_libraries(${PROGRAM_PREFIX}gmunpack gatemate ${Boost_LIBRARIES} ${CMAKE_DL_LIBS} ${link_param})
setup_rpath(${PROGRAM_PREFIX}gmunpack)

add_executable(${PROGRAM_PREFIX}gmpack ${INCLUDE_FILES} tools/gmpack.cpp "${CMAKE_BINARY_DIR}/generated/version.cpp")
target_include_directories(${PROGRAM_PREFIX}gmpack PRIVATE tools)
target_compile_definitions(${PROGRAM_PREFIX}gmpack PRIVATE GATEMATE_RPATH_DATADIR="${GATEMATE_RPATH_DATADIR}" GATEMATE_PREFIX="${CMAKE_INSTALL_PREFIX}" GATEMATE_PROGRAM_PREFIX="${PROGRAM_PREFIX}")
target_link_libraries(${PROGRAM_PREFIX}gmpack gatemate ${Boost_LIBRARIES} ${CMAKE_DL_LIBS} ${link_param})
setup_rpath(${PROGRAM_PREFIX}gmpack)

if (WASI)
    foreach (tool gmunpack gmpack)
        # set(CMAKE_EXECUTABLE_SUFFIX) breaks CMake tests for some reason
        set_property(TARGET ${PROGRAM_PREFIX}${tool} PROPERTY SUFFIX ".wasm")
    endforeach()
endif()

if (BUILD_SHARED)
    install(TARGETS gatemate ${PROGRAM_PREFIX}gmunpack ${PROGRAM_PREFIX}gmpack
            LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}/${PROGRAM_PREFIX}gatemate
            RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
else()
    install(TARGETS ${PROGRAM_PREFIX}gmunpack ${PROGRAM_PREFIX}gmpack
            RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
endif()

file(GLOB_RECURSE CLANGFORMAT_FILES *.cpp *.hpp)

add_custom_target(
    clangformat
    COMMAND clang-format
    -style=file
    -i
    ${CLANGFORMAT_FILES}
)
