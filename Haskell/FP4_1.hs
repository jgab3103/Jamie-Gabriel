
-- load this script with gchi FP4_1.hs
-- reload with :reload
-- :? help
-- funcioins are lower case
-- lists have s suffix
-- each def in same column - 

double x = x + x
quadruple x = double (double x)


factorial n = product [1 ..n]

average ns = sum ns `div` length ns -- will accept list

n = a `div` length xs
    where
        a = 10
        xs = [3,4,5,4,5]

