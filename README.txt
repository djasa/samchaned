Tutorial:

1. Export channels list from TV to USB Drive. You will get
something like "channel_list_LE47C650_1001.scm"

2. Rename "channel_list_LE47C650_1001.scm" to 
"channel_list_LE47C650_1001.zip" and unpack it.

3. Copy map-AirA and map-CableA to examples directory

4. Run ./src/dumper.py ./examples/map-AirA to get list
of channels stored in TV (names nad frequencies) 

5. Create file sorted.txt with your custom channels list.
The list should look like this:

TVN24	383.25
DiscS	631.25
Discv	415.25
NatGe	431.25
TLC	639.25
Travl	231.25
13thS	463.25
TVPKu	319.25

Columns are separated by spaces. Names can NOT be longer than 5 chars.

6. Generate new map-AirA and map-CableA using following command

./src/generator.py -a ./examples/map-AirA \
	-c ./examples/map-CableA -s ./examples/sorted.txt \
	-d ./examples/out/

7. Copy new map-AirA and map-CableA to directory of unpacked 
channel_list_LE47C650_1001.zip

8. Create new channel_list_LE47C650_1001.zip with new map-AirA 
and map-CableA

9. Rename channel_list_LE47C650_1001.zip back to 
channel_list_LE47C650_1001.scm

10. Import channel_list_LE47C650_1001.scm into TV
