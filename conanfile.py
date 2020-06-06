from conans import ConanFile, tools, AutoToolsBuildEnvironment
import os

class GsaslConan(ConanFile):
    name = "gsasl"
    version = "1.8.1"
    license = "<Put the package license here>"
    author = "<Put your name here> <And your email here>"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "<Description of Gsasl here>"
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "cmake"
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
        atargs = ["--disable-obsolete"]
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
        pass

