# minimgnt (miniMAGENTA)

A mini subset of the [MAGENTA](https://www.broadinstitute.org/mpg/magenta/) software, reimplemented in Python.
The `minimgnt` enables users to calculate the corrected "gene association score" from a GWAS result, according to MAGENTA's method.

For the full functionality of MAGENTA (i.e. GSEA analysis), try [MAGENTApy](https://github.com/mkanai/MAGENTApy), an experimental complete port of MAGENTA to Python. (Note: `MAGENTApy` is still under beta.)

## Usage
```
./minimgnt.py score_filename [--out OUT] [-j CPUS] [--not-remove-HLA] [--remove-NA] [--no-rsid]
```

* *`score_filename`* : GWAS SNP score filename.
    * [columns]
        1. rsID (*optional with `--no-rsid` flag.*)
        2. chromosome
        3. bp
        4. z-score (*optional*)
        5. p-value

* `--out OUT` : output filename prefix. (default: minimgnt)
* `-j/--cpus CPUS` : a number of cpus used for computation. (default: 1)
* `--not-remove-HLA` : do not remove genes in HLA region from a result. (default: False)
* `--remove-NA` : remove genes with NA score from the output. (default: False)
* `--no-rsid` : use this flag when a score file doesn't contain a rsID column. (default: False)
    * This file format corresponds to *Input file #1* of the original MAGENTA.
* `--HLA-start HLA_START` : start position (bp) of HLA region in chr6. (default: 25,000,000)
* `--HLA-end HLA_END` : end position (bp) of HLA region in chr6. (default: 35,000,000)
* `--boundary-upstream BOUNDR_UPSTR` : added distance (bp) upstream to gene's start position. (default: 110,000)
* `--boundary-downstream BOUNDR_DOWNSTR` : added distance (bp) downstream to gene's end position. (default: 40,000)

## Reference Data

All pre-installed reference data are located at `./minimgnt/data`.

* `AllHumanGeneChrPosStrandNames_RefSeq_hg19_072111.txt`
    * The data were retrieved from RefSeq ver. 48 (released at July 10, 2011), using the same dataset as the MAGENTA software.
    * [columns]
        1. chromosome
        2. txStart (bp)
        3. txEnd (bp)
        4. strand (1: forward, 2: reverse)
        5. name
* `AllHumanMiRNAChrPosStrandNames_miRBase_hg19_062413.txt`
    * The data were retrieved from miRBase release 20 (released at June 24, 2013).
    * [columns] same as the above.
* `CEU_HapMap_pruned_SNPs_ChrNumPos_hg19_072111.txt`
    * The LD information used for correcting "gene association score" is based on the CEU HapMap dataset.
    * For other ethnic samples, you can calculate similar properties using the appropriate HapMap dataset as described in Segrè et al. (2010).
    * [columns]
        1. chromosome
        2. position (bp)
* `hotspot_boundaries_b37_hg19_072111.txt`
    * [columns]
        1. chromosome
        2. start (bp)
        3. end (bp)

## Install
```
git clone https://github.com/mkanai/minimgnt
```
### Requirements
* numpy
* scipy
* pandas
* six
* argparse
* futures

To install these requirements,
```
[sudo] pip install -r requirements.txt
```

## Credits

* The original [MAGENTA](https://www.broadinstitute.org/mpg/magenta/) was written by Ayellet Segre, Mark Daly, and David Altshuler of The Broad Institute.
    * Ayellet V. Segrè, DIAGRAM Consortium, MAGIC investigators, Leif Groop, Vamsi K. Mootha, Mark J. Daly, and David Altshuler (2010). **Common Inherited Variation in Mitochondrial Genes is not Enriched for Associations with Type 2 Diabetes or Related Glycemic Traits.** [PLoS Genetics Aug 12;6(8). pii: e1001058.](http://journals.plos.org/plosgenetics/article?id=10.1371/journal.pgen.1001058)
* This minimgnt (miniMAGENTA) was written by [Masahiro Kanai](http://mkanai.github.io/), reimplementing the calculation of "gene associatino score" feature in Python.
