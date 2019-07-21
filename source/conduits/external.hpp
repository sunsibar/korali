#ifndef _KORALI_CONDUIT_EXTERNAL_HPP_
#define _KORALI_CONDUIT_EXTERNAL_HPP_

#include "conduits/base.hpp"
#include <sys/types.h>
#include <unistd.h>
#include <queue>
#include <vector>
#include <map>

namespace Korali { namespace Conduit {

class External : public Base {
 public:

 int _concurrentJobs;
 std::vector<std::vector<int>> _pipeDescriptors;
 std::queue<int> _launcherQueue;

 std::map<int, size_t> _launcherIdToSamplerIdMap;
 std::map<int, pid_t> _launcherIdToProcessIdMap;
 std::map<pid_t, int> _processIdMapToLauncherIdMap;

 void initialize() override;
 void finalize() override;

 void evaluateSample(double* sampleArray, size_t sampleId) override;
 void checkProgress() override;
 bool isRoot() override;

 // Serialization Methods
 void getConfiguration() override;
 void setConfiguration() override;
};
} } // namespace Korali::Conduit

#endif // _KORALI_CONDUIT_EXTERNAL_HPP_