# Sexual Predator Detection Datasets

This repo is for preprocessing and creating the datasets
- PAN12,
- ChatCoder2 (CC2),
- VTPAN, and
- PANC.

Datasets can be saved as both
- .tsv files and
- datapacks, compatible with [Chat Visualizer](https://github.com/matthias-vogt/chat-visualizer). More information about datapack files can also be found in the [Chat Visualizer](https://github.com/matthias-vogt/chat-visualizer) repo.

## Requirements

- A good amount of RAM
- 4GB of disk space
- The [PAN12](https://pan.webis.de/clef12/pan12-web/) [1] dataset (can be obtained from [Zenodo](https://zenodo.org/record/3713280))
- If you also want to create the PANC dataset you need the [ChatCoder2](https://www.chatcoder.com/drupal/index.php) [2] Dataset, which is available [by request to April Edwards](https://www.chatcoder.com/drupal/DataDownload)

## Usage

The `create_everything.sh` script creates all datasets. They can then be found in the respective `{Dataset}/csv/` and `{Dataset}/datapacks/` directories.

To create a datapack, use `python {Dataset}/create_datapack.py`. This command has to be run from the base directory of the repository (i.e. this directory).

To create a csv file, first create a datapack of the respective dataset and then use `python create_csv.py --dataset {Dataset}`.

You might want to make changes to the code and change chat preprocessing, filtering etc. In this case you can also add `--datapackID {SomeID}` to the commands to identify different versions of a dataset.


## References
[1] Inches, G. & Crestani, F. Overview of the International Sexual Predator Identification Competition at PAN-2012. in CLEF (Online Working Notes/Labs/Workshop) 30, (2012).

[2] McGhee, I. et al. Learning to identify Internet sexual predation. Int. J. Electron. Commer. (2011). doi:10.2753/JEC1086-4415150305
