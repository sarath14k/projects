cmake_minimum_required(VERSION 3.16)

# Set project details
project(Notepad VERSION 0.1 LANGUAGES CXX)

# Enable automatic handling of UIC, MOC, and RCC files
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)

# Set the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find the necessary Qt components (Qt5 or Qt6)
find_package(QT NAMES Qt6 Qt5 COMPONENTS Core Widgets PrintSupport REQUIRED)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Core Widgets PrintSupport)

# Get all .cpp files in the src folder
file(GLOB_RECURSE SOURCES "src/*.cpp")

# Get all .h files in the include folder
file(GLOB_RECURSE HEADERS "include/*.h")

# Get all .ui files in the ui folder
file(GLOB_RECURSE UIS "ui/*.ui")

# Include the headers directory
include_directories(include)

# Specify where to find .ui files
set(CMAKE_AUTOUIC_SEARCH_PATHS "${CMAKE_SOURCE_DIR}/ui")

# Add executable based on Qt version
if(${QT_VERSION_MAJOR} GREATER_EQUAL 6)
    qt_add_executable(Notepad
        MANUAL_FINALIZATION
        ${SOURCES}
        ${HEADERS}
        ${UIS}  # Ensure UI files are included
        Resource.qrc  # Include the resource file
    )
else()
    add_executable(Notepad
        ${SOURCES}
        ${HEADERS}
        ${UIS}  # Ensure UI files are included
        Resource.qrc  # Include the resource file
    )
endif()

# Link the appropriate Qt libraries
target_link_libraries(Notepad PRIVATE Qt${QT_VERSION_MAJOR}::Core Qt${QT_VERSION_MAJOR}::Widgets Qt${QT_VERSION_MAJOR}::PrintSupport)

# Set bundle properties for macOS/iOS
set_target_properties(Notepad PROPERTIES
    MACOSX_BUNDLE TRUE
    WIN32_EXECUTABLE TRUE
    MACOSX_BUNDLE_BUNDLE_VERSION ${PROJECT_VERSION}
    MACOSX_BUNDLE_SHORT_VERSION_STRING ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}
)

# Installation instructions
install(TARGETS Notepad
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)

# Finalize executable for Qt6
if(QT_VERSION_MAJOR EQUAL 6)
    qt_finalize_executable(Notepad)
endif()

# Add runnable rule
add_custom_target(run
    COMMAND $<TARGET_FILE:Notepad>
    DEPENDS Notepad
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    COMMENT "Running the Notepad application"
)


