%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%	EPN FIS THESIS for LaTeX files	 01 January 2024
%% %%	For any information please send an e-mail to:
%% %%		epn.fis@epn.edu.ec
%% %%
%% %%	Initial class provided by:
%% %%		EPN FIS
%% %%   Modified by:
%% %%		--
%% %%   Versions:
%% %%		v1.0
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%% IDENTIFICATION
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{thesis}[01/01/2024 EPN FIS THESIS paper class]

%%% PRELIMINARY DECLARATIONS
\LoadClass[11pt,a4paper]{report}
\RequirePackage[T1]{fontenc}                                            % Font encodigns -> Mapping of the character codes to the font glyphs that are used to typeset your output.
\RequirePackage[utf8]{inputenc}                                         % Specify an input encoding (for example, ASCII, ISO Latin-1 or Macintosh)
\RequirePackage[spanish]{babel}                                         % Spanish Traduction
\RequirePackage{helvet}                                                 % Fonts Package (Arial, Times, Courier)
\RequirePackage[
    top=3cm,
    left=3cm,
    right=2.5cm,
    bottom=2.5cm]{geometry}                                             % Page margins
\RequirePackage[
	colorlinks=true, 
	linkcolor=black, 
	citecolor=black, 
	urlcolor=black, 
	hyperfootnotes=false]{hyperref}                                     % Handle cross-referencing commands in LATEX to produce hypertext links in the document.
\RequirePackage{amsmath}                                                % General Math package
\RequirePackage{amsfonts}                                               % Math fonts
\RequirePackage{amssymb}                                                % Math symbols
\RequirePackage{float}                                                  % Improves the interface for defining floating object
\RequirePackage{csquotes}                                               % Provides advanced facilities for inline and display quotations
\RequirePackage{graphicx}                                               % The ‘extended’ or ‘enhanced’ graphics package.
\RequirePackage{tabularx}                                               % The extended tabular package.
\RequirePackage{array}                                                  % For table array
\RequirePackage{booktabs}                                               % For \toprule etc. in tables
\RequirePackage{multirow}
\RequirePackage{longtable}
\RequirePackage[table]{xcolor}
\usepackage{datetime}

\newdateformat{monthyeardate}{%
    \monthname[\THEMONTH] \THEYEAR
}
%% MINITOC
\RequirePackage[spanish]{minitoc}                                       % Mini-tables-of-contents
% Change fonts of minitoc
\renewcommand{\mtifont}{\large\sffamily}                                % Title
\renewcommand{\mtcfont}{\small\sffamily}                                % Chapters (I guess)
\renewcommand{\mtcSfont}{\small\sffamily}                               % Sections
\renewcommand{\mtcSSfont}{\small\sffamily}                              % Subsections
\renewcommand{\mtcSSSfont}{\small\sffamily}                             % Subsubsections

%Adding a caption to an equation in LaTeX
\usepackage{caption}
\DeclareCaptionType{equ}[][]

%% TITLES
\RequirePackage{titlesec}                                               % Interface to sectioning commands for selection from various title styles.
% Chapters
%\titleformat{\chapter}[hang]{
%        \bfseries\fontsize{16pt}{20pt}\selectfont
%    }{
%        \MakeUppercase{}\ \thechapter.}{5.0mm}{\MakeUppercase
%    }

% Sections
\titleformat{\section}[hang]{
        \bfseries\fontsize{14pt}{20pt}\selectfont
    }{
        \thesection.}{5.0mm}{
    }
    
% Subsections
\titleformat{\subsection}[hang]{
        \bfseries\fontsize{14pt}{20pt}\selectfont
    }{
        \thesubsection.}{5.0mm}{
    }
    
% SubSubSections
\titleformat{\subsubsection}[hang]{
        \bfseries\fontsize{12pt}{20pt}\selectfont
    }{
        \thesubsubsection.}{5.0mm}{
    }

% Paragraph
\titleformat{\paragraph}[hang]{
        \bfseries\fontsize{12pt}{20pt}\selectfont
    }{
        }{}{
    }
    
\titlespacing{\paragraph}{0pt}{4pt}{3pt}

%% Bibliography
\usepackage[style=ieee]{biblatex}                                       % BibLATEX uses its own data backend program called “biber” to read and process the bibliographic data.
\addbibresource{../04Sections/04References/bibliography.bib}

%% Latin Sample Text Pack
\RequirePackage{lipsum}                                                 % Create text in Latin, ideal for visualizing the changes.

