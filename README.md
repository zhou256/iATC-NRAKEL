# iATC-NRAKEL

***Functions*** : Recognizing the Anatomical Therapeutic Chemical (ATC) classes of first level for given drugs.
Seven drug networks were constructed according to the chemical associations reported in STITCH and KEGG, from which informative drug features were produced via Mashup. Obtained features were tackled by random k-Labelsets (RAKEL) algorithm, in which support vector machine (SVM) was adopted as prediction engine, to build the multi-label classifier, iATC-NRAKEL. Through rigorous 10-fold cross-validation, iATC-NRAKEL yielded the absolute true of 74.51% and accuracy of 76.56%. The Jackknife test results were 75.93% (absolute true) and 77.86% (accuracy), which were much higher than those yiedled by all previous classifers.

<div align=center><img src="https://github.com/zhou256/iATC-NRAKEL/blob/master/iATC-NRAKEL.jpg" width="1100" height="650" />
</div>


## Meka command
Suppose the Meka installation root directory is "E:\meka1.9.2".
### 1. Ten-fold cross-validaion command for Meka:
cd E:\meka1.9.2             
E:\meka1.9.2>  java -cp "./lib/*" meka.classifiers.multilabel.RAkEL -M 10 -k 14 -P 0 -N 0 -S 0 -x 10
 -R -verbosity 7 -t path/Meka3883_700_pinjie.arff -W weka.classifiers.functions.SMO -- -C 1.0 -L 0.001
-P 1.0E-12 -N 0 -V -1 -W 1 -K "weka.classifiers.functions.supportVector.PolyKernel -E 1.0 -C 250007"
 -calibrator "weka.classifiers.functions.Logistic -R 1.0E-8 -M -1 -num-decimal-places 4" > path/cross_10_3883_folds.txt

### 2. Jackknife test command for Meka:
cd E:\meka1.9.2              
E:\meka1.9.2>  java -cp "./lib/*" meka.classifiers.multilabel.RAkEL -M 10 -k 14 -P 0 -N 0 -S 0 -x 3883
 -R -verbosity 7 -t path/Meka3883_700_pinjie.arff -W weka.classifiers.functions.SMO -- -C 1.0 -L 0.001
-P 1.0E-12 -N 0 -V -1 -W 1 -K "weka.classifiers.functions.supportVector.PolyKernel -E 1.0 -C 250007"
 -calibrator "weka.classifiers.functions.Logistic -R 1.0E-8 -M -1 -num-decimal-places 4" > path/jackknife.txt


## Other requirements
The codebase is implemented in Python 3.5.6. Information of used packages is listed below.
```Python3.5.6            
   Matlab 2016a
   Meka 1.9.2              download address: http://meka.sourceforge.net/
   Mashup                  download address: http://mashup.csail.mit.edu
```
