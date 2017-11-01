The format of the csv file should be like:

```
Option1,Option2
NameOfCriteria,ValueBetweenNegativeOneAndOne,Weight
NameOfCriteria,ValueBetweenNegativeOneAndOne,Weight
NameOfCriteria,ValueBetweenNegativeOneAndOne,Weight
...
```

`example.csv` has an example (duhh).

`-1` means Option1 wins completely, whereas `1` means Option2 wins completely.

`Weight` should be a value between `0` and `1` where `0` means you don't care
at all and `1` means it's super important to you.
