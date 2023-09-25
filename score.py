import os.path
import argparse
import sys

args = argparse.ArgumentParser(description = 'Score simulator.')
args.add_argument("bin_path", type = str, help = "bin_path")
args.add_argument("traces_dir_path", type = str, help = "traces_dir_path")
args = args.parse_args() 

# check
if not os.path.exists(args.bin_path) or args.bin_path[-5:] != "1core":
    print("illegal bin_path!")
    exit(0)

if not os.path.isdir(args.traces_dir_path):
    print("illegal traces_dir_path!")
    exit(0)
    
for path,d,filelist in os.walk(args.traces_dir_path):
    for filename in filelist:
        if filename[-8:] != "trace.xz":
            print("illegal trace files!")
            exit(0)
            
bin_path = args.bin_path
trace_file_path = args.traces_dir_path
print("bin_path: ",bin_path)
print("trace_file_path: ",trace_file_path)

traces = []
for path,d,filelist in os.walk(trace_file_path):
    for filename in filelist:
        t = os.path.join(path,filename)
        traces.append(t)
        
cmd = "./run_champsim.sh " + bin_path + " 50 100 "

print("please wait...")
student_num = "tmplog"
log_num = 0
for trace in traces:
    trace_cmd = cmd + trace + "> " + student_num + "_" + str(log_num)
    log_num = log_num + 1
    os.system(trace_cmd)

res = 0
for i in range(log_num):
    filename = student_num+"_"+str(i)
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if line[0:8] == "Finished":
                t = line.find("IPC")
                res += float(line[t+5:t+12])
                print("%s score: %f"  %(traces[int(filename.strip()[-1:])], float(line[t+5:t+12])))

print("avg score: %.6f" %(res/log_num))