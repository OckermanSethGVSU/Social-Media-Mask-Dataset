# Social Media Mask Dataset

The Social Media Mask Dataset is a dataset made up of Twitter Images intended for the training of Convalutional Neural Networks to detect masks in images and video. In this case, the term masks refer to a device worn on the face intended to reduce the spread of respiratory illness. Two categories of images exist: "mask" and "no_mask". All efforts were made to ensure each image contains a person and is viable for training CNN models. For more details the makeup of the dataset and the collection process refer to the accompanying paper published in IEEE ICMLA 2022.   

The initial published version of this dataset can also be found on [Zenodo](https://doi.org/10.5281/zenodo.5813804).


## Instructions for Download Script Use
Below is a step by step walkthrough on how to successfully use our download script.


### Before you begin

Before running our script, you need to register for a free Twitter developer account. Instructions for doing so can be found on [Twitter's Developer Website](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api). Once you have an account, you will be assigned a bearer token for the V2 API. Keep it in a safe place for later.


Our script makes use of Bash commands and was developed on Ubuntu Linux. If you are on a Linux System, and are using the Bash kernel (as far as the authors are aware) you should have no operating system issues. If you are on a Windows system, you will need to enable the Linux subystem for Linux. Instructions to do so on a Windows 10 machine can be found [the windows central website ](https://www.windowscentral.com/install-windows-subsystem-linux-windows-10) while Windows 11 instructions are found on the the [pure info tech website](https://pureinfotech.com/install-wsl-windows-11/) (full credit to these guides go to their respective authors).


Ensure you have Python3 installed on your device. Instructions to install Python3 on a linux machine or the linux subsystem on a windows machine can be found on the [Hitch Hikers Guide to Python](https://docs.python-guide.org/starting/install3/linux/). We developed and tested this script using Python 3.8.

### Running the Script
To run our script use the command line to navigate to the directory with `testing.json`, `training.json`, and `download_dataset.py`. Then enter the simple command `python3 download_dataset.py`. The script will then ask you if you are ready to continue. If you enter yes, the script will ask for your Twitter bearer token. Copy paste it into the command line with no extra spaces or new lines. Your download should now begin.

## Guide to Understanding the Dataset
Below are annotated examples of dataset entries and a numerical breakdown of the contents of the Social Media Mask Dataset.

### Annotated Examples  
Due to Twitter's TOS, we cannot directly publish Twitter images. Instead, we publish Tweet keys along with information our script uses to download the target image. An Annotated example is shown below.

![Annotated_Example](figures/instance.png)


### Numerical Breakdown
As of summer of 2020, there are 12,482 masked and 116,620 unmasked images, totaling approximately 129,000 images (129,102).


### Citation

If you use this dataset, please cite

```
@INPROCEEDINGS{10068950,
  author={Ockerman, Seth and Carrier, Erin},
  booktitle={2022 21st IEEE International Conference on Machine Learning and Applications (ICMLA)}, 
  title={Predicting COVID-19 Case Counts using Twitter Image Data}, 
  year={2022},
  volume={},
  number={},
  pages={1695-1701},
  keywords={COVID-19;Social networking (online);Time series analysis;Blogs;Urban areas;Predictive models;Data models;COVID-19;Twitter analysis;predictive time series;computer vision},
  doi={10.1109/ICMLA55696.2022.00260}}
```