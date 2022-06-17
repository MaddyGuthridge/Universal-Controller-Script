
# Profiling

The script contains a simple profiler which can trace the execution path and
monitor performance of the script.

## Performance Monitoring

Sometimes, certain script behavior may cause performance issues. To help
analyze these issues, a simple performance profiler is included.

To get profiling info, enter the following into the script's output window:
`getContext().profiler.inspect()`

If you get an error `NoneType has no method 'inspect'`, ensure profiling is
enabled (add `"debug.profiling": True` to your `config.py` file).

You will get a print-out like the following, which contains information on
performance of the script:

```
 Name                                                   | Total (ms)     | Samples | Ave (ms)   | Max (ms)
==========================================================================================================
 tick.Device tick.lk-color-change                       |       78.08680 |     608 |    0.12843 |    0.71490
 tick.Device tick                                       |       87.93350 |     188 |    0.46773 |    3.50390
 tick.Tick <class 'plugs.special.transport.Transport'>  |        0.00000 |     188 |    0.00000 |    0.00000
 tick.Apply <class 'plugs.special.transport.Transport'> |        2.99360 |     188 |    0.01592 |    0.50400
 tick.Tick <class 'plugs.special.fallback.Fallback'>    |        0.00000 |     188 |    0.00000 |    0.00000
 tick.Apply <class 'plugs.special.fallback.Fallback'>   |       73.60720 |     188 |    0.39153 |    1.01750
 tick.getActive                                         |        0.00000 |     188 |    0.00000 |    0.00000
 tick.Tick <class 'plugs.standard.fl.flex.Flex'>        |     1238.25260 |     188 |    6.58645 |   21.99950
 tick.Apply <class 'plugs.standard.fl.flex.Flex'>       |        3.00640 |     188 |    0.01599 |    0.50170
 tick                                                   |     1419.92000 |     188 |    7.55277 |   24.98580
```

As can be seen, profiling is categorized into a hierarchy, separated by dots.

### Adding profiling to your code

Profiling is simple to add to your code. Import the required code from
the `common` module.

To profile an entire function, decorate it using `@profilerDecoration`.

To profile a single component of a function, use the `with ProfilerContext`
context manager.

Both of these require the name of the context to profile as an argument.

By default, event recognition and processing, as well as ticking and applying is
profiled for all plugins and devices.

## Stack Tracing

The profiler system can also be used to get stack traces if FL Studio crashes
or freezes due to the script's behavior. To enable tracing of profiler
contexts, enabled `"debug.exec_tracing"` in your `config.py`. Note that this
causes a massive amount of terminal output, so should be used sparingly.
