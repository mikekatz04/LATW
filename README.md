# LISA Analysis Tools Workshop (LATW)

This repo houses the tutorial codes for the LISA Analysis Tools Workshop. The tutorials are stored in the [tutorials](tutorials/) directory. The tutorials are numbered as follows:

0) Introductory tutorial for helpful Python concepts related to the successful usage of LISA Analysis Tools packages. This also gives the user a flavor of what the tutorials are like. 

1) Introduction to [LISA Analysis Tools](https://mikekatz04.github.io/LISAanalysistools) (`lisatools`). This includes setting up LISA sensitivity information, using data analysis classes, calculating inner products, SNRs, and Likelihoods. 

2) EMRIs and LISA Response: build EMRI waveforms wrapped in a time-domain LISA response function. This combines the use of [Fast EMRI Waveforms](https://bhptoolkit.org/FastEMRIWaveforms/html/index.html) (`few`) and [`fastlisaresponse`](https://mikekatz04.github.io/lisa-on-gpu).

3) MCMC with Eryn: use various **fixed-dimensional** MCMC techniques with the [Eryn](https://mikekatz04.github.io/Eryn) (`eryn`) sampler package.

4) MCMC and MBHBs: use lessons learned in Eryn to build up to a full MCMC with Massive Black Hole Binaries. [BBHx](https://mikekatz04.github.io/BBHx) (`bbhx`) is used to produce LISA TDI waveforms. We also use that package to perform the analysis with the "Heterodyning" technique. 

5) RJMCMC with Eryn: perform trans-dimensional or Reversible Jump MCMC with the [Eryn](https://mikekatz04.github.io/Eryn) (`eryn`) sampler package. 

6) Galactic Binaries: analyze Galactic binary waveforms and use them in MCMC and RJMCMC analyses. We will use [GBGPU](https://mikekatz04.github.io/GBGPU) to produce waveforms using the FastGB waveform construction method in the frequency domain. 


# Installation

LATW leverages conda environments to install and use necessary packages. If you do not have [Anaconda](https://www.anaconda.com/download) or [miniconda](https://docs.anaconda.com/free/miniconda/index.html) installed, you must do this first and load your `base` conda environment. 

First, clone the repo and `cd` to the `LATW` directory.:
```
git clone https://github.com/mikekatz04/LATW.git
cd LATW/
```

Install all packages necessary for the tutorials by running:
```
bash install.sh
```
Running `bash install.sh -h` will also give you some basic install options. 

If you want more flexibility (you will need Python 3.12), you can install each package with `pip`: `numpy`, `scipy`, `matplotlib`, `pandas`, `eryn`, `corner`, `chainconsumer`, `lisaanalysistools`, `fastlisaresponse`, `gbgpu`, `bbhx`, `fastemriwaveforms`.

Once installation is completed, `cd` to the tutorial directory and run `jupyter lab`. Select your tutorial and begin!

# Code of Conduct

In [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), you will find the workshop code of conduct. It is heavily based on the LISA Consortium code of conduct. We strongly advise anyone who uses these tutorials in any way to follow this code of conduct. 

# Authors

* **Michael Katz**

# Contributors / Organizing Committee

* Nikos Karnesis
* Natalia Korsakova
* Argyro Sasli
* Albin Nilsson
* Rodrigo Tenorio
* Durgesh Rai
* Lorenzo Speri

