# IDEAL

#### _An Open-Source Identifier Name Appraisal Tool_

## Usage

<details>
	<summary><b> 🔵 Docker (recommended)</b></summary>
	<br><b>🚧🚧🚧 IMPORTANT</b>: Currently through the Dockerfile you will only be able to run tests. <br> 
	<br>
	<ol>
		<li>Clone the repo</li>
		<li>
		Build the Dockerfile<br>
		<code>docker build . -t ideal</code>
		</li>
		<li>
		Run the Dockerfile<br>
		<code>docker run -it ideal</code><br>
    <b>Optionally</b>, you can mount the root folder when running the container to use files from the host directly in the container with the following command (assumed to be run from the root project folder):<br>
      <code>docker run -v ./:/app/ -it ideal</code>
    </li>
    </ol>
  This ensures all the required executables and dependencies are installed, and runs unit and integration tests inside the container.<br>
  The image is also available on DockerHub <a href="https://hub.docker.com/r/xrenegade100/ideal">at this link</a>.
</details>
<details>
  <summary><b>Manual Installation</b></summary>
  <a href="./documentation/IDEAL/SetupAndUse.md">Here</a> you can find some detailed instructions on how to setup and run the software.
</details>
<hr>

### Abstract

Developers must comprehend the code they will maintain, meaning that the code must be legible and reasonably
self-descriptive. Unfortunately, there is still a lack of research and tooling that supports developers in understanding
their naming practices; whether the names they choose make sense, whether they are consistent, and whether they convey
the information required of them. In this paper, we present IDEAL, a tool that will provide feedback to developers about
their identifier naming practices. Among its planned features, it will support linguistic anti-pattern detection, which
is what will be discussed in this paper. IDEAL is designed to, and will, be extended to cover further anti-patterns,
naming structures, and practices in the near future. IDEAL is open-source and publicly available, with a demo video
available at: [https://youtu.be/fVoOYGe50zg](https://youtu.be/fVoOYGe50zg)

### Setup and Use

Details around setting up and using IDEAL are available [here](documentation/IDEAL/SetupAndUse.md).

### Evaluation Results

The results of our evaluation of IDEAL is available [here](https://drive.google.com/drive/folders/183J3_4xIdA3Xy762ryLrr0MVJbD5Oz8D).

### Naming Violation Examples

Examples of naming violations currently detected by IDEAL are available [here](documentation/IDEAL/NamingViolationExamples.md).

### IDEAL Architecture

Details around the architecture of IDEAL is available [here](documentation/IDEAL/Architecture.md).

### Naming Violations

-   ### [Arnaoudova et al.](documentaion/IDEAL/AntiPatternRules_Arnaoudova.md)
-   ### [SCANL](documentaion/IDEAL/AntiPatternRules_SCANL.md)

### Cite IDEAL

If you are using IDEAL in your research, please cite the following paper:

> Anthony Peruma, Venera Arnaoudova, and Christian D. Newman, "IDEAL: An Open-Source Identifier Name Appraisal Tool," 37th IEEE International Conference on Software Maintenance and Evolution (ICSME 2021), Luxembourg City, Luxembourg, September 27 - October 1, 2021.
