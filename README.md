<img src="doc/pict/Frame.png" alt="drawing" style="height: 35px;"/> 

# FRAME: Floorplanning with RectilineAr ModulEs

`FRAME` is a framework for chip planning where modules can be implemented as rectilinear
blocks.

If we consider _floorplanning_ as an evolutive process, a floorplan can be represented at 
different levels of abstraction. Depending on the level of detail, a module can be seen 
as a point, a circle, a rectangle or a rectilinear shape. 
When floorplanning is automated, a sequence of optimization tasks
based on mathematical models is typically envisioned, as shown in the figure below.

<img src="doc/pict/FPprocess.png" alt="Evolutive floorplanning" style="height: 180px;"/>

Modern floorplans require shapes beyond the conventional rectangles, e.g., L-shapes, 
T-shapes or even  C-shapes. Moreover, a close interaction with the designer is often 
required, e.g., by fixing blocks or by defining non-rectangular dies. Using a simple trick,
non-rectangular dies can be represented by including _fake_ blocks that determine the 
blockages inside the rectangular  die, as shown in the following figure.

<img src="doc/pict/FakeFixedBlocks.png" alt="Fake and fixed blocks" style="height: 200px;"/>

The die where the system must be floorplanned may contain dedicated regions. 
A typical example is an
FPGA die with slices dedicated to BRAMs or DSPs, as shown in the figure below.

<img src="doc/pict/FPGA_structure.png" alt="Die with dedicated regions" style="height: 200px;"/>

Modules may use resources from different regions and floorplanning must take into account 
where these resources are located on the die.

## Installation for development

Install [Python 3](https://www.python.org/downloads/) and [Git](https://git-scm.com/download/).
Then, open a terminal and execute the following commands, depending on your operating system:

#### Linux or macOS
```
git clone https://github.com/jordicf/FRAME.git
cd FRAME
python -m venv venv
source venv/bin/activate
pip install setuptools
pip install -e .
```

#### Windows
```
git clone https://github.com/jordicf/FRAME.git
cd FRAME
python -m venv venv
.\venv\Scripts\activate
pip install setuptools
pip install -e .
```

If you use PyCharm, to configure the project Python interpreter go to File | Settings... |
Project: FRAME | Python Interpreter.
Then click the gears icon, Add..., and choose Existing environment and select Interpreter as the one
in the `FRAME/venv` folder. 

## Testing

To run all the tests, execute the following command from the project folder:

```
python -m unittest discover -v -s tests
```