%%% NEW COMMANDS
%% Font General
\renewcommand{\familydefault}{\sfdefault}

% Note:
% \sf Command turns on sans serif mode for uppercase and lowercase letters and digits, and for uppercase Greek.
% \bf Used to turn on boldface; affects uppercase and lowercase letters, and digits.
% \centering Center text

%% Certification Section
\newcommand{\certification}[1]{
    \newpage
    \chapter*{\sf\bf\centering\fontsize{14}{20pt}\selectfont CERTIFICACIÓN}
    {
        {\setlength{\parindent}{0pt} 
        Yo, #1 declaro que el trabajo de integración curricular aquí descrito es de mi autoría; que no ha sido previamente presentado para ningún grado o calificación profesional; y, que he consultado las referencias bibliográficas que se incluyen en este documento.
        
        \vspace{0.5cm}
        
        Asimismo, declaro que he utilizado la herramienta de inteligencia artificial Gemini únicamente como apoyo en la codificación, redacción y revisión de literatura, sin atribuirle autoría, y que todo el contenido derivado ha sido revisado, validado y es de mi exclusiva responsabilidad.
        \begin{center}
            \signature{(#1)}{}
        \end{center}    

        \vspace{2cm}
        
        Certifico que el presente trabajo de integración curricular fue desarrollado por #1, bajo mi supervisión.
        \begin{flushright}
            \signature{(PHD. VICTOR VICENTE VELEPUCHA BONETT)}{DIRECTOR}
            %\signature{(TITULO. NOMBRE1 NOMBRE2 APELLIDO1 APELLIDO2)}{CO DIRECTOR}
        \end{flushright}
        }
    }
    %{\noindent Certifico que el presente trabajo fue desarrollado por #1, bajo mi supervisión.}
}

%% Declaration Section
\newcommand{\declaration}[1]{
    \newpage
    \chapter*{\sf\bf\centering\fontsize{14}{20pt}\selectfont DECLARACIÓN DE AUTORÍA}
    {
        {\setlength{\parindent}{0pt} 
        A través de la presente declaración, afirmamos que el trabajo de integración curricular aquí descrito, así como el (los) producto(s) resultante(s) del mismo, son públicos y estarán a disposición de la comunidad a través del repositorio institucional de la Escuela Politécnica Nacional; sin embargo, la titularidad de los derechos patrimoniales nos corresponde a los autores que hemos contribuido en el desarrollo del presente trabajo; observando para el efecto las disposiciones establecidas por el órgano competente en propiedad intelectual, la normativa interna y demás normas. 
    
        \vspace{2cm}
        
        {#1} \\
        {PHD. VICTOR VICENTE VELEPUCHA BONETT} \\
        {EDWIN ANDRÉS CANTUÑA GUANO} \\
        {JAIRO RENE SIMBAÑA CAIZA} \\
        }
    }
}


%% Dedication Section
\newcommand{\dedication}[1]{
    \newpage
    \chapter*{\sf\bf\centering\fontsize{14}{20pt}\selectfont DEDICATORIA}
    {
        {\setlength{\parindent}{0pt} 
        #1}
    }
}

%% Acknowledgements Section
\newcommand{\acknowledgements}[1]{
    \newpage
    \chapter*{\sf\bf\centering\fontsize{14}{20pt}\selectfont AGRADECIMIENTOS}
    {
        {\setlength{\parindent}{0pt} 
        #1}
    }
}

%% Signature
\newcommand{\signature}[2]{
    \vspace{2.5cm}
    \makebox[2.82in]{\hrulefill}    \\
    \bf{#1}                         \\
    \bf{#2}
}

%% Resumen - Abstract
\renewcommand{\abstract}[3]{
    \ifthenelse{\equal{#1}{spanish}}{
        %% Resumen
        \chapter*{\sf\bf\centering\fontsize{14}{20pt}\selectfont RESUMEN}
        {
            {\setlength{\parindent}{0pt} 
                #2}
        } \\
        %% Palabras Clave
        {
            {\setlength{\parindent}{0pt} 
                \textbf{\textit{Palabras Claves -}} #3}
        }
    }{\ }
    \ifthenelse{\equal{#1}{english}}{
        %% Abstract
        \chapter*{\sf\bf\centering\fontsize{14}{20pt}\selectfont ABSTRACT}
        {
            {\setlength{\parindent}{0pt} 
                #2}
        } \\
        %% KeyWords
        {
            {\setlength{\parindent}{0pt} 
                \textbf{\textit{Keywords -}} #3}
        }
    }{\ }
    
}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Cover
%\usepackage{eso-pic}

% Graphics
    %\usepackage{tikz}
    %\usetikzlibrary{shapes,arrows}
    %\usetikzlibrary{plotmarks}
    %\usepackage{pgfplots}
    %\pgfplotsset{compat=newest}
    %\pgfplotsset{plot coordinates/math parser=false}
    %\newlength\figureheight
    %\newlength\figurewidth
    %\usepackage{textpos}
    %\usepackage{etoolbox}
    
%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   Representar Código Fuente
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Necesario para la inclusión de código fuente 
\usepackage{listings}
% Necesario para resaltado de la sintaxis
\usepackage{color}
% Colores de resaltado 
\definecolor{letraAzul}{cmyk}{1,0.5,0,0.5}
\definecolor{lstrule}{RGB}{158,180,204}
\definecolor{fondo}{RGB}{245,245,250}
\definecolor{gray}{rgb}{0.5,0.5,0.5}
\definecolor{darkviolet}{rgb}{0.5,0,0.4}
\definecolor{darkpink}{rgb}{0.8,0.3,0.5}
\lstset{ %
  language=Java,
  basicstyle=\footnotesize\color{letraAzul},
  numbers=left,
  numberstyle=\scriptsize\color{gray},
  numberfirstline=true,
  firstnumber=1,
  stepnumber=5,
  numbersep=8pt,
  backgroundcolor=\color{fondo},
  showspaces=false,
  showstringspaces=false,
  showtabs=false,
  frame=single,
  rulecolor=\color{lstrule},
  tabsize=4,
  captionpos=t,
  breaklines=true,
  breakatwhitespace=false,
  title=\lstname,
  keywordstyle=\bfseries\color{darkviolet},
  commentstyle=\color{gray},
  stringstyle=\color{darkpink},
  escapeinside={\%*}{*)},
  morekeywords={*,...}
  inputencoding=utf8,
  emphstyle=\color{red},
  extendedchars=true,
  literate={á}{{\'a}}1
         {é}{{\'e}}1
         {í}{{\'i}}1
         {ó}{{\'o}}1
         {ú}{{\'u}}1
         {ñ}{{\~n}}1
}

%%% EXTRA CONFIGURATIONS
%% Line Spacing
\linespread{1.5}
% Note: If you use either the babel or polyglossia package you'll have to change the name for the particular language you use with babel or polyglossia.

\addto\captionsspanish{% Replace "english" with the language you use
    %% Change title of Table of Contents (Índice General)
    %\renewcommand{\contentsname}{Tabla de Contenidos}
    %% Change title of List Of Figures
    %\renewcommand{\listfigurename}{Lista de Figuras}
    %% Change title of List Of Tables
    \renewcommand{\listtablename}{Índice de Tablas}
    %% Change name of Tables
    \renewcommand{\tablename}{Tabla}
    %% Change title of Minitoc
    %\renewcommand{\mtctitle}{Mini Indice}
}

%%% REFERENCES
% 1. https://ondahostil.wordpress.com/2016/09/14/lo-que-he-aprendido-definir-comando-en-latex/
% 2. http://elclubdelautodidacta.es/wp/2012/07/latex-controlando-la-indentacion-de-los-parrafos/#:~:text=Si%20no%20te%20gusta%20indentar,p%C3%A1rrafo%20o%20en%20el%20siguiente.
% 3. https://mirrors.ucr.ac.cr/CTAN/macros/latex/base/ifthen.pdf
% 4. https://latexref.xyz/dev/latex2e-es.html#Acerca-de-este-documento
% 5. https://www.latex-project.org/help/documentation/usrguide.pdf
% 6. https://www.javatpoint.com/latex-fonts-size-and-styles
% 7. https://www.youtube.com/watch?v=mY2JquEjnNI
% 8. https://linorg.usp.br/CTAN/macros/latex/contrib/titlesec/titlesec.pdf
% 9. https://tex.stackexchange.com/questions/28516/how-to-change-the-title-of-toc
% 10. https://texblog.org/2011/09/09/10-ways-to-customize-tocloflot/
% 11. https://tex.stackexchange.com/questions/312979/removing-renaming-the-title-of-minitoc
