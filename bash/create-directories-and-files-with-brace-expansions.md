# Use brace expansion to quickly create directories and files

I knew that I could use brace expansion to quickly create files like:

```bash
touch foo{,1,2,3,4}.txt
```

or directories like:

```bash
mkdir -p project{1,2}/src/test
```

What I didn't know was that I could use brace expansion to quickly create directories and files with a cartesian product of multiple sets of values.

```bash
touch project{1,2}/src/test/test{1,2,3}.py

# let's see our output
➜ tree project?
project1
└── src
    └── test
        ├── test1.py
        ├── test2.py
        └── test3.py
project2
└── src
    └── test
        ├── test1.py
        ├── test2.py
        └── test3.py

4 directories, 6 files
```

We can also use ranges like `{4..10}` to create a range of files.

```bash
➜ touch project{1,2}/src/test/test{4..10}.py
➜ tree project?
project1
└── src
    └── test
        ├── test1.py
        ├── test10.py
        ├── test2.py
        ├── test3.py
        ├── test4.py
        ├── test5.py
        ├── test6.py
        ├── test7.py
        ├── test8.py
        └── test9.py
project2
└── src
    └── test
        ├── test1.py
        ├── test10.py
        ├── test2.py
        ├── test3.py
        ├── test4.py
        ├── test5.py
        ├── test6.py
        ├── test7.py
        ├── test8.py
        └── test9.py

4 directories, 20 files
```

We can also use more combinations like `{A..C}` and `{1..3}` for a cartesian product between sets of values.

```bash
touch project{1,2}/src/test/test{A..C}{1..3}.py

➜ tree project?
project1
└── src
    └── test
        ├── test1.py
        ├── test10.py
        ├── test2.py
        ├── test3.py
        ├── test4.py
        ├── test5.py
        ├── test6.py
        ├── test7.py
        ├── test8.py
        ├── test9.py
        ├── testA1.py
        ├── testA2.py
        ├── testA3.py
        ├── testB1.py
        ├── testB2.py
        ├── testB3.py
        ├── testC1.py
        ├── testC2.py
        └── testC3.py
project2
└── src
    └── test
        ├── test1.py
        ├── test10.py
        ├── test2.py
        ├── test3.py
        ├── test4.py
        ├── test5.py
        ├── test6.py
        ├── test7.py
        ├── test8.py
        ├── test9.py
        ├── testA1.py
        ├── testA2.py
        ├── testA3.py
        ├── testB1.py
        ├── testB2.py
        ├── testB3.py
        ├── testC1.py
        ├── testC2.py
        └── testC3.py

4 directories, 38 files
```
