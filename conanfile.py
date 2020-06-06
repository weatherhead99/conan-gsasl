from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os

class GsaslConan(ConanFile):
    name = "gsasl"
    version = "1.8.1"
    license = "GPL-3.0"
    author = "Dan Weatherill dan.weatherill@cantab.net"
    url = "https://github.com/weatherhead99/conan-gsasl"
    description = "GNU Simple Authentication and Security Layer"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    requires = ("libiconv/[>=1.15]@bincrafters/stable",
                "readline/[>=7.0]@bincrafters/stable")

    def source(self):
        git = tools.Git()
        tag_name = "gsasl-%s" % self.version.replace(".","-")
        git.clone("https://git.savannah.gnu.org/git/gsasl.git")
        git.checkout(tag_name)
        
    def build(self):
        #need to run the autoreconf etc
        self.output.info("running autoreconf...")
        os.chdir(self.source_folder)
        self.run("make bootstrap")
        autotools = AutoToolsBuildEnvironment(self)
        atargs = ["--disable-obsolete",
                  "--with-packager weatherhead99",
                  "--with-package-version 1.8.1-conan0"]
        if self.options.shared:
            atargs.extend(["--enable-static=no"])
        else:
            atargs.extend(["--enable-shared=no"])
        
        autotools.configure()
        #note, build breaks in parallel due to some strange error
        os.environ["CONAN_CPU_COUNT"] = "1"
        autotools.make()
        autotools.install()

    def package(self):
        #get rid of documentation directories
        tools.rmdir("share/info")
        tools.rmdir("share/man")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

