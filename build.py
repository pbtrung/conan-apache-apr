from conan.packager import ConanMultiPackager

if __name__ == "__main__":
	mingw_configurations = [("5.4", "x86_64", "seh", "posix"),
	                        ("5.4", "x86_64", "sjlj", "posix"),
	                        ("5.4", "x86", "seh", "posix"),
	                        ("5.4", "x86", "sjlj", "posix")]
	builder = ConanMultiPackager(mingw_configurations=mingw_configurations)
    builder.add_common_builds(shared_option_name="apache-apr:shared", pure_c=True)
    builder.run()