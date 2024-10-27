# Script to evaluate performance of language models with ollama on edge devices

### Get Started

Run the following code to execute the test

```
python3 run_test.py -m MODEL 
```

**NOTE: ** MODEL in this case is the model that can execute locally with ```ollama run MODEL```


### Argument

- model: The model to be tested
- nt / num-turn: The number of times to run benchmarking
- ni / num-iteration: The number of iteration to run in each benchmarking
- st / sleep-time: The time for the program to sleep between two consecutive turns



### How it works

- The model will be test to process random text from test data and gerate the output. The information of processing & generating speed can be achieved through `ollama` library.

- The model will be run for `nt` turns and in each turn it will tested on `ni` texts


- After each turn, the code will sleep for `st` minutes for cooling down (especially naked raspberry). If the temperature is not high, we can consider reduce the sleeping time.



