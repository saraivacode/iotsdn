# iotsdn

## About this code

A solution that uses SDN to deal with IOT network traffic considering the requirements of different applications in a smart citie..

This implementation uses the Mininet-wifi emulator (https://github.com/intrig-unicamp/mininet-wifi)

The codes here refer to a performance evaluation is a scenario with nine IoT devices (stations) and three servers of different applications with a heterogeneous network with the representation of LTE, Wifi, and D2D (BLE) technologies.

<img src="https://github.com/saraivacode/iotsdn/blob/master/implementacao.jpg" width="700">

This implementation permits to compare the results of PDR, throughput and RTT obtained with the use of the proposed solution with the default one where the devices connects to a network without considering the requirements of the IoT applications.

### Implementation scripts

#### 1. The main script that builds the topology in Mininet-wifi, with general emulation parameters and starts the experiment:
https://github.com/saraivacode/iotsdn/blob/master/main2.py

##### main2.py options:

-pv: proposed solution approach   
-df: default approach

#### 2. Shell script used to generate in the IoT stations the traffic related to the applications:
https://github.com/saraivacode/framework_its_sdn/blob/master/carcon.sh

##### For Generic Internet app: https://github.com/saraivacode/iotsdn/blob/master/carconiotgi.sh
##### For Industrial Monitoring app: https://github.com/saraivacode/iotsdn/blob/master/carconiotim.sh
##### For Smart Home app: https://github.com/saraivacode/iotsdn/blob/master/carconiotsh.sh

#### 3. Codes to compile the results:

##### Shell code that is used to extract, from the files generated in emulation, the information necessary to compile the results:
https://github.com/saraivacode/iotsdn/blob/master/tratamento_c3iot.sh

###### tratamento_c3.sh options:

fn: For any approach (will be adjusted)

##### R codes to generate the graphs

1 - Our approach results:
https://github.com/saraivacode/iotsdn/blob/master/iot1.R

2 - Default approach results:
https://github.com/saraivacode/iotsdn/blob/master/iot2.R

### Execution example 1

##### step 1 (Run experiment with proposed approach): # main2.py -pv

##### step 2 (Adjust the results): # tratamento_c3.sh fn

##### step 3 (Generate in R the graphs of the results for the proposed approach): execute in R iot1.R file

### Execution example 2

##### step 1 (Run experiment with default approach): # main2.py -df

##### step 2 (Adjust the results): # tratamento_c3.sh fn

##### step 3 (Generate in R the graphs of the results for the default approach): execute in R iot2.R file
