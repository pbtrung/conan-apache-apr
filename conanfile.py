from conans import ConanFile, AutoToolsBuildEnvironment, tools
from conans.util import files
import os

class ApacheaprConan(ConanFile):
    description = "Apache Portable Runtime"
    name = "apache-apr"
    version = "1.6.0"
    license = "Apache-2.0"
    url = "https://github.com/pbtrung/conan-apache-apr"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    install_dir = "install"

    def source(self):
        zip_name = "apr-%s.tar.gz" % self.version
        tools.download("https://codeload.github.com/apache/apr/tar.gz/%s" % self.version, zip_name, verify=False)
        tools.unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        env_build = AutoToolsBuildEnvironment(self)
        with tools.environment_append(env_build.vars):
            buildconf_command = "./buildconf"
            configure_command = "./configure"
            configure_command += " --prefix=%s%s%s" % (os.getcwd(), os.sep, self.install_dir)
            with tools.chdir("apr-" + self.version):
                files.mkdir(self.install_dir)
                self.run(buildconf_command)
                self.run(configure_command)
                self.run("make -j " + str(max(tools.cpu_count() - 1, 1)))
                self.run("make install")

    def package(self):
        install_path = self.install_dir + os.sep
        self.copy("*.h", dst="include/apr-1", src=install_path + "include/apr-1", keep_path=False)
        if self.settings.os != "Windows":
            self.copy("*.pc", dst="lib/pkgconfig", src=install_path + "lib", keep_path=False)
            if self.options.shared:
                self.copy("*.so*", dst="lib", src=install_path + "lib", keep_path=False)
                self.copy("*.dylib", dst="lib", src=install_path + "lib", keep_path=False)
            else:
                self.copy("*.a", dst="lib", src=install_path + "lib", keep_path=False)
        else:
            if self.options.shared:
                self.copy("*.dll", dst="bin", src=install_path + "bin", keep_path=False)
            else:
                self.copy("*.lib", dst="lib", src=install_path + "lib", keep_path=False)

        self.copy("apr-1-config", dst="bin", src=install_path + "bin", keep_path=False)
        self.copy("*.exp", dst="lib", src=install_path + "lib", keep_path=False)
        self.copy("*", dst="build-1", src=install_path + "build-1", keep_path=False)

    def package_info(self):
        self.cpp_info.includedirs = ["include", "include/apr-1"]
        self.cpp_info.bindirs = ["bin"]
        self.cpp_info.libs = ["apr-1"]