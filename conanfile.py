from conans import ConanFile, CMake
from conans.tools import download, unzip, check_sha256
import os, shutil

class SDLConanFile(ConanFile):
    name = "sdl"
    version = "2.0.4"
    branch = "stable"
    settings = "os", "compiler", "arch", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"
    license = "zlib/png"
    url = "http://github.com/chaosteil/conan-sdl"
    exports = ["CMakeLists.txt"]
    so_version = "0.4.0"
    mercurial_archive = "330f500d5815"
    full_version = 'SDL2-2.0.4'

    def source(self):
        zip_name = "%s.zip" % self.full_version
        # download("https://www.libsdl.org/release/%s" % zip_name, zip_name)
        # We use this mercurial package because it fixes a critical build error
        # on the latest Arch linux. Remove once SDL 2.0.5 is released.
        download("https://hg.libsdl.org/SDL/archive/%s.zip" % self.mercurial_archive, zip_name)
        check_sha256(zip_name, 'dd2816bd7551ed206a8687dad224d3651522551dd3669a97ed820ba641f89a51')
        unzip(zip_name)
        os.unlink(zip_name)

        folder_name = 'SDL-%s' % (self.mercurial_archive)
        self.run("chmod +x ./%s/configure" % folder_name)

    def config(self):
        del self.settings.compiler.libcxx

    def build(self):
        folder_name = 'SDL-%s' % (self.mercurial_archive)
        cmake = CMake(self.settings)
        self.run("mkdir -p _build")
        cd_build = "cd _build"
        self.output.warn('%s && cmake ../%s %s' % (cd_build, folder_name, cmake.command_line))
        self.run('%s && cmake ../%s %s' % (cd_build, folder_name, cmake.command_line))
        self.output.warn("%s && cmake --build . %s" % (cd_build, cmake.build_config))
        self.run("%s && cmake --build . %s" % (cd_build, cmake.build_config))

    def package(self):
        folder_name = 'SDL-%s' % (self.mercurial_archive)
        self.copy("*.h", "include", "%s" % (folder_name), keep_path=False)
        self.copy("*.h", "include", "%s" % ("_build"), keep_path=False)

        # Copying static and dynamic libs
        if self.options.shared:
            if self.settings.os == "Macos":
                self.copy(pattern="*.dylib", dst="lib", keep_path=False)
            else:
                self.copy(pattern="*.so*", dst="lib", src="_build", keep_path=False)
        else:
            self.copy(pattern="*.a", dst="lib", src="_build", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['SDL2-2.0']
