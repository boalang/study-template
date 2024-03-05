# The Boa Study Template

Boa is a domain-specific language and infrastructure that eases mining software repositories. Boa's infrastructure leverages distributed computing techniques to execute queries against hundreds of thousands of software projects very efficiently.

Boa's Study Template was designed to aid researchers who want to use Boa in a research study.  The goal was two-fold: first, to make it easier to write, run, and process Boa queries and outputs, and second, to enable better replication of research.

To accomplish these goals, the study template automatically manages a lot of the details such as when to run a Boa query, when to download its results, and automatic conversion of the output to CSV.  Additionally, the study template provides some helper functions in Python to make it easier to analyze that data.  Generally, researchers using the study template simply need to write their Boa queries, write the Python analyses to process the output, and then run `make` to execute the study.  The study template figures out what queries need to be run, what outputs need to be downloaded, and what analyses need to be run based on what files have changed since the last run.

Moreover, the study template has reproducibility in mind.  It automatically records information about the Boa jobs that were run and stores the data in a converted, compressed Parquet file.  It also provides `make` targets to produce replication package ZIP files that contain all the data and analyses needed to reproduce the study.  This includes the Boa queries, the Python analyses, the data, and the generated figures and tables.

The study template also provides support for publishing your replication package on Zenodo.  This is a great way to get a DOI for your replication package and to make it easy for others to cite your work.  The study template will automatically generate a Zenodo metadata file and upload the replication package to Zenodo.  By default, it will support double-blinded submissions and provides an easy way to unblind your replication after your paper is accepted.
