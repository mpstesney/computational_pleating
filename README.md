Computational Pleating
======================

This repository contains the code for a workflow that converts Rhino model geometry into a format suitable for use in origami simulators. The [original work](https://courses.ideate.cmu.edu/16-455/s2020/1998/pleating-final-report/) was completed for the Spring '20 Human-Machine Virtuosity: Hybrid Skill, Fabrication, and Design course at Carnegie Mellon University, taught by Dr. Garth Zeglin and Prof. Joshua Bard. My teammates were Ryan Smerker and Ruohai Ge.

Our workflow integrates traditional pleating and folding techniques into a digital design process. We used the excellent [Complete Pleats](https://www.amazon.com/Complete-Pleats-Pleating-Techniques-Architecture/dp/1780676018/ref=sr_1_1?dchild=1&keywords=paper+pleating&qid=1623266145&sr=8-1) by Paul Jackson as our reference to folding techniques and annotation. The FOLD format was invented to be the common interchange format for computational oragami and therefore we chose it as the output format of our tool. Specifications and documentation can be found [here](https://github.com/edemaine/fold). To view FOLD files we used this online [origami viewer](https://origamisimulator.org). The viewer can also export 3D geometry in STL and OBJ formats.

### Core Workflow

<img src="/images/basic_workflow.jpg" alt="basic workflow" width="500" />
<img src="/images/basic_examples.jpg" alt="basic workflow" width="500" />

### Results

Each team member explored and expanded the core workflow by developing their own creative scripts to algorithmically generate fold patterns. Check out the [final project report](https://courses.ideate.cmu.edu/16-455/s2020/1998/pleating-final-report/) for the great results produced by my teammates.

My workflow introduces an alternate representation method to the core tool. In addition to using single lines to represent individual folds, single line representations are expanded to include pleats of multiple folds, e.g. knife pleats. Rhino layers for left and right-hand knife pleats are added for the designer’s use.

Paper studies were used to understand the pattern of the resultant folds at an intersection of pleats with multiple folds. Because the sequence of each intersection is required to be defined, a second layer of complexity is available for the designer to manipulate.

<img src="/images/intersection_studies.jpg" alt="intersection studies" width="500" />

The work below introduces the formal possibilities that can be explored when intersecting knife pleats. The order of the pleats was created using simple looping algorithms. However, the nature of this intersection representation affords many other possibilities to assign order values. As is seen below, the interplay between even simple variations in the knife fold direction and order of folding creates a broad variation in the formal and performance qualities of the 3D object. The folds below are rendered in Rhino.

<img src="/images/artifact1.png" alt="artifact 1" width="500" />

Knife fold pattern 1

<img src="/images/artifact2.png" alt="artifact 3" width="500" />

Knife fold pattern 2

<img src="/images/artifact3.png" alt="artifact 3" width="500" />

Knife fold pattern 3

<img src="/images/artifact4.png" alt="artifact 4" width="500" />

Knife fold pattern 4

<img src="/images/fold_animation.gif" alt="fold animation" width="500" />

Demonstration of the variable dynamic qualities of the fold patterns

### Future work:

* Add the code that created examples of the geometry shown here and in the project report
* Package code as a Grasshopper plug-in and share on [Food4Rhino](https://www.food4rhino.com/en)
