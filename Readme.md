# Single Server Queueing System Simulation
 
A simulation design of a single-server queueing system. The input file provides 
mean interarrival time, mean service time, and number of customers.  
* Three performance metrics average delay in queue, average number in queue, server utilization are measured. 
* The ratio, k, between the mean service time and the mean interarrival time is varied. The experiment is run for k = 0.5, 0.6, 0.7, 0.8, 0.9. 
* Various statistics [min, max, median, P(x), F(x)] for the uniform and exponential random variates during this experiment are shown. 

## Results

An example measurement-
```
Number of Customers 1000
Mean interarrival time 1.00 min
Mean service time 0.5 to 0.9 mins

k	Avg delay in queue (mins)	Avg number in queue	Server utilization	Total sim time (mins)
0.5	0.43	0.42	0.48	1028.65
0.6	0.86	0.81	0.6	997.94
0.7	1.61	1.35	0.69	1015.22
0.8	3.26	2.88	0.82	1005.99
0.9	6.55	5.46	0.88	1012.46

Uniform and Exponential random variates 
Uniform: min 0.006, max 0.998, median 0.41
Exp: min 0.001, max 4.06, median 0.734
```
 