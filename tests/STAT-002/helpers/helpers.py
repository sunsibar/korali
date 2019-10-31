import numpy as np

def compareMean(k):
    samples = k["Solver"]["Internal"]["Sample Database"]
    
    mean      = np.mean(samples)
    chainmean = k["Solver"]["Internal"]["Chain Mean"]
    
    assert np.isclose(mean, chainmean), "Chain Mean deviates from Mean of "\
            "Samples ({0} vs {1})".format(mean, chainmean)

def compareStd(k):
    samples = k["Solver"]["Internal"]["Sample Database"]

    mean     = np.mean(samples)
    std      = np.sqrt(sum((samples - mean)**2)/(len(samples)-1))
    chainstd = k["Solver"]["Internal"]["Cholesky Decomposition Chain Covariance"]
    
    assert np.isclose(std, chainstd), "Cholesky Decomposition of Chain" \
            "Covariance deviates from Standard Deviation of Samples ({0} vs {1})".format(std, chainstd)


