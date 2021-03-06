import conans
import os
import os.path
import pathlib
import shutil


GEN_SRC = pathlib.Path('gen_src')


class LuaConan(conans.ConanFile):
    name = "Lua"
    version = "5.2.3"

    # Where the extract file contents end up.
    lua_dir = pathlib.Path(f'lua-{version}')

    exports_sources = ("CMakeLists.txt", "Config.cmake.in")

    def source(self):
        # Download the official Lua sources
        conans.tools.get(**self.conan_data["sources"][self.version])
        shutil.copy(pathlib.Path(self.source_folder) / "CMakeLists.txt",
                    self.lua_dir / "CMakeLists.txt")
        shutil.copy(pathlib.Path(self.source_folder) / "Config.cmake.in",
                    self.lua_dir / "Config.cmake.in")

    def _configed_cmake(self):
        cmake = conans.CMake(self)
        lua_dir = pathlib.Path(self.source_folder) / self.lua_dir
        cmake.configure(source_folder=str(lua_dir))
        return cmake

    def build(self):
        cmake = self._configed_cmake()
        cmake.build()

    def package(self):
        cmake = self._configed_cmake()
        cmake.install()

        # self.copy(pattern="*.h", dst="include", src=os.path.join(self.lua_dir, "src"))
        # self.copy(pattern="*.lib", dst="lib", src="lib")
        # self.copy(pattern="*.a", dst="lib", src="lib")

    def package_info(self):
        self.cpp_info.libs = ["lua_lib"]
        self.cpp_info.includedirs = [f"include/lua{self.version}"]
