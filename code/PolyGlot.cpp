#ifndef dPolyGlot_Cpp
#define dPolyGlot_Cpp
//headers
#include "PolyGlot.hpp"
//content
namespace nPolyGlot
{
//testing
#if defined(dPolyGlot_MakeTest)
//-//typedef
using tTestKey = std::string_view;
using tTestOut = int;
using tTestFun = std::function<tTestOut(void)>;
using tTestTab = std::unordered_map<tTestKey, tTestFun>;
using tTestRef = tTestTab::iterator;
//-//consdef
static const tTestTab vTestTab = {
	{"Hello",
	 []()
	 {
		 fmt::println(stdout, "HelloWorld");
		 return EXIT_SUCCESS;
	 }},
	{"FileSystem",
	 []()
	 {
		 auto vAbsolutePath = nFileSystem::current_path();
		 auto vRelativePath = nFileSystem::relative(vAbsolutePath);
		 fmt::println(stdout, "RelativePath={:s}", vRelativePath.c_str());
		 fmt::println(
			 stdout, "ProjPathFound={:d}", std::filesystem::exists(dPolyGlot_ProjPath)
		 );
		 fmt::println(
			 stdout, "DataPathFound={:d}", std::filesystem::exists(dPolyGlot_ProjPath)
		 );
		 return EXIT_SUCCESS;
	 }},
};
#endif//ifd(dPolyGlot_MakeTest)
}//namespace nPolyGlot
//actions
int main(int vArgC, char **vArgV, char **vEnvi)
{
	nPolyGlot::nFileSystem::current_path(dPolyGlot_ProjPath);
#if defined(dPolyGlot_MakeTest)
	if(vArgC == 3 && std::string_view(vArgV[1]) == "test")
	{
		auto vTestKey = std::string_view(vArgV[2]);
		auto vTestRef = nPolyGlot::vTestTab.find(vTestKey);
		if(vTestRef == nPolyGlot::vTestTab.end())
		{
			fmt::println(stderr, "invalid test key: {}", vTestKey);
			return EXIT_FAILURE;
		}
		else
		{
			fmt::println(stdout, "{}?", vTestKey);
			auto vTestOut = vTestRef->second();
			fmt::println(stdout, "{}!", vTestKey);
			return vTestOut;
		}
	}
	else
#endif//ifd(dPolyGlot_MakeTest)
	{
		auto vIter = std::ostream_iterator<char *>(std::cout, "\n");
		std::copy(vArgV, vArgV + vArgC, vIter);
	}
	return EXIT_SUCCESS;
}
#endif//dPolyGlot_Cpp
