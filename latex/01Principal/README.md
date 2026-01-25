Fecha de actualización martes 01 de enero de 2024

# EPN FIS THESIS (for LaTeX)

## INTRODUCTION
This collection of LaTeX files is a thesis template intended to work with 
PDFLatex 2e. It includes the official title page from Escuela Politécnica 
Nacional and relies on an extensible structure. The sample files are 
written in English and Spanish but can be easily changed to another 
language thanks to UTF-8 encoding and redefining few variables.


## MANIFEST OF FILES AND FOLDERS

### 01Principal:
- main.tex:     the main LaTeX file of the project.
- README.txt:   this file
- tesis.cls:    required packages and definition of commands.
    
### 02Figures:
- Includes images and illustrations according to each chapter.

### 03Tables:
- Includes tables according to each chapter.

### 04Sections:

**01CoverPage:**
- It includes the two title pages established by the EPN.

**02Preliminary:**
- It includes the certification, declaration, dedication, and acknowledgments contained within commands.

**03ContentOfDocument:**
- It includes all the writing of the document such as the chapters, the summary and the conclusions. Also, the main file is 00ContentOfDocument.tex

**04References:**
- It includes the bibliography.bib file which contains the entire bibLatex database and the 00References.tex file contains the basic settings for how all bibliographic references will be printed.

**05Annexes:**
- It includes all the annexes.


## NOMENCLATURE
You can avoid putting the chapter number as long as they are inside 
the respective chapter folder. Except in the \label{}.

### General:
```
chapter-section-type
```

### Figures:
```
file:   C-chapterNumber-F(figure)-numeration
label:  C-chapterNumber-F(figure)-numeration:shortDescriptiveName
```

### Tables:
```
.tex:   C-chapterNumber-T(table)-numeration
label:  C-chapterNumber-T(table)-numerationn:shortDescriptiveName
```

*Examples:*
```
General:    01Chapter/01-00-Chapter.tex

Figure:     02Figures/C1F1:figureExample.png        or
            02Figures/01Chapter/F1:figureExample.png
            \label{C1F1:figureExample}

Table:      03Tables/C1T1:tableExample.tex          or
            03Tables/01Chapter/T1:tableExamplee.tex
            \label{C1T1:tableExample}
```

## USING COMMANDS
The numbers are used to explain the operation of the commands, 
as the respective user can modify within the code.

### Declaration
Instead of 1, you must write their names
```
\declaration{1}
```

  
### Certification
Instead of 1, you must write their names
```
\certification{1}
```

### Dedication
Instead of 1, you must write the entire dedication paragraph
```
\dedication{1}
```

### Acknowledgements
Instead of 1, you must write the entire acknowledgements paragraph
```
\acknowledgements{1}
```

### Signature
1. Name
2. Job
```
\signature{1}{2}
```

### Resumen - Abstract
1. Language -> spanish or english
2. Summary paragraph
```
\abstract{1}{2}
```

## CREDITS
This template has been created by EPN FIS.
