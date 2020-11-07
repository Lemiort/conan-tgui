from conans import ConanFile
import os, shutil
from conans.tools import download, unzip, check_sha256
from conans import CMake

class PackagerTGUI(ConanFile):
    name = 'tgui'
    version = '0.8.8'
    branch = 'stable'
    settings = 'os', 'compiler', 'arch', 'build_type'
    options = {'shared': [True, False]}
    default_options = 'shared=True'
    generators = 'cmake'
    license = 'zlib/png'
    url='https://github.com/texus/TGUI'
    exports = ['CMakeLists.txt']
    so_version = '0.8.0'
    ZIP_FOLDER_NAME = 'TGUI-0.8.8'

    def source(self):
        zip_name = '0.8.zip'
        download('https://github.com/texus/TGUI/archive/%s' % zip_name, zip_name)
        check_sha256(zip_name, 'BB9A796482D4DB78DDA244BCABBDAFFC9009EEF7F2C0F3FECEB9CC04DBE2DDC0')
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self.settings)
        self.run('mkdir _build')
        self.run('cd _build && cmake ../%s -DBUILD_SHARED_LIBS=%s -DCMAKE_INSTALL_PREFIX=../install %s' %
            (self.ZIP_FOLDER_NAME, 'ON' if self.options.shared else 'OFF', cmake.command_line)
        )
        if self.settings.os == 'Windows':
            self.run('cd _build && cmake --build . %s --target install --config %s' % (cmake.build_config, self.settings.build_type))
        else:
            self.run('cd _build && cmake --build . %s -- -j2 install' % cmake.build_config)

    def package(self):
        self.copy('*.*', 'include', 'install/include', keep_path=True)
        self.copy(pattern='*.a', dst='lib', src='install/lib', keep_path=False)
        self.copy(pattern='*.so.' + self.so_version, dst='lib', src='install/lib', keep_path=False)
        self.copy(pattern='*.lib', dst='lib', src='install/lib', keep_path=False)
        self.copy(pattern='*.dll', dst='bin', src='install/lib', keep_path=False)

    def package_info(self):
        if (not self.settings.os == 'Windows') and self.options.shared:
            self.cpp_info.libs = [':libtgui'
                                  + ('-d' if self.settings.build_type == 'Debug' else '')
                                  + '.so.'
                                  + self.so_version]
        else:
            self.cpp_info.libs = ['tgui'
                                  + ('' if self.options.shared else '-s')
                                  + ('-d' if self.settings.build_type == 'Debug' else '')]

