### Notes

A collection of all the notes taken during the development of the project.

- GCC, Clang, and MSVC are the three main compilers for C++.
- Compilers implement the C++ standard.
- Code is passed to the compiler to generate machine code.
- There may be compiler-specific primitives in the implementation of the standard.
- Clang is the frontend of the LLVM compiler.
- LLVM represents a more modern and flexible paradigm in compiler design.
- The frontend of a compiler is responsible for parsing the code and generating an intermediate representation (IR).
- GCC and MSVC contain both frontend and backend components.
- The full C++ modules feature is only supported by MSVC at the moment.

- Use `.vscode/c_cpp_properties.json` to configure IntelliSense.

- A Makefile is like a script that runs the compiler's build commands and other related tasks.
- CMake is like a meta-build system that generates Makefiles.
- Automake is similar to CMake but is more complex and specific to GNU build systems.

- Use `2>&1` to redirect error output to standard output.
- `#include` is essentially an instruction for copying and pasting code from header files.

- **libvpx** is the library for the VP8 and VP9 video codecs.
- **FFmpeg** uses libvpx under the hood for VP8 and VP9 encoding.
- **AV1** is the successor to VP9.
- **WebM** and **MP4** are two widely-used video container formats.


- reentrant(re-entrant) means the code can be interrupted and re-entered.
- The compiler flag -D_REENTRANT is used to enable reentrant version of implementations.