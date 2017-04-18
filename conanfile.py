from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os

class ApacheaprConan(ConanFile):
    description = "Apache Portable Runtime"
    name = "apache-apr"
    version = "1.5.2"
    license = "Apache-2.0"
    url = "https://github.com/pbtrung/conan-apache-apr"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    lib_name = name + "-" + version

    def source(self):
        file_ext = ".tar.gz" if not self.settings.os == "Windows" else "-win32-src.zip"
        tools.download("https://www.apache.org/dyn/mirrors/mirrors.cgi?action=download&filename=apr/apr-" + self.version + file_ext, self.lib_name + file_ext)
        tools.unzip(self.lib_name + file_ext)

    def build(self):
        env_build = AutoToolsBuildEnvironment(self)
        with tools.environment_append(env_build.vars):
            configure_command = "./configure"
            configure_command += " --prefix=" + os.getcwd()
            if self.settings.os == "Windows":
                configure_command = "nmake -f ./Makefile.win"

            install_command = "nmake -f ./Makefile.win PREFIX=" + os.getcwd() + " install"

            with tools.chdir("apr-" + self.version):
                self.run(configure_command)
                if self.settings.os != "Windows":
                    self.run("make -j " + str(max(tools.cpu_count() - 1, 1)))
                    self.run("make install")
                else:
                    self.run(install_command)

    def package(self):
        self.copy("*.h", dst="include/apr-1", src="include/apr-1", keep_path=False)
        if self.settings.os != "Windows":
            self.copy("*.pc", dst="lib/pkgconfig", src="lib", keep_path=False)
            if self.options.shared:
                self.copy("*.so*", dst="lib", src="lib", keep_path=False)
                self.copy("*.dylib", dst="lib", src="lib", keep_path=False)
            else:
                self.copy("*.a", dst="lib", src="lib", keep_path=False)
        else:
            if self.options.shared:
                self.copy("*.dll", dst="bin", src="bin", keep_path=False)
            else:
                self.copy("*.lib", dst="lib", src="lib", keep_path=False)

        self.copy("apr-1-config", dst="bin", src="bin", keep_path=False)
        self.copy("*.exp", dst="lib", src="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["apr-1"]