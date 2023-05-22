# Binary_trees_speed

### In this project we compere speeds of searching in binary trees. We use dictionary of english words to test our trees

We have 4 different situations. This is just one take.

1. Searching in python list in alphabetic order using `**.index()**` = 0.12200021743774414s
2. Searching in tree that has been filled alphabetically = 0.02299189567565918s
3. Searching in random ordered tree = 0.010999679565429688s
4. Searching in balanced  tree = 0.00905299186706543s

---
Essentially the fastest are last two methods, and it is generally good to balance your tree. Random order can sometimes be quite lucky too.

In theory alphabetic ordered tree search should be the slowest because it is just linear search then. But it is not always like this in my program, if we take more words from dictionary we can demonstrate better its slowness. Although building alphabetic ordered tree is by far the longest process here.

And python built in method is pretty bad here because we make list sorted, and it is designed for more random distributions.
