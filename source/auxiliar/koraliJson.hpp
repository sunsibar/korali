#ifndef _KORALI_AUXILIARS_KORALIJSON_HPP_
#define _KORALI_AUXILIARS_KORALIJSON_HPP_

#include <string>
#include "external/json/json.hpp"
#include "pybind11/pybind11.h"
#include "pybind11/functional.h"
#include "pybind11/stl.h"

namespace korali
{

class Sample;

class KoraliJson {

 public:

 KoraliJson();

 // JSON-based configuration
 nlohmann::json  _js;

 // Python and Json Configuration Binding Methods
 nlohmann::json*  _opt;

 nlohmann::json& getJson();
 void setJson(nlohmann::json& js);

 pybind11::object getItem(pybind11::object key);
 void setItem(pybind11::object key, pybind11::object val);

 nlohmann::json& operator[](const std::string& key);
 nlohmann::json& operator[](const unsigned long int& key);

 bool contains(const std::string& key);
 void traverseKey(pybind11::object key);
};


/*********************************************************************
 * The following class was introduced for support to Korali:
 *********************************************************************/

class JsonInterface
{

public:

static bool isEmpty(nlohmann::json& js)
{
 bool empty = true;

 if (js.is_null()) return true;
 if (js.is_primitive()) return false;

 if (js.is_array())
 {
  for (size_t i = 0; i < js.size(); i++)
  {
   bool elEmpty = isEmpty(js[i]);
   if (elEmpty) js.erase(i--);
   empty = empty && elEmpty;
  }
 }

 if (js.is_object())
 {
  std::vector<std::string> erasedKeys;
  for (auto& el : js.items())
  {
   bool elEmpty = isEmpty(el.value());
   if (elEmpty == true) erasedKeys.push_back(el.key());
   empty = empty && elEmpty;
  }
  for (size_t i = 0; i < erasedKeys.size(); i++) js.erase(erasedKeys[i]);
 }

 return empty;
}

static bool isElemental(nlohmann::json& js)
{
 if (js.is_number()) return true;
 if (js.is_string()) return true;

 bool isArray = true;

 if (js.is_array())
 {
  for (size_t i = 0; i < js.size(); i++)
  {
   bool isElementArray = false;
   if (js[i].is_array()) isElementArray = isElemental(js[i]);
   if (js[i].is_number()) isElementArray = true;
   if (js[i].is_string()) isElementArray = true;
   isArray = isArray && isElementArray;
  }
 }
 else isArray = false;

 return isArray;
}

static std::vector<std::string> getJsonPath(std::string path)
{
 std::vector<size_t> positions;

 size_t curpos = 0;
 while (curpos != std::string::npos)
 {
  if (curpos > 0) positions.push_back(curpos);
  curpos = path.find("'", curpos + 1);
 }

 if (positions.size() % 2 != 0) korali::logError("Incorrect path description: %s\n", path.c_str());

 std::vector<std::string> settings;

 for (size_t i = 0; i < positions.size(); i += 2)
 {
  size_t start = positions[i] + 1;
  size_t length = positions[i+1] - start;
  settings.push_back(path.substr(start, length));
 }

 return settings;
}

static void eraseValue(nlohmann::json& js, std::string path)
{
 std::vector<std::string> settings = getJsonPath(path);

 nlohmann::json* aux = &js;
 size_t i = 0;
 for (; i < settings.size()-1; i++)
  aux = &aux->at(settings[i]);
 aux->erase(settings[i]);
}

static bool isDefined(nlohmann::json& js, std::vector<std::string> settings)
{
 auto tmp = js;

 for (size_t i = 0; i < settings.size(); i++)
 {
  if (tmp.find(settings[i]) == tmp.end()) return false;
  tmp = tmp[settings[i]];
 }
 return true;
}

static bool isDefined(nlohmann::json& js, std::string path)
{
 return isDefined(js, getJsonPath(path));
}

static bool loadJsonFromFile(nlohmann::json& dst, const char* fileName)
{
 FILE *fid = fopen(fileName, "r");
 if (fid != nullptr)
 {
   fseek(fid, 0, SEEK_END);
   long fsize = ftell(fid);
   fseek(fid, 0, SEEK_SET);  /* same as rewind(f); */

   char *string = (char*) malloc(fsize + 1);
   fread(string, 1, fsize, fid);
   fclose(fid);

   string[fsize] = '\0';

   dst = nlohmann::json::parse(string);

   free(string);

   return true;
 }

 return false;
}

static void saveJsonToFile(const char* fileName, nlohmann::json& js)
{
 FILE *fid = fopen(fileName, "w");
 if (fid != nullptr)
 {
   fprintf(fid, "%s", js.dump(1).c_str());
   fclose(fid);
 }
 else
  korali::logError("Could not write to file: %s.\n", fileName);
}


/********************************************************
 * End of additional class by the Korali team:
 *******************************************************/
};

}
#endif // _KORALI_AUXILIARS_KORALIJSON_HPP_
