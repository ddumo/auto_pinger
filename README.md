# auto_pinger
This is a working project that is used to take a source list of IPs or Hostnames, and output their status, and basic information about the system itself.


Python Requirements:
1 - Python3  apt install python3 OR apt install python-as-python3
2 - pip  --> apt install pip3
3 - Pandas --> pip3 install pandas
4 - Numpy --> pip3 install numpy
5 - A CSV with hostnames or IPs you'd like to get informaiton about

install:
1 - cd to the directory your want it in.
2 - git clone https://github.com/ddumo/auto_pinger.git
3 - to start the file: python3 auto_pinger.py
 
Note: if you want to make the program to be able to be called from an easier name say "ping" or "auto" do the following:
   1 - chmod+x auto_pinger.py 
   2 - sudo cp auto_pinger.py /bin/auto <-- replace "auto" with how you'd like to call the program
