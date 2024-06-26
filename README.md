# analysis_utils
 
Utilities for data science analysis.
Analyze co-change over time, twin experiments, feature stability, ploting and more.

# Corrective commit probability: a measure of the effort invested in bug fixing
Supplementary Materials of the ["Corrective commit probability: a measure of the effort invested in bug fixing"](https://www.cs.huji.ac.il/~feit/papers/CCP21SQJ.pdf) paper by Idan Amit and [Dror G. Feitelson](https://www.cs.huji.ac.il/~feit/).

Please cite as
``` 
@Article{Amit2021CCP,
author={Amit, Idan
and Feitelson, Dror G.},
title={Corrective commit probability: a measure of the effort invested in bug fixing},
journal={Software Quality Journal},
year={2021},
month={Aug},
day={05},
abstract={The effort invested in software development should ideally be devoted to the implementation of new features. But some of the effort is invariably also invested in corrective maintenance, that is in fixing bugs. Not much is known about what fraction of software development work is devoted to bug fixing, and what factors affect this fraction. We suggest the Corrective Commit Probability (CCP), which measures the probability that a commit reflects corrective maintenance, as an estimate of the relative effort invested in fixing bugs. We identify corrective commits by applying a linguistic model to the commit messages, achieving an accuracy of 93{\%}, higher than any previously reported model. We compute the CCP of all large active GitHub projects (7,557 projects with 200+ commits in 2019). This leads to the creation of an investment scale, suggesting that the bottom 10{\%} of projects spend less than 6{\%} of their total effort on bug fixing, while the top 10{\%} of projects spend at least 39{\%} of their effort on bug fixing --- more than 6 times more. Being a process metric, CCP is conditionally independent of source code metrics, enabling their evaluation and investigation. Analysis of project attributes shows that lower CCP (that is, lower relative investment in bug fixing) is associated with smaller files, lower coupling, use of languages like JavaScript and C{\#} as opposed to PHP and C++, fewer code smells, lower project age, better perceived quality, fewer developers, lower developer churn, better onboarding, and better productivity.},
issn={1573-1367},
doi={10.1007/s11219-021-09564-z},
url={https://doi.org/10.1007/s11219-021-09564-z},
pages={1--45},
publisher={Springer}

}

```

It was later extended as part of

["Follow Your Nose -- Which Code Smells are Worth Chasing?"](https://arxiv.org/pdf/2103.01861.pdf) paper by Idan Amit, Nili Ben Ezra, and [Dror G. Feitelson](https://www.cs.huji.ac.il/~feit/).

Please cite as
``` 
@misc{amit2021follow,
      title={Follow Your Nose -- Which Code Smells are Worth Chasing?}, 
      author={Idan Amit and Nili Ben Ezra and Dror G. Feitelson},
      year={2021},
      eprint={2103.01861},
      archivePrefix={arXiv},
      primaryClass={cs.SE}
}
```

The repository itself should be cited as
```
@article{Amit2021Analysis
, title={Analysis utilities}, 
DOI={10.5281/zenodo.5179861},
publisher={Zenodo}
, author={Idan Amit}
, year={2021}
, month={Aug}}

```

See here the [linguistic commit classification](https://github.com/evidencebp/commit-classification)

See here the [corrective commit probability code](https://github.com/evidencebp/corrective-commit-probability)

# Versions

Version used for "ComSum: Commit Messages Summarization and Meaning Preservation" by Leshem Choshen and Idan Amit.
[![DOI](https://zenodo.org/badge/254577147.svg)](https://zenodo.org/badge/latestdoi/254577147)

Live version is updating at https://github.com/evidencebp/analysis_utils/

Adding the setup, to allow pipi install, changed the repository structure.
To run the code of the related paper, use version up to commit e4f9ba0

Repository will keep advancing.